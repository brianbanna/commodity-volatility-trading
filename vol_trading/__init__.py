"""Commodity volatility trading: risk premium, event volatility, skew against tightness.

SPEC.md at the repo root is the build authority. Read it before writing code.

Subpackage map, keyed to the SPEC Part D deliverable table:

    collection  D3 daily settlement and option tool scrapes, D4 futures, physical, calendar
    chains      D5 chain builder, D6 surface builder, D7 quality flag layer
    realized    D8 realized volatility library, D9 HAR forecast and comparisons
    hedge_sim   D10 hedge simulator and the P&L decomposition
    vrp         D11 volatility risk premium backtest
    events      D12 the event study, D13 event trading backtest
    skew        D14 skew research in 3 layers, D15 the conditional trade layer
    book        D16 the full book run, D17 site update

All option maths comes from `statarb.pricing`, the engine frozen 20 December 2026 in the
relative value project. It is imported at a pinned tag, never reimplemented, never forked.

The data is the scarce asset in this project. There is no free backfill for the
settlement data, so every collected day is owned history and a manifest gap is the highest
priority incident here.
"""

__version__ = "0.0.0"
