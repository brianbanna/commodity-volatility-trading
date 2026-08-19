# D1, data audit note

**Deliverable:** D1, SPEC Part D.
**Date:** 17 August 2026.
**Acceptance gate:** universe locked. Hard floor of 2 PASS markets, WTI plus 1, or the
project halts and escalates.

# **GATE FAILED. 0 PASS markets. THE PROJECT HALTS AND ESCALATES.**

The reason is 1 finding that applies identically to every market in the universe, so it is
stated first and the per market table follows from it.

---

## 1. The determining finding

SPEC deliverable D3 specifies the collection design as scrapes of the CME delayed
settlement pages and the CME option settlement tool, 2x daily. On 17 August 2026 a request
to `cmegroup.com/markets/energy/crude-oil/light-sweet-crude.settlements.html` returned
HTTP 403 with this body:

> This IP address is blocked due to suspected web scraping activity associated with it on
> this CMEgroup.com page. Use of scripts, software, spiders, robots, avatars, agents, tools
> or other scraping mechanisms is strictly prohibited by CME Group's website Data Terms of
> Use. If you are attempting to access data or content from the website via automated means
> or for commercial purposes, CME has numerous other methods to deliver the content you
> require. Please contact CME Group's Global Command Center (GCC) at gcc@cmegroup.com and
> your inquiry will be directed to the appropriate team.

The same 403 was returned by the settlements web service endpoint
(`cmegroup.com/CmeWS/mvc/Settlements/Options/...`).

**This is not a technical obstacle. It is the data owner stating in writing that the access
method the project is designed around is prohibited by its terms of use.** SPEC Part E
already rated these pages PLAUSIBLE FRAGILE under amendment C1, on the expectation that the
fragility was the pages being overwritten daily. The actual position is stronger than
fragile: automated retrieval is not permitted at all.

**A note on 1 thing that was tested and is being rejected rather than used.** Re issuing the
same request with a full set of browser headers returned HTTP 200. That is the scraping
mechanism the terms name, dressed to look like a browser, applied after the operator
returned an explicit block and an explicit prohibition. **It is not recorded here as an
access path and no collection job will be built on it.** Doing so would mean building the
project's foundational infrastructure on deliberate circumvention of a stated restriction
by a named counterparty, and every artifact downstream would inherit that.

## 2. Verdict per market

The retrieval method, the field set, and the free history depth are all downstream of
section 1, so none of them could be verified for any market.

| Market | Options product | Retrieval method verified | Fields verified | Free history depth | Verdict |
|---|---|---|---|---|---|
| WTI crude | LO on CL | **No**, prohibited per section 1 | Not reachable | Not establishable | **CUT** |
| Henry Hub natural gas | LN on NG | **No**, prohibited per section 1 | Not reachable | Not establishable | **CUT** |
| Corn | OZC on ZC | **No**, prohibited per section 1 | Not reachable | Not establishable | **CUT** |
| Soybeans | OZS on ZS | **No**, prohibited per section 1 | Not reachable | Not establishable | **CUT** |
| TTF options | ICE | Not applicable | Not applicable | Not applicable | **DROPPED**, confirmed per amendment C10. Gas volatility was already reassigned to Henry Hub |

**PASS count: 0. Required floor: 2. The gate fails.**

Fields that D5 and D6 require, meaning settlement, implied volatility, open interest, and
volume per strike per expiry, were not confirmed present for any market, because the pages
that would carry them could not be retrieved by permitted means.

## 3. What this does to the project

Every deliverable from D5 onward reads from the collection D3 was to produce.

- **D5 chain builder, D6 surface builder, D7 quality flags**: no input.
- **D8 realized volatility, D9 HAR**: the underlying futures legs are a separate source and
  are affected only through D4, but their purpose is to forecast against an implied level
  that does not exist without chains.
- **D10 hedge simulator, D11 VRP backtest, D12 event study, D13 event trades, D14 to D15
  skew**: all blocked.

**The history clock does not start.** SPEC Part K states the data is the scarce asset in
this project and that every collected day is owned history with no free backfill. Each day
without a permitted collection path is a day permanently absent from every backtest window
this project will ever run. That is the cost of the delay and it does not decrease.

## 3a. There is no free automated CME path. Confirmed, and the search is closed.

CME shut down its free FTP settlement site in 2023 and routed everything through DataMine,
which is paid. Combined with section 1, the position is complete rather than partial:

- the historical bulk route, the free FTP site, no longer exists,
- the remaining route, the web pages and the settlements web service, is prohibited for
  automated retrieval by the Data Terms of Use and is actively blocked.

**No free automated path to CME settlement or option data exists. Do not spend further time
searching for one.** This is recorded so the search is not silently repeated by a later
session reading the CUT verdicts and assuming they were reached for want of looking. They
were not. The verdicts in section 2 stand as written.

## 4. Options, for Brian's decision. None of these is chosen here.

1. **The D2 DataMine request, already sent.** Confirmed sent 17 August 2026 from
   `brian.banna@epfl.ch` to `marketdata@cmegroup.com`, EPFL supervised research framing,
   150 EUR threshold. Given section 3a this is not merely the primary path, it is the only
   licensed route to the specified data. Outcome pending; the lab escalation step stays
   live if the quote lands above threshold.
2. **The GCC clarification ask. SENT AND ANSWERED, case 04698817, 17 August 2026.** Sent
   from `brian.banna@epfl.ch` to `gcc@cmegroup.com`, the address CME's own 403 names.
   CME's answer:

   - **DataMine is the only path.** Stated by the data owner.
   - The block was automated IP scraping detection, which is how section 1 read it.
   - Dataset and pricing questions go to `cmedatasales@cmegroup.com`, not GCC.
   - A student or higher education discount is likely to apply.

   **This independently confirms section 3a.** That section was written on 17 August from
   the shutdown of the free FTP site and the terms of use position, before any reply
   arrived; CME's answer matches it exactly. The finding now rests on both the audit and the
   counterparty's own statement, which is as settled as it gets. **No verdict in section 2
   changes. A confirmation that the door is closed is not an opening.**

3. **The CME Data Sales ask. SENT 17 August 2026, outcome pending.** From
   `brian.banna@epfl.ch` to `cmedatasales@cmegroup.com`, following GCC's redirection,
   referencing case 04698817. Asks specifically about the CME DataMine for Education
   discount against the original 150 EUR budget request. No reply, no quote, nothing
   granted. This is a pricing question about option 1, not a separate route.
4. **Re scope to a market whose options data is free under terms that permit automation.**
   This is a real change to what the project is: SPEC Part A is built on CME commodity
   options specifically, and Part E already records that WRDS OptionMetrics covers equity
   and index options only and is NOT A FIX for CME commodity options.
5. **Re scope to what the free data supports.** The EIA daily spot series verified in
   project 2's D1 note support realized volatility work, D8 and D9, and the underlying leg
   of the event study. They do not support anything involving an implied volatility or a
   surface, which is 3 of the project's 4 ranked goals.

Options 1 to 3 preserve the project as specified and are 1 path, not 3: a licensed DataMine
purchase, with the GCC exchange establishing that it is the only path and the Data Sales
exchange establishing what it costs. Options 4 and 5 change what the project is. That is
why this is an escalation and not a fallback: SPEC Part I has a pre committed fallback for
the scraping breaking or shallowing, and it assumes the scraping path exists. It does not
cover the path being prohibited.

**The decision has not been made.** 2 replies are outstanding, DataMine and Data Sales, and
the halt in CLAUDE.md stands until every open reply is in and Brian has decided. A discount
quote is not a decision.

## 5. What was checked, and what was not

Checked on 17 August 2026, by request: the CME settlements page, the CME settlements web
service endpoint, and the response body of both.

Not checked, because section 1 makes them moot until it resolves: per strike field
availability, the implied volatility cross check target in D6, free history depth per
product, and the option settlement tool's own terms as distinct from the main site's.

Confirmed without needing CME: the TTF options DROP under amendment C10 stands, and the
EIA weekly petroleum, gas storage, Cushing, and utilization series that feed D4 and D14 are
US government data and are unaffected by any of the above.

## 6. Honest negative

SPEC Part H rule 7 requires honest negatives to ship as findings. This note is 1. The
project is not behind because the work was not done; it is halted because the access the
design assumed is not available on the terms assumed. Recording that on the date it was
found, with the source's own words, is the deliverable.

---

## 7. Revision, 18 August 2026: the CME quote, the decision, and the Black 76 reframe

**This section appends the note. Sections 1 to 6 above are unchanged and remain the
record of what was checked between 17 and 18 August 2026. No CME verdict in section 2
moves: still CUT on all 4 markets, still prohibited, still no free automated path.**

### 7.1 CME Data Sales replied. Option 1 is declined, not pending.

CME Data Sales answered the 17 August ask, referencing case 04698817, with pricing:

- Standard End of Market Summary: 43 USD per month per instrument.
- Basic: 426 USD per month per asset class.
- Both carry a 50 percent academic discount.

**Decision: declined.** Brian has zero budget for this project. Any nonzero price fails
that constraint regardless of the discount. This closes option 1 in section 4 above on
budget, not on price or on access. The DataMine route, which section 3a and the GCC reply
in section 7 of CLAUDE.md already established as the only compliant path to CME options
data, is now fully closed: not unavailable, not unauthorized, simply unaffordable.

### 7.2 The Black 76 reframe, and why it reopens the universe question

The original D1 audit, sections 1 to 6, searched for free **implied volatility**. That was
too narrow a search. The project does not need published implied volatility directly. It
needs 2 more primitive things: option settlement prices per strike per expiry, and the
underlying futures price. Black 76 recovers implied volatility from those, and
`statarb.pricing.black76` already performs exactly that inversion, per the shared engine's
D11 deliverable. Free settlement price data is materially more available than free implied
volatility data, because implied volatility is a derived, licensed analytic product in most
commercial distributions while raw settlement prices are sometimes published as a byproduct
of exchange operations under looser terms.

This does not change the CME verdict. CME's Data Terms of Use prohibit automated retrieval
of BOTH the settlement prices and the published implied volatilities, from the same pages,
under the same prohibition. The reframe does not open a door at CME. It opens the question
of whether some OTHER exchange publishes settlement prices under different terms, which is
Track B, section 9 below.

It also reopens a narrower question this audit had closed prematurely: sources that publish
**volatility indices or vol adjacent products directly**, rather than a strike chain, which
do not need the reframe at all. That is Track A, section 8 below.

## 8. The revised universe, Track A. Committed, does not wait on Track B.

Every verdict below is from an actual request or an actual reading of a terms and license
page, issued 18 August 2026, recorded with what was checked. Nothing inferred from
documentation or from memory.

### 8.1 CBOE OVX via FRED, series OVXCLS. VERIFIED, with 2 stated caveats.

Retrieved `fred.stlouisfed.org/graph/fredgraph.csv?id=OVXCLS` directly, no API key, no
account. **5028 daily observations, 2007-05-10 to 2026-08-17.** The retrieval itself was
intermittently rate limited by Akamai bot mitigation on this network, clearing after 10 to
15 seconds; this is a network characteristic, not a terms restriction, and is unlike the
CME finding in kind.

**Citation, captured verbatim from the FRED series page**, to be reproduced exactly
wherever OVX or anything derived from it is shown:

> Chicago Board Options Exchange, CBOE Crude Oil ETF Volatility Index [OVXCLS], retrieved
> from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/OVXCLS,
> [retrieval date].

The series page's copyright note reads: "Copyright, 2016, Chicago Board Options Exchange,
Inc. Reprinted with permission," and separately: "Data in this graph are copyrighted.
Please review the copyright information in the series notes before sharing."

**A correction to the premise this task was framed with.** The premise stated that FRED
permits publishing derived statistics from a copyrighted series with attribution. FRED's
own general guidance on copyrighted series, which is more restrictive than that premise:
redistributing a copyrighted series is permitted for personal, non-commercial use with
citation; sharing it, or material derived from it, for anything beyond personal
non-commercial use requires permission from the original data provider, which here is
CBOE, not FRED. **Attribution alone is not established as sufficient for a public
research repository; permission from CBOE is the stricter and more literal reading.**
This project proceeds on the conservative interpretation until clarified: OVX levels feed
internal backtest computation freely, with the citation attached to any note or figure
that shows OVX values or values computed from them, and no bulk republication of the raw
OVXCLS series itself happens anywhere in this repo. If a stricter position is needed later,
that is a design decision for Brian, not a default this note assumes away.

**Instrument caveat, stated honestly and carried into every downstream use of OVX:** OVX
is computed on options on the USO ETF, which holds near term WTI futures. **It is not
computed on CME WTI futures options.** It is a documented proxy for WTI implied volatility,
not the instrument itself, and every output built on it, every VRP signal and every P&L
decomposition, states that plainly rather than presenting OVX as CME implied volatility
under another name.

**Source routing: FRED, not cboe.com.** This follows the instruction as given; it was not
independently re-derived by comparing cboe.com's terms against FRED's in this session.

### 8.2 EIA STEO implied volatility and probability files. CHECKED. NOT USABLE.

The Short Term Energy Outlook links to exactly 2 files matching this description, found on
the crude oil and natural gas report pages respectively:

- `eia.gov/outlooks/steo/xls/probability_WTI.xlsx`
- `eia.gov/outlooks/steo/xls/probability_HH.xlsx`

Both downloaded successfully, free, no key, no account: US government data. Both opened
and inspected cell by cell with `openpyxl`, formulas included.

**Finding: both files are broken as public data products.** They are S&P Capital IQ
Excel plugin templates. The header row states "Average NYMEX Data for Aug 28 - Sep 4" and
the workbook defines named ranges belonging to the Capital IQ add in (`IQ_CH`, `IQ_CQ`,
`IQ_TODAY`, and others). Every data cell that should carry the futures price, the implied
volatility, and the days to expiration for every contract month resolves to a **cached
`#N/A` error**, because those cells were originally populated by the Capital IQ plugin
against a live terminal connection and EIA published the workbook without that connection
resolved. The probability formulas in the remaining columns are ordinary Black-Scholes
probability calculations, correctly written, but they compute against inputs that are all
errors, so every output cell is also `#N/A`.

This is not a formatting inconvenience. There is no cached historical series anywhere in
either file: the contract month rows run from January 2025 forward with no populated row
at all, meaning the template was never refreshed with a live pull before EIA re-published
it as the current download.

**Cross checked against the STEO master data workbook**, `steo/xls/STEO_m.xlsx`, which
contains every one of the 28 official STEO data tables, tables 1 through 10b. None of them
is a volatility or probability table. The only other artifacts EIA publishes on this topic
are PDF chart archives of the WTI 95 percent confidence interval band, back to 2009, which
are images, not machine readable data, and a 2009 methodology PDF describing the
methodology these broken templates were meant to implement.

**Verdict: UNVERIFIED, NOT USABLE.** This is a genuine, checked negative, not an
unretrieved source. Do not attempt to parse these files programmatically; there is nothing
in them to parse. Do not treat the archived PDF confidence interval charts as a data
source; they are not machine readable. If EIA ever republishes a working version of these
templates with live Capital IQ values resolved, that would need to be independently
re-verified before use, because the current files establish that EIA's own publication
pipeline for this specific product is unreliable.

### 8.3 EIA price series for realized volatility. Already PASS, per project 2's D1.

Originally verified in `adaptive-stat-arb-commodities/docs/D1-data-audit.md` section 1, on
17 August 2026, and not re-verified here; that would duplicate a check. Retrieved over
plain HTTPS, no API key, no account, no browser challenge, US government data, public
domain, redistribution permitted with attribution:

| Series | Endpoint | Rows | Range observed |
|---|---|---|---|
| WTI Cushing spot | `eia.gov/dnav/pet/hist_xls/RWTCd.xls` | 10221 | 1986-01-02 to 2026-08-11 |
| Henry Hub spot | `eia.gov/dnav/ng/hist_xls/RNGWHHDd.xls` | 7431 | 1997-01-07 to 2026-08-11 |

This project uses `wti_cushing` and `henry_hub` specifically, for its realized volatility
work. The other 3 series project 2 verified, Brent Europe, NY Harbor gasoline, and NY
Harbor No 2 heating oil, feed that project's crack and Brent WTI baskets and have no use
here.

**The 4 business day publication lag applies here exactly as recorded there, stated in
full, with no weakening.** All 5 series were observed ending 2026-08-11 when queried on
2026-08-17. These are a history and realized volatility input, never a live daily source.
A backtest treating an EIA spot print as available on its observation date is lookahead
that voids the run. Project 3's realized volatility library, D8, and its HAR forecast, D9,
apply this lag rule as stated here, not a weaker or re-derived version of it.

**This finding was briefly shared through `commodity-data-platform`, retired 18 August
2026.** Each project now owns its own ingestion. This project holds its own copy of the
verification above rather than importing it; the original verification remains project
2's, reached independently on 17 August 2026, and this project's copy is not a
re-verification, only a record that the same finding is now owned in 2 places rather than
imported from a third.

## 9. Track B, the Euronext verification spike. Time boxed to 1 day. FAILED at step 1.

Checked 18 August 2026, in the order the task specified: terms first, then robots.txt,
then reachability, then liquidity, then the futures leg. **The spike stopped at step 1,
per instruction: if any step fails, stop and record the failure, do not work around a
prohibition.**

### 9.1 Step 1, terms of use. PROHIBITED.

Retrieved `euronext.com/en/terms-use` directly, 409719 bytes, read in full. 2 clauses
determine the outcome, quoted verbatim:

> Except if we give you prior written permission, use of any Web browsers (other than
> generally available third-party browsers), engines, software, spiders, robots, avatars,
> agents, tools or other devices or mechanisms to navigate, search or determine the
> Euronext Website is strictly prohibited.

And, on reproduction and derivative works:

> ...you will not sell, license, rent, modify, print, copy, reproduce, download, upload,
> transmit, distribute, disseminate, publicly display, publicly perform, publish, edit,
> adapt, compile or create derivative works from any Content or materials (including,
> without limitation, through framing or systematic retrieval to create collections,
> compilations, databases or directories)...

A narrower personal use allowance exists, quoted for completeness: "You may print or
download a single, unaltered, permanent copy or one temporary copy in a single computer's
memory of any Content for your personal, non-commercial use only," and a classroom
distribution allowance for educational institutions. **Neither allowance covers automated,
scheduled, systematic retrieval feeding a research pipeline.** The prohibition on
"spiders, robots... tools or other devices or mechanisms" requires prior written
permission with no exception for research or education, and the reproduction clause
separately and independently prohibits exactly what a collection job would do: systematic
retrieval to build a database.

**This is structurally identical to the CME finding in section 1.** Same category of
prohibition, same absence of a research carve out, same remedy, which is to request
written permission rather than to route around the block.

### 9.2 Steps 2 through 5. NOT PERFORMED.

Per the task's explicit instruction, a failure at step 1 stops the spike. **robots.txt on
live.euronext.com was not checked. Settlement price reachability, bulk versus current day
display, and history depth were not checked. Open interest and volume per strike for a
recent expiry were not checked, so liquidity is not established either way. The rapeseed,
milling wheat, and corn futures legs were not checked.** None of these absences should be
read as a finding; they are simply not performed, consistent with not working around a
documented prohibition to gather information the prohibition already rules out using.

### 9.3 Verdict

**Euronext options (OBM, OMA, OCO) and Euronext futures (rapeseed, milling wheat, corn):
CUT, on Terms of Use grounds, without a liquidity or reachability finding either way.**
This is a clean negative and a valid outcome, recorded per instruction. It closes both
the chain and skew question for this project and the crush question flagged for the
relative value project in that project's own D1 note; see section 5 there.

If this verdict is ever revisited, it starts at requesting written permission from
Euronext's Legal Department, Copyright Agent, the address and email the terms page itself
names, not at re-checking robots.txt or attempting retrieval under different headers.

## 10. Revised project 3 scope, 18 August 2026

**Track A is committed. It does not wait on Track B, and Track B's failure does not
change what Track A supports.**

### 10.1 What Track A alone supports

| Ranked goal | Supported | Basis |
|---|---|---|
| 1. Collection infrastructure | Partial | The scarce asset framing in Part B assumed CME chains. What survives is EIA realized vol inputs, ingested here project locally as of 18 August 2026, and OVX, also project local |
| VRP, the variance risk premium | Yes, as a proxy | OVX in place of CME WTI implied volatility, HAR forecast against EIA realized vol. The straddle structure in D11 as literally specified needs a strike chain to enter and exit against real settlement prices; without one, this is a level based proxy strategy priced through `statarb.pricing`, not a backtest against quoted CME markets. That distinction is stated in the eventual note, not elided |
| Event study, D12 | Yes, modified | The spec's literal method prices the move from the shortest spanning straddle, which needs a chain. Without one, the priced move is read from OVX around the release instead. This is a substitution, recorded as one, not the spec's original method under the same name |
| Realized volatility and HAR, D8 D9 | Yes | Runs entirely on the EIA series, unaffected by the chain question |
| The P&L decomposition, D10 | Yes, as a proxy | Greeks and values come from `statarb.pricing` fed by OVX and the EIA futures proxy; it demonstrates the decomposition mechanics, not a reconciliation against real market hedge fills |
| Event trading, skew, D13 to D15 | **No** | All need a strike chain. Not supported by Track A |

**3 of the 4 ranked goals in SPEC Part B are supported, in modified or proxy form, and
goal 4, the skew layer contingent on D14 research, is not reachable at all.** This is
stated for the README, plainly, so a reader understands why the project covers 3 goals
rather than 4 without discovering it from an absence.

### 10.2 What Track B would have added, and why it does not

Full chain work, D5 to D7, the surface, D6, and the skew layer, D14 to D15, all require a
strike chain with open interest and volume, which only a chain source provides. Euronext
was the candidate. **It failed at the terms check.** No other chain source has been
identified. Goals 5 (VRP as literally specified) and 6 (skew) remain out of reach absent a
new, unidentified, compliant chain source or a future licensed purchase Brian chooses to
fund.

### 10.3 D15 is dropped, and this is the spec's own design, not a new failure

D15, the skew trade layer, was always conditional on D14's 3 research layers supporting it,
per SPEC Part H rule 9 and Part K's research first rule: no trade layer without research
support, and the research note shipping alone is success, not failure. **D14 itself cannot
run without a chain**, so the conditional logic resolves at 1 step earlier than the spec
anticipated: instead of D14 running and finding no support, D14 cannot run at all, for a
data reason rather than a research finding. The outcome is the same shape the spec already
designed for: no trade layer, a research gap recorded honestly, no strategy shipped without
support. This is recorded as dropped for data reasons, not as a research negative, because
those are 2 different findings and conflating them would misrepresent which one occurred.

---

## 11. Findings inherited from the now retired shared platform repo, 18 August 2026

`commodity-data-platform` was retired 18 August 2026: each project now owns its own data
ingestion rather than sharing a collection layer. The EIA daily spot finding is already
made self contained in section 8.3 above. What remains is the platform repo's gap tracking
relevant to this project, carried forward here rather than lost. No new source was checked
to write this section.

- **`cl_futures`.** Continuous CL futures were not verified for either this project or the
  relative value project as of 18 August 2026. This project's WTI volatility work and that
  project's crack and Brent WTI baskets need the same contract. Whichever project resolves
  this first, the other should read that project's own D1 note
  (`adaptive-stat-arb-commodities/docs/D1-data-audit.md`) before attempting an independent
  check, so the search is not run twice.
- **`soybean_complex`, ZS specifically.** No free daily source found. ZS is a needed
  underlying for this project's soybean event and volatility work, and also for the
  relative value project's crush basket, its designated near certain anchor. Both projects
  are blocked on the same gap as of 18 August 2026.
- **`zc_corn`.** No free daily source has been checked for this. As of 18 August 2026 this
  is a single consumer need, this project only, for WASDE event work: the relative value
  spec's basket universe does not include a corn leg.

None of these gaps were resolved by the platform repo's retirement; they were unresolved
before and remain unresolved after, now tracked in this project's own note rather than in a
shared config file.
