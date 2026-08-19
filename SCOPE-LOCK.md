# SCOPE-LOCK.md, commodity-volatility-trading

Locked 18 August 2026. This file is the current authoritative state of this repo's scope
and data sources. Read this before CLAUDE.md's history sections. If this file and an older
CLAUDE.md section disagree, this file is correct and the older section should be treated as
superseded narrative, not reopened.

## Permanently closed, do not re-investigate

| What | Checked | Reason closed | What would reopen it |
|---|---|---|---|
| CME web pages and settlements web service, free automated access | 17 August 2026 | HTTP 403 with a body stating automated retrieval is prohibited by CME's Data Terms of Use. The free FTP settlement site was separately confirmed shut down in 2023. `docs/D1-data-audit.md` sections 1 and 3a | Only if Brian requests, and receives, written permission from CME. Not requested |
| CME DataMine, the Standard purchase | 19 August 2026, final. CME Data Sales, Joaquin Morales, answered every outstanding pricing question | 43 USD 1 time historical extract, full options chain, all strikes and expiries, for the requested date range; approximately 21.50 USD with the 50 percent academic discount. Basic and Basic Plus confirmed settlement only, no per strike implied volatility or delta, no dedicated WTI feed, historical extracts still cost on the free tiers: no free path exists anywhere in CME's tier structure. Brian declines at any price point discussed. `docs/D1-data-audit.md` section 12 | **Only if Brian explicitly raises it again.** Not budget dependent: this is a final decision, not a constraint that lifts if money becomes available. Do not infer a reopening from silence or from the passage of time |
| Euronext, all pages, options and futures alike | 18 August 2026, Track B verification spike, time boxed 1 day, stopped at step 1 | Terms of Use prohibit "spiders, robots, avatars, agents, tools" without prior written permission, and separately prohibit systematic retrieval to build collections or databases, in language structurally identical to CME's. `docs/D1-data-audit.md` section 9 | Only if Brian requests written permission from Euronext's Legal Department, Copyright Agent, the address the terms page itself names. Not requested. Steps 2 to 5 of the spike, robots.txt, reachability, liquidity, the futures leg, were never performed and remain unperformed; do not check them as a way around step 1 |
| EIA STEO `probability_WTI.xlsx` and `probability_HH.xlsx` | 18 August 2026, checked cell by cell with openpyxl | Both are broken S&P Capital IQ plugin templates; every data cell that should carry a futures price, implied volatility, or days to expiration caches as `#N/A`. Cross checked against EIA's full 28 table STEO master workbook, which contains no volatility or probability table at all. `docs/D1-data-audit.md` section 8.2 | Only if EIA republishes a working version of these templates with the Capital IQ values actually resolved. If that happens, it needs independent re-verification, since the current publication pipeline for this specific product is established as unreliable, not merely stale |

## Currently verified and in use

| Source | Covers | License, 1 line | Local or imported |
|---|---|---|---|
| CBOE OVX, series OVXCLS | Implied volatility proxy for WTI, feeding D11 VRP and D12 event study | CBOE copyright, "reprinted with permission" on FRED; personal non-commercial use with citation is established, anything beyond that needs CBOE permission per FRED's own guidance, treated conservatively here | **Project local.** Single consumer |
| EIA daily spot: `wti_cushing`, `henry_hub` | Realized volatility inputs, D8 and D9 | US government, public domain, redistribution with attribution | **Project local.** Originally verified in `adaptive-stat-arb-commodities`'s D1 audit, 17 August 2026; copied here in full, including the 4 business day publication lag rule stated in full, in `docs/D1-data-audit.md` section 8.3, as of 18 August 2026 |
| EIA weekly petroleum, gas storage reports; USDA WASDE schedule | Underlying data for D4 and future event work | US government data, unaffected by the CME or Euronext findings | Not yet formally routed; both are single agency government sources with no chain dependency |

**Instrument caveat, applies to every downstream use of OVX and is not optional context:**
OVX is computed on options on the USO ETF, which holds near term WTI futures. It is not
computed on CME WTI futures options. It is a documented proxy for WTI implied volatility,
not the instrument itself.

## Open, not blocking anything today

| Item | Status | Who resolves it, and how | Blocking date |
|---|---|---|---|
| CL futures, continuous | Unverified. Shared need with the relative value project, neither side verified as of 18 August 2026. See `docs/D1-data-audit.md` section 11 | Whichever project resolves this first, the other should read that project's own D1 note before re-investigating | Not currently blocking; this project's WTI work runs on OVX and EIA spot regardless |
| ZS, soybean futures | Unverified. Shared need with the relative value project's crush basket, its designated near certain anchor. See `docs/D1-data-audit.md` section 11 | Same as above | Not currently blocking; soybean event work has not started |
| ZC, corn futures | Unverified. Single identified consumer, this project, as of 18 August 2026. See `docs/D1-data-audit.md` section 11 | No free daily source has been checked for it | Not currently blocking; WASDE event work has not started |
| A general chain source, any exchange | No candidate identified. CME is permanently closed, both on terms of use and on price, see the Permanently closed table. Euronext is closed on terms of use | An unidentified compliant exchange, elsewhere: CME specifically is not reopening. Or Brian explicitly raising the CME purchase question again, his call, not inferred | **Blocks D5 to D7, D13 to D15 indefinitely, no date attached**, since no candidate source exists to put a date against |

## What this project can currently claim

As of 19 August 2026, this project measures a proxy for WTI implied volatility, CBOE's OVX
computed from options on the USO ETF, not from CME WTI futures options directly, alongside
EIA realized volatility data, and prices everything through `statarb.pricing`. **This is the
project's permanent data foundation, not an interim state pending a future CME purchase.**
Brian declined the CME DataMine Standard purchase permanently on 19 August 2026, at every
price point discussed, a final decision rather than a budget constraint that might lift
later. It does not have, and has no path to, real option chain data from any exchange: CME
is closed on terms of use and on price, permanently, Euronext is closed on terms of use.
This supports realized
volatility and HAR forecasting in full, and supports a proxy version of variance risk
premium harvesting and event volatility work, explicitly distinguished from a backtest
against real quoted markets. It does not support event trading, D13, or skew research and
trading, D14 and D15, which are dropped for a data reason rather than a research finding, a
distinction this project's own documents draw deliberately and any external description of
this project should preserve rather than compress into "it does not work." **Any external
facing description of this project, a README, a CV line, a LinkedIn post, must preserve the
OVX-versus-CME-options distinction explicitly rather than describe this project as trading
or measuring CME WTI options implied volatility.** No backtest has run and no result exists;
this file describes what is buildable, not what has been built.

## Next deliverable

**D4, futures legs, physical data, and the event calendar, due 25 August 2026.** D1, the
audit, and its revision, are delivered. D2, D3, and the CME Data Sales pricing ask are all
sent and answered; the pricing question is closed permanently as of 19 August 2026 and does
not gate D4. D4 proceeds on the sources listed above as currently verified or open; no
collection code has been written for any of them as of this lock.
