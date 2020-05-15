import datetime

filters = {
    "start_date": datetime.date,
    "end_date": datetime.date,
    "std_expr": bool,
    "contract_size": int,
    "entry_dte": (int, tuple),
    "entry_days": int,
    "leg1_delta": (int, float, tuple),
    "leg2_delta": (int, float, tuple),
    "leg3_delta": (int, float, tuple),
    "leg4_delta": (int, float, tuple),
    "leg1_strike_pct": (int, float, tuple),
    "leg2_strike_pct": (int, float, tuple),
    "leg3_strike_pct": (int, float, tuple),
    "leg4_strike_pct": (int, float, tuple),
    "entry_spread_price": (int, float, tuple),
    "entry_spread_delta": (int, float, tuple),
    "entry_spread_yield": (int, float, tuple),
    "exit_dte": int,
    "exit_hold_days": int,
    "exit_leg_1_delta": (int, float, tuple),
    "exit_leg_1_otm_pct": (int, float, tuple),
    "exit_profit_loss_pct": (int, float, tuple),
    "exit_spread_delta": (int, float, tuple),
    "exit_spread_price": (int, float, tuple),
    "exit_strike_diff_pct": (int, float, tuple),
}


def _type_check(filter):
    # return all([isinstance(filter[f], filters[f]) for f in filter])
    return True


def singles_checks(filter):
    return "leg1_delta" in filter and _type_check(filter)