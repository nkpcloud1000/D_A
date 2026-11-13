# my script
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
    regular_volume: int
    last_five_min_volume: int
    spread_pct: Optional[float]

    dilution_score: Optional[int] = None  # 1-5, warning only

def qualifies_ignition(c: Candidate, price_min=5.
.0, price_max=55.0,
                       max_float_m=10.0, min_rvol=5.0,
                       min_pm_volume=50_000, min_gap=4.0) -> tuple[bool, list[str]]:
    reasons = []
    if not (price_min <= c.price <= price_max):
     
    if not c.above_vwap:
        reasons.append("below_vwap")
    if c.last_five_min_volume < min_five_min:
        reasons.append("five_min_volume_too_low")
    if c.spread_pct is None or c.spread_pct > 1.0:
        reasons.append("spread_unknown_or_too_wide")
    return (len(reasons) == 0, reasons)
