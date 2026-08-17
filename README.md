# Commodity volatility trading

Trading how much prices move, 3 ways, as 1 book.

## The sentence this project is built to support

> I trade commodity volatility 3 ways: systematic risk premium harvesting with daily delta
> hedging, event volatility around EIA and WASDE prints, and skew against physical
> inventory data, all running on the same pricing engine as my relative value book.

That sentence is the target, not a current claim. Nothing in it is quotable with numbers
until the artifact behind it passes its acceptance gate.

## Status

**In progress. Build starts 17 August 2026** with D1, the data audit note, and D2, the
DataMine academic email, followed by D3, the daily collection jobs, on 18 August. As of 17
August 2026 the repo holds the skeleton, the calendar scaffold, and the specification. No
data has been collected and no result exists.

Definition of done, from SPEC Part J:

- Minimum viable, June 2027: D1 to D12, collection running since August, surfaces built,
  realized volatility and the HAR forecast evaluated, the hedge simulator with its
  decomposition verified, the volatility risk premium backtest with its stated window, and
  the standalone event study.
- Full, August 2027: D13 to D17.

## The shared pricing engine is a hard dependency

Every option value, every implied volatility inversion, and every Greek in this project
comes from `statarb.pricing`, the engine built in the relative value project
(`adaptive-stat-arb-commodities`). That engine's API freezes on **20 December 2026**, and
from that date this project imports it at a pinned tag with its harness green.

**This project never reimplements and never forks that engine.** If a payoff or a Greek is
missing, the path is an additive pull request to the engine package, the harness green on
that change, a tag bump, and a deliberate repin here. Copying the maths into this repo is a
refusal point, not a judgment call. See [CLAUDE.md](CLAUDE.md).

Until the freeze there is nothing to pin, which is why the dependency sits as a comment in
`pyproject.toml` rather than as a version range that would resolve to something
unintended.

## The data is the scarce asset

There is no free backfill for the settlement data this project runs on. The CME delayed
settlement pages carry the top day only and are overwritten, so every collected day is
owned history and a missed day is permanently missing. Collection outranks every other
task in this repo. A manifest gap is the highest priority incident here.

That is also why `data/raw/` is immutable: a fix regenerates processed data from raw and
never edits raw.

## Layout

```
vol_trading/
  collection/  D3 settlement and option tool scrapes, D4 futures, physical, calendar
  chains/      D5 chain builder, D6 surface builder, D7 quality flags
  realized/    D8 realized volatility library, D9 HAR forecast
  hedge_sim/   D10 hedge simulator and the P&L decomposition
  vrp/         D11 volatility risk premium backtest
  events/      D12 event study, D13 event trading backtest
  skew/        D14 skew research, D15 conditional trade layer
  book/        D16 full book run, D17 site update
config/
  event_calendar.yaml   release timestamps in UTC, the only place daylight saving lives
tests/
data/raw/        collected data, gitignored, immutable, the record
data/processed/  regenerated from raw, gitignored, disposable
```

## Build authority

[SPEC.md](SPEC.md) governs this repo: goals, the deliverables table with dates and
acceptance gates, the phase plan, the methods core, the hard rules, the risks with their
pre committed fallbacks, and the definition of done. Read it before writing code.
[CLAUDE.md](CLAUDE.md) is the operating brief for an agent session opened here.

## Data sources

CME delayed settlement pages and the CME option settlement tool for daily chains and
implied volatilities, free futures aggregators for the underlying legs, EIA for petroleum
and gas storage and Cushing and utilization, USDA for the WASDE schedule and stocks to
use, AGSI+ for EU storage context. Full register with verdicts in SPEC Part E. Settlement
tables are never republished in any artifact.

## License

Research code. Not investment advice. No result here is a claim about the conduct of any
market participant.
