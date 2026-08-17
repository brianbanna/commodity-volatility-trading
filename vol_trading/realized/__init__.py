"""Realized volatility and its forecast. SPEC Part D deliverables D8 and D9.

D8  Realized volatility library. Close to close at 10, 21, and 63 days, annualized.
    Parkinson and Garman Klass where OHLC exists. The event day split is first class:
    an ex event series and an event only series, both maintained, because which series
    feeds which sub strategy is a design decision and not a preference. The volatility
    risk premium trades against ex event realized; the event study trades against event
    only realized.
    Gate: the estimators agree within their expected relationships on test data.

D9  HAR forecast. Daily, weekly, and monthly realized components regressed on the next 21
    day ex event realized. GARCH(1,1) and a 21 day naive forecast run alongside as the
    honest comparison, not as decoration. Out of sample RMSE and Mincer Zarnowitz per
    market.
    Gate: evaluation on the training window only, and the freeze documented. The winner is
    frozen thereafter and does not get revisited because a later result would look better.
"""
