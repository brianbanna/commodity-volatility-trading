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
