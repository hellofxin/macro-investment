#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
portfolio_pnl.py — 17 产品组合盈亏复算（一直不动 vs 按规则减仓）

用途
----
每次校准后复算：
  1) 一直不动：按 03_PORTFOLIO v5 目标权重，在 --start 买入并持有到 --end；
  2) 按规则：在指定日期卖出指定产品的指定比例，回款转入 511360 短融ETF，再持有到 --end；
  3) 输出期末市值、盈亏、收益率、最大回撤、逐产品盈亏贡献、期末权重。

默认口径与 00_STATE §3.1/§3.2 一致：
  - 初始 1000 万，目标权重见 PRODUCTS；
  - 数据源：腾讯行情日线（前复权）；
  - R1 默认 2026-10-22，卖出 159516/516820/159201 各 1/3，回款转 511360；
  - 不计交易费用、冲击成本、分红税。

常用命令
--------
  # 一直不动 + 默认 R1（2026-10-22 三只各 1/3）
  python tools/portfolio_pnl.py --start 2026-07-01 --end 2026-11-20

  # 只算一直不动
  python tools/portfolio_pnl.py --start 2026-07-01 --end 2026-11-20 --no-rule

  # 自定义卖出动作（可重复；frac=1.0 表示清仓）
  python tools/portfolio_pnl.py --start 2026-07-01 --end 2026-11-20 \
    --sell 2026-10-22:159516:0.333333 \
    --sell 2026-10-22:516820:0.333333 \
    --sell 2026-10-22:159201:0.333333

  # 输出可直接粘贴到 STATE §3.1 的 Markdown 产品行（前 7 列）
  python tools/portfolio_pnl.py --start 2026-07-01 --end 2026-11-20 --markdown

  # 导出 JSON / CSV
  python tools/portfolio_pnl.py --start 2026-07-01 --end 2026-11-20 --json
  python tools/portfolio_pnl.py --start 2026-07-01 --end 2026-11-20 --csv tools/pnl.csv

  # 强制刷新行情缓存
  python tools/portfolio_pnl.py --start 2026-07-01 --end 2026-11-20 --refresh

注意
----
- 腾讯接口单次最多约 320 根日线；当前区间足够。若 --start 太早，请分段或改用其他数据源。
- 缓存目录 tools/.cache/ 可按需删除；--refresh 会重新拉取。
- 本脚本只做“规则路径”的机械复算，不构成投资建议。
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import date, datetime

# ---------------------------------------------------------------------------
# 组合定义（与 03_PORTFOLIO v5 一致；权重合计 100%）
# ---------------------------------------------------------------------------
PRODUCTS = [
    {"code": "511360", "name": "短融ETF",       "symbol": "sh511360", "weight": 0.15, "category": "现金/短债"},
    {"code": "511520", "name": "政金债ETF",     "symbol": "sh511520", "weight": 0.05, "category": "利率债"},
    {"code": "511260", "name": "十年国债ETF",   "symbol": "sh511260", "weight": 0.05, "category": "利率债"},
    {"code": "518880", "name": "黄金ETF",       "symbol": "sh518880", "weight": 0.10, "category": "黄金"},
    {"code": "512890", "name": "红利低波ETF",   "symbol": "sh512890", "weight": 0.15, "category": "红利"},
    {"code": "159201", "name": "自由现金流ETF", "symbol": "sz159201", "weight": 0.05, "category": "红利"},
    {"code": "511380", "name": "可转债ETF",     "symbol": "sh511380", "weight": 0.05, "category": "可转债"},
    {"code": "510300", "name": "沪深300ETF",    "symbol": "sh510300", "weight": 0.05, "category": "宽基"},
    {"code": "159915", "name": "创业板ETF",     "symbol": "sz159915", "weight": 0.10, "category": "宽基"},
    {"code": "159516", "name": "半导体设备ETF", "symbol": "sz159516", "weight": 0.04, "category": "铲子线"},
    {"code": "515880", "name": "通信ETF",       "symbol": "sh515880", "weight": 0.04, "category": "铲子线"},
    {"code": "159326", "name": "电网设备ETF",   "symbol": "sz159326", "weight": 0.03, "category": "铲子线"},
    {"code": "512400", "name": "有色金属ETF",   "symbol": "sh512400", "weight": 0.03, "category": "铲子线"},
    {"code": "513120", "name": "港股创新药ETF", "symbol": "sh513120", "weight": 0.03, "category": "医药"},
    {"code": "516820", "name": "医疗创新ETF",   "symbol": "sh516820", "weight": 0.02, "category": "医药"},
    {"code": "513130", "name": "恒生科技ETF",   "symbol": "sh513130", "weight": 0.03, "category": "其他"},
    {"code": "512070", "name": "证券保险ETF",   "symbol": "sh512070", "weight": 0.03, "category": "其他"},
]
CODE_TO_PRODUCT = {p["code"]: p for p in PRODUCTS}
DEFAULT_START = "2026-07-01"
DEFAULT_R1_DATE = "2026-10-22"
DEFAULT_R1_SELL = "159516:0.333333,516820:0.333333,159201:0.333333"
DEFAULT_CASH = "511360"
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".cache")
API = "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get"


# ---------------------------------------------------------------------------
# 行情获取与缓存
# ---------------------------------------------------------------------------
def fetch_kline(symbol: str, start: str, end: str, refresh: bool = False) -> dict:
    """拉取腾讯前复权日线；同一 (symbol,start,end) 默认走缓存。"""
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache = os.path.join(CACHE_DIR, f"{symbol}_{start}_{end}.json")
    if os.path.exists(cache) and not refresh:
        with open(cache, "r", encoding="utf-8") as f:
            return json.load(f)

    params = {"param": f"{symbol},day,{start},{end},320,qfq"}
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(f"行情拉取失败 {symbol}: {exc}") from exc

    if not data.get("data"):
        raise SystemExit(f"行情返回为空 {symbol}: {data}")
    with open(cache, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    time.sleep(0.15)  # 温和限速
    return data


def parse_prices(data: dict, symbol: str) -> dict[str, float]:
    """腾讯日线行格式：[date, open, close, high, low, volume]；取 close=索引2。"""
    node = data.get("data", {}).get(symbol, {})
    rows = node.get("qfqday") or node.get("day") or []
    prices: dict[str, float] = {}
    for row in rows:
        if len(row) >= 3:
            try:
                prices[row[0]] = float(row[2])
            except (TypeError, ValueError):
                continue
    return prices


def load_prices(start: str, end: str, refresh: bool = False) -> tuple[dict[str, dict[str, float]], list[str]]:
    prices: dict[str, dict[str, float]] = {}
    for p in PRODUCTS:
        data = fetch_kline(p["symbol"], start, end, refresh=refresh)
        px = parse_prices(data, p["symbol"])
        if not px:
            raise SystemExit(f"{p['code']} {p['name']} 无行情数据")
        prices[p["code"]] = px

    common = set.intersection(*(set(px) for px in prices.values()))
    dates = sorted(d for d in common if start <= d <= end)
    if not dates:
        raise SystemExit(f"{start} → {end} 无共同交易日")
    return prices, dates


# ---------------------------------------------------------------------------
# 模拟
# ---------------------------------------------------------------------------
def parse_actions(args: argparse.Namespace) -> list[tuple[str, str, float]]:
    """返回 [(date, code, frac)]。--sell 优先；否则用 R1 默认清单。"""
    actions: list[tuple[str, str, float]] = []
    if args.no_rule:
        return actions
    if args.sell:
        for item in args.sell:
            parts = item.split(":")
            if len(parts) != 3:
                raise SystemExit(f"--sell 格式应为 DATE:CODE:FRAC，收到：{item}")
            d, code, frac = parts
            actions.append((d, code, float(frac)))
    elif not args.no_rule:
        for item in args.r1_sell.split(","):
            item = item.strip()
            if not item:
                continue
            code, frac = item.split(":")
            actions.append((args.r1_date, code, float(frac)))

    for d, code, frac in actions:
        if code not in CODE_TO_PRODUCT:
            raise SystemExit(f"未知代码：{code}")
        if not (0 < frac <= 1):
            raise SystemExit(f"卖出比例应在 (0,1]：{code} {frac}")
        try:
            datetime.strptime(d, "%Y-%m-%d")
        except ValueError as exc:
            raise SystemExit(f"日期格式应为 YYYY-MM-DD：{d}") from exc
    return actions


def next_trading_day(dates: list[str], target: str) -> str:
    for d in dates:
        if d >= target:
            return d
    raise SystemExit(f"卖出日期 {target} 之后无交易日")


def simulate(
    prices: dict[str, dict[str, float]],
    dates: list[str],
    initial: float,
    actions: list[tuple[str, str, float]],
    cash_code: str,
) -> dict:
    """按目标权重买入，执行 actions 中的卖出（回款转 cash_code），持有到期末。"""
    if cash_code not in CODE_TO_PRODUCT:
        raise SystemExit(f"现金替代代码不在组合内：{cash_code}")

    first, last = dates[0], dates[-1]
    shares = {p["code"]: initial * p["weight"] / prices[p["code"]][first] for p in PRODUCTS}
    initial_shares = dict(shares)
    realized = {p["code"]: 0.0 for p in PRODUCTS}
    cash_lots: list[tuple[float, float]] = []  # (shares, buy_price) for cash_code

    # 将动作映射到交易日
    action_map: dict[str, list[tuple[str, float]]] = {}
    for target, code, frac in actions:
        day = next_trading_day(dates, target)
        if day != target:
            print(f"⚠️  {target} 非交易日，{code} 卖出顺延至 {day} 收盘", file=sys.stderr)
        action_map.setdefault(day, []).append((code, frac))

    values: list[float] = []
    for d in dates:
        if d in action_map:
            cash = 0.0
            for code, frac in action_map[d]:
                qty = shares[code] * frac
                px = prices[code][d]
                realized[code] += qty * (px - prices[code][first])
                shares[code] -= qty
                cash += qty * px
            if cash:
                buy_px = prices[cash_code][d]
                qty_cash = cash / buy_px
                shares[cash_code] += qty_cash
                cash_lots.append((qty_cash, buy_px))
        values.append(sum(shares[c] * prices[c][d] for c in shares))

    final = values[-1]
    pnl = {}
    for c in shares:
        if c == cash_code:
            pnl[c] = initial_shares[c] * (prices[c][last] - prices[c][first]) + sum(
                q * (prices[c][last] - buy_px) for q, buy_px in cash_lots
            )
        else:
            pnl[c] = realized[c] + shares[c] * (prices[c][last] - prices[c][first])

    total_pnl = final - initial
    if abs(sum(pnl.values()) - total_pnl) > 0.01:
        print(
            f"⚠️  逐产品盈亏合计 {sum(pnl.values()):.2f} 与总盈亏 {total_pnl:.2f} 不一致（四舍五入/数据源）",
            file=sys.stderr,
        )

    end_weights = {c: shares[c] * prices[c][last] / final for c in shares}
    returns = {c: (prices[c][last] / prices[c][first] - 1) for c in shares}
    peak = values[0]
    max_dd = 0.0
    for v in values:
        peak = max(peak, v)
        max_dd = min(max_dd, v / peak - 1)

    return {
        "first": first,
        "last": last,
        "initial": initial,
        "final": final,
        "pnl": total_pnl,
        "return": final / initial - 1,
        "max_drawdown": max_dd,
        "values": values,
        "end_weights": end_weights,
        "product_pnl": pnl,
        "product_return": returns,
        "shares": shares,
        "actions": actions,
    }


# ---------------------------------------------------------------------------
# 输出
# ---------------------------------------------------------------------------
def fmt_money(x: float) -> str:
    return f"{x:+,.2f}"


def print_summary(hold: dict, rule: dict | None) -> None:
    print()
    print(f"== 汇总（初始 {hold['initial']:.2f} 万，{hold['first']} → {hold['last']}）==")
    print()
    print("| 路径 | 期末市值(万) | 盈亏(万) | 收益率 | 最大回撤 |")
    print("|---|---:|---:|---:|---:|")
    print(f"| 一直不动 | {hold['final']:,.2f} | {fmt_money(hold['pnl'])} | {hold['return']*100:+.2f}% | {hold['max_drawdown']*100:.2f}% |")
    if rule:
        label = rule_label(rule["actions"])
        print(f"| {label} | {rule['final']:,.2f} | {fmt_money(rule['pnl'])} | {rule['return']*100:+.2f}% | {rule['max_drawdown']*100:.2f}% |")
        print(
            f"| 差额（按规则-不动） | {rule['final']-hold['final']:+,.2f} | {fmt_money(rule['pnl']-hold['pnl'])} | "
            f"{(rule['return']-hold['return'])*100:+.2f}pp | {(rule['max_drawdown']-hold['max_drawdown'])*100:+.2f}pp |"
        )


def _is_default_r1(actions: list[tuple[str, str, float]]) -> bool:
    if not actions:
        return False
    default_codes = sorted(x.split(":")[0] for x in DEFAULT_R1_SELL.split(","))
    dates = sorted({d for d, _, _ in actions})
    codes = sorted({c for _, c, _ in actions})
    return len(dates) == 1 and codes == default_codes


def rule_label(actions: list[tuple[str, str, float]]) -> str:
    if not actions:
        return "按规则"
    dates = sorted({d for d, _, _ in actions})
    if _is_default_r1(actions):
        return f"按规则 R1@{dates[0]}"
    codes = sorted({c for _, c, _ in actions})
    return f"按规则({'/'.join(dates)}) {','.join(codes)}"


def markdown_rule_label(actions: list[tuple[str, str, float]]) -> str:
    """STATE §3.1 表头用的短标签。"""
    if not actions:
        return "规则后应持"
    dates = sorted({d for d, _, _ in actions})
    if _is_default_r1(actions):
        return f"R1后应持（{dates[0]}）"
    return f"规则后应持（{'/'.join(dates)}）"


def print_products(hold: dict, rule: dict | None, markdown: bool = False) -> None:
    print()
    print("== 逐产品（一直不动）==")
    print()
    print("| 代码 | 名称 | 类别 | 目标权重 | 期末权重 | 自起始盈亏(万) | 收益率 |")
    print("|:--:|---|---|---:|---:|---:|---:|")
    for p in PRODUCTS:
        c = p["code"]
        print(
            f"| {c} | {p['name']} | {p['category']} | {p['weight']*100:.0f}% | "
            f"{hold['end_weights'][c]*100:.2f}% | {fmt_money(hold['product_pnl'][c])} | "
            f"{hold['product_return'][c]*100:+.2f}% |"
        )
    print(f"| **合计** | **17 产品** | — | **100%** | **100%** | **{fmt_money(hold['pnl'])}** | **{hold['return']*100:+.2f}%** |")

    if rule:
        print()
        print(f"== 逐产品（{rule_label(rule['actions'])}）==")
        print()
        print("| 代码 | 名称 | 类别 | 目标权重 | 期末权重 | 自起始盈亏(万) | 收益率 |")
        print("|:--:|---|---|---:|---:|---:|---:|")
        for p in PRODUCTS:
            c = p["code"]
            print(
                f"| {c} | {p['name']} | {p['category']} | {p['weight']*100:.0f}% | "
                f"{rule['end_weights'][c]*100:.2f}% | {fmt_money(rule['product_pnl'][c])} | "
                f"{rule['product_return'][c]*100:+.2f}% |"
            )
        print(f"| **合计** | **17 产品** | — | **100%** | **100%** | **{fmt_money(rule['pnl'])}** | **{rule['return']*100:+.2f}%** |")

    if markdown and rule:
        print()
        print("== STATE §3.1 可粘贴行（前 7 列；当前操作/备注需手工补）==")
        print()
        print(f"| 代码 | 名称 | 类别 | 目标权重(v5) | {rule['last']}实际估算 | 自{rule['first']}盈亏(万/收益率) | {markdown_rule_label(rule['actions'])} |")
        print("|:--:|---|---|---:|---:|---:|---:|")
        for p in PRODUCTS:
            c = p["code"]
            print(
                f"| {c} | {p['name']} | {p['category']} | {p['weight']*100:.0f}% | "
                f"{hold['end_weights'][c]*100:.2f}% | {fmt_money(hold['product_pnl'][c])}（{hold['product_return'][c]*100:+.2f}%） | "
                f"{rule['end_weights'][c]*100:.2f}% |"
            )
        print(f"| **合计** | **17 产品** | — | **100%** | **100%** | **{fmt_money(hold['pnl'])}（{hold['return']*100:+.2f}%）** | **100%** |")


def write_csv(path: str, hold: dict, rule: dict | None) -> None:
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        header = ["code", "name", "category", "target_weight", "hold_end_weight", "hold_pnl", "hold_return"]
        if rule:
            header += ["rule_end_weight", "rule_pnl", "rule_return"]
        w.writerow(header)
        for p in PRODUCTS:
            c = p["code"]
            row = [
                c,
                p["name"],
                p["category"],
                f"{p['weight']:.4f}",
                f"{hold['end_weights'][c]:.6f}",
                f"{hold['product_pnl'][c]:.4f}",
                f"{hold['product_return'][c]:.6f}",
            ]
            if rule:
                row += [
                    f"{rule['end_weights'][c]:.6f}",
                    f"{rule['product_pnl'][c]:.4f}",
                    f"{rule['product_return'][c]:.6f}",
                ]
            w.writerow(row)


def to_json(hold: dict, rule: dict | None, actions: list[tuple[str, str, float]]) -> dict:
    def pack(res: dict) -> dict:
        return {
            "first": res["first"],
            "last": res["last"],
            "initial": res["initial"],
            "final": round(res["final"], 4),
            "pnl": round(res["pnl"], 4),
            "return": round(res["return"], 6),
            "max_drawdown": round(res["max_drawdown"], 6),
            "end_weights": {c: round(v, 6) for c, v in res["end_weights"].items()},
            "product_pnl": {c: round(v, 4) for c, v in res["product_pnl"].items()},
            "product_return": {c: round(v, 6) for c, v in res["product_return"].items()},
        }

    out = {"hold": pack(hold), "actions": [{"date": d, "code": c, "frac": f} for d, c, f in actions]}
    if rule:
        out["rule"] = pack(rule)
        out["diff"] = {
            "final": round(rule["final"] - hold["final"], 4),
            "pnl": round(rule["pnl"] - hold["pnl"], 4),
            "return": round(rule["return"] - hold["return"], 6),
            "max_drawdown": round(rule["max_drawdown"] - hold["max_drawdown"], 6),
        }
    return out


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="17 产品组合盈亏复算：一直不动 vs 按规则减仓（默认 R1 2026-10-22）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--start", default=DEFAULT_START, help=f"起始日期，默认 {DEFAULT_START}")
    p.add_argument("--end", default=date.today().isoformat(), help="结束日期，默认今天")
    p.add_argument("--initial", type=float, default=1000.0, help="初始资金（万），默认 1000")
    p.add_argument("--r1-date", default=DEFAULT_R1_DATE, help=f"默认 R1 日期，默认 {DEFAULT_R1_DATE}")
    p.add_argument("--r1-sell", default=DEFAULT_R1_SELL, help=f"默认 R1 卖出清单 code:frac，默认 {DEFAULT_R1_SELL}")
    p.add_argument("--cash", default=DEFAULT_CASH, help=f"回款转入的现金替代代码，默认 {DEFAULT_CASH}")
    p.add_argument("--sell", action="append", metavar="DATE:CODE:FRAC", help="自定义卖出动作，可重复；给此参数时忽略 --r1-*")
    p.add_argument("--no-rule", action="store_true", help="只算一直不动")
    p.add_argument("--refresh", action="store_true", help="强制刷新行情缓存")
    p.add_argument("--json", action="store_true", help="输出 JSON")
    p.add_argument("--csv", metavar="PATH", help="输出逐产品 CSV")
    p.add_argument("--markdown", action="store_true", help="额外输出 STATE §3.1 可粘贴行")
    return p


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    args = build_parser().parse_args(argv)
    actions = parse_actions(args)

    prices, dates = load_prices(args.start, args.end, refresh=args.refresh)
    hold = simulate(prices, dates, args.initial, [], args.cash)
    rule = simulate(prices, dates, args.initial, actions, args.cash) if actions else None

    if args.json:
        print(json.dumps(to_json(hold, rule, actions), ensure_ascii=False, indent=2))
    else:
        print_summary(hold, rule)
        print_products(hold, rule, markdown=args.markdown)

    if args.csv:
        write_csv(args.csv, hold, rule)
        print(f"\nCSV 已写入：{args.csv}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
