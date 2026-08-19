# Commodity volatility trading

Trading how much prices move, 3 ways, as 1 book.

## The sentence this project is built to support

> I trade commodity volatility 3 ways: systematic risk premium harvesting with daily delta
> hedging, event volatility around EIA and WASDE prints, and skew against physical
> inventory data, all running on the same pricing engine as my relative value book.

That sentence is the target, not a current claim, and as of 18 August 2026 it is not fully
reachable. **The data constraint below changes what this project can claim; read it before
reading anything else here.**

## Status

**In progress. The data plan changed on 18 August 2026.** D1, the data audit, found the CME
options market this project was designed around inaccessible on any free or affordable
basis. A revised plan, Track A, was verified the same day and covers realized volatility,
variance risk premium harvesting, and event volatility as proxy or modified strategies, on
different underlyings than originally specified. A parallel check, Track B, tried to
recover full chain access through Euronext and found it equally closed. No data has been
collected and no result exists; this is a data plan decision, not a backtest result.

**The data constraint, stated plainly.** This project covers 3 of its 4 ranked goals, not
4, because the fourth, skew against physical tightness, needs a strike chain with open
interest and volume per strike, and no compliant source for that exists. CME's Data Terms
of Use prohibit automated retrieval and the paid DataMine alternative was declined on
budget. Euronext's Terms of Use, checked as an alternative, prohibit the same thing in
materially the same words. Full detail, including the exact clauses read from each
exchange's own terms page, is in `docs/D1-data-audit.md`.

What this means concretely: the volatility risk premium and event volatility strategies run
on CBOE's OVX index, sourced via FRED, as a documented proxy for WTI implied volatility,
rather than against real CME option settlement prices. OVX is computed from options on the
USO ETF, not from CME WTI futures options, and every figure built on it says so. The skew
layer, D14 and D15, is dropped entirely: not because the research did not support a trade,
which is the outcome the spec's own research first rule anticipated, but because the
research could not run at all for lack of a chain to run it on. Those are 2 different
findings and this project does not present 1 as the other.

Definition of done, revised from SPEC Part J to match what is currently reachable:

- Minimum viable: D1 to D12 in modified form, meaning realized volatility and the HAR
  forecast on real EIA data, the variance risk premium and event volatility strategies on
  the OVX proxy, and the P&L decomposition through `statarb.pricing` demonstrating the
  mechanics rather than reconciling against real market hedge fills.
- D5 to D7, D13 to D15 are out of scope on current data. D16 and D17, the full book run and
  the site update, proceed on whatever of D1 to D12 is actually built, with the scope
  limitation stated in the book note rather than left for a reader to discover.

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

This was true of the CME chain data this project was originally designed around and it
remains true structurally, even though that specific data is now out of reach. The CME
delayed settlement pages carry the top day only and are overwritten, there is no free
backfill for them, and there never was: CME's Data Terms of Use prohibit automated
retrieval outright, and the paid DataMine route was checked, priced, and declined on
budget on 18 August 2026. Euronext, checked the same day as a possible alternative, is
prohibited on the same grounds.

For the data this project does use, the discipline is unchanged. Collection outranks every
other task in this repo, a manifest gap is the highest priority incident, and `data/raw/`
is immutable: a fix regenerates processed data from raw and never edits raw. The EIA daily
spot series this project draws on was originally verified in the relative value project's
own D1 audit and is now held here as this project's own copy of that finding, including
the 4 business day publication lag rule stated in full, in `docs/D1-data-audit.md` section
8.3.

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

**As specified in SPEC Part E**, and now superseded in part: CME delayed settlement pages
and the CME option settlement tool for daily chains and implied volatilities, free futures
aggregators for the underlying legs, EIA for petroleum and gas storage and Cushing and
utilization, USDA for the WASDE schedule and stocks to use, AGSI+ for EU storage context.
Settlement tables are never republished in any artifact.

**As actually verified, 18 August 2026**: CBOE's OVX crude oil implied volatility index,
sourced via FRED series OVXCLS with attribution to both CBOE and FRED, project local to
this repo; EIA daily petroleum and natural gas spot data, originally verified in the
relative value project's D1 audit and held here as this project's own copy of that
finding; EIA weekly petroleum and gas storage reports and USDA's WASDE schedule, both
government data unaffected by the CME or Euronext findings. CME chain data and Euronext
chain and futures data are both prohibited under their respective terms of use; see
`docs/D1-data-audit.md` for the full record with verbatim clauses.

## License

Research code. Not investment advice. No result here is a claim about the conduct of any
market participant.
