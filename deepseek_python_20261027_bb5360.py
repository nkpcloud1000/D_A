from dataclasses import dataclass
from typing import Optional

@dataclass
class Candidate:
    symbol: str
    price: float
    float_m: Optional[float]
    premarket_rvol_tod: Optional[float]
    regular_rvol_tod: Optional[float]
    gap_pct: float
    premarket_volume: int
    regular_volume: int
    last_five_min_volume: int
    spread_pct: Optional[float]
    catalyst_verified: bool
    catalyst_auto: bool
    hod_break: bool
    above_vwap: bool
    dilution_score: Optional[int] = None  # 1-5, warning only

def qualifies_ignition(c: Candidate, price_min=2.0, price_max=50.0,
                       max_float_m=10.0, min_rvol=5.0,
                       min_pm_volume=50_000, min_gap=4.0) -> tuple[bool, list[str]]:
    reasons = []
    if not (price_min <= c.price <= price_max):
        reasons.append("price_out_of_band")
    if c.float_m is None or c.float_m > max_float_m:
        reasons.append("float_unknown_or_too_large")
    if c.premarket_rvol_tod is None or c.premarket_rvol_tod < min_rvol:
        reasons.append("premarket_rvol_below_threshold")
    if c.premarket_volume < min_pm_volume:
        reasons.append("premarket_volume_too_low")
    if c.gap_pct < min_gap:
        reasons.append("gap_too_small")
    if c.spread_pct is None or c.spread_pct > 1.0:
        reasons.append("spread_unknown_or_too_wide")
    if not c.catalyst_verified and not c.catalyst_auto:
        reasons.append("no_catalyst")
    return (len(reasons) == 0, reasons)

def qualifies_continuation(c: Candidate, price_min=2.0, price_max=50.0,
                           max_float_m=20.0, min_rvol=5.0,
                           min_five_min=100_000) -> tuple[bool, list[str]]:
    reasons = []
    if not (price_min <= c.price <= price_max):
        reasons.append("price_out_of_band")
    if c.float_m is None or c.float_m > max_float_m:
        reasons.append("float_unknown_or_too_large")
    if c.regular_rvol_tod is None or c.regular_rvol_tod < min_rvol:
        reasons.append("regular_rvol_below_threshold")
    if not c.hod_break:
        reasons.append("no_hod_break")
    if not c.above_vwap:
        reasons.append("below_vwap")
    if c.last_five_min_volume < min_five_min:
        reasons.append("five_min_volume_too_low")
    if c.spread_pct is None or c.spread_pct > 1.0:
        reasons.append("spread_unknown_or_too_wide")
    return (len(reasons) == 0, reasons)