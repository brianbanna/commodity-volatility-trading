"""Volatility risk premium backtest. SPEC Part D deliverable D11, sub strategy 1.

Signal: 30 day constant maturity ATM implied minus the D9 HAR forecast, z scored on a
trailing 252 days. Entry beyond plus or minus 1.

Structure: the nearest 25 to 45 day ATM straddle, delta hedged, rolled or closed at 10
days to expiry. Vega targeted at 25 bps per volatility point. 3x premium stop. No short
volatility entries within 5 days of a scheduled major release.

Gate: the point in time audit passes, and the history window honesty sentence is present
verbatim in the note. That sentence is written before the results are looked at, not
after. With no affordable history purchase the collected window is the backtest and it is
thin for this sub strategy; the note says so plainly rather than presenting a Sharpe from
a short window as though the window were adequate.

Costs: options bid ask as a percent of premium per side, WTI ATM 1.5 and wings 3, Henry
Hub ATM 2 and wings 4, ags ATM 2 and wings 4. Futures hedges per the project 2 model.
The 1x, 2x, 4x sensitivity table is mandatory. T5 trigger: if the Sharpe sign flips
between 1x and 2x, the strategy is labeled not robust to costs and excluded from every
headline, and the table ships regardless.
"""
