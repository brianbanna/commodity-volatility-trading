"""Event volatility. SPEC Part D deliverables D12 and D13, sub strategy 2.

D12 The event study. Per release type, EIA petroleum Wednesdays, EIA gas Thursdays, USDA
    WASDE: the priced move, taken from the shortest straddle spanning the release with the
    multi day adjustment and the formula documented, against the realized settlement to
    settlement distribution. Conditional splits for routine against report heavy weeks.
    Implied volatility run up and crush term structure exhibits.
    Gate: publishable on its own, every figure regenerable. This deliverable is the
    standalone artifact that stands even if nothing else in the project ships, and it is
    protected from the cut order in SPEC Part I.

D13 Event trading backtest. Sell rich, meaning the top conditional quartile, and own
    cheap. Hedge once at entry, exit at the post release settlement. Fixed 15 bps premium
    at risk per event. The implied volatility crush series ships as a reported exhibit.
    Gate: the same point in time discipline, and per event accounting written out
    explicitly rather than aggregated.

Release timestamps live in config/event_calendar.yaml in UTC and nowhere else. Daylight
saving is handled in that file only. A timestamp computed anywhere else in the codebase is
a defect. Vintages are as published on the day: a revised EIA or WASDE figure is lookahead
and is refused, not adjusted for.
"""
