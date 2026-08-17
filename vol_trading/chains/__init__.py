"""Chain, surface, and quality layers. SPEC Part D deliverables D5, D6, D7.

D5  Chain builder. Parses raw into per day per market chains: strikes, expiries,
    settlements, implied volatilities, open interest, volume. Moneyness filter 0.5 to 2.0
    of forward. Open interest floor 100 across the chain.
    Gate: rebuilding from raw reproduces byte identical output. That is the guarantee that
    processed data is disposable and raw data is the record.

D6  Surface builder. Black 76 inversion by a Brent root finder wrapping
    `statarb.pricing.black76`, cross checked against the implied volatilities the CME tool
    publishes. Flat short rate from config; the rate sensitivity at these tenors is
    documented as negligible rather than assumed away silently. ATM interpolated at the
    forward. 25 delta risk reversal and butterfly. Smile as a cubic spline in delta space
    with documented extrapolation; SVI is deferred, not attempted. 30 and 60 day constant
    maturity by linear interpolation in variance.
    Gate: median absolute gap between inverted and published implied volatility within
    tolerance, and every discrepancy logged rather than smoothed.

D7  Quality flag layer. Arbitrage sanity, meaning call spread monotonicity and butterfly
    non negativity. Stale wing detection, the T4 metrics: a wing unchanged while ATM moves
    more than 1 point, and risk reversal autocorrelation. Warn days are excluded from
    signals and retained in raw.
    Gate: a deliberately corrupted chain is caught. That fixture lives in tests/.
    T4 trigger: wing unchanged while ATM moves more than 1 point on more than 20 percent
    of days, or risk reversal autocorrelation above 0.99. On trigger, the pre committed
    fallback is 35 delta metrics, a higher open interest floor, a volume above 0
    requirement, and sub strategy 3 demoted to research only.
"""
