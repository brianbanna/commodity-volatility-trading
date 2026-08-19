# CLAUDE.md, commodity volatility trading

You are in a public repo. Read this file completely before your first tool call, then read
`SPEC.md`. If you are about to write code and you have not read `SPEC.md`, stop and read it.

Read `SCOPE-LOCK.md` next, before anything else in this file. It is the current state;
sections below are history that led to it.

---

## 1. SPEC.md is the build authority

`SPEC.md` at the repo root is the full standalone specification for this project. It
carries Part A the plain words, Part B the ranked goals, Part C worked data scenarios,
Part D the deliverables table with IDs and dates and acceptance gates, Part E the data
register, Part F the phase by phase plan, Part G the methods core with the actual
parameters, Part H the hard rules, Part I the risks with pre committed fallbacks, Part J
the definition of done, Part K executor notes.

Nothing outside `SPEC.md` is required to execute this project. When this file and
`SPEC.md` disagree on a fact, `SPEC.md` wins and this file is wrong and should be fixed.
When they disagree on a prohibition, the stricter reading wins.

`SPEC.md` is reproduced from the master document with 1 token level redaction, marked in a
comment at the top of the file, required by its own Part H rule 1. Nothing else is altered.

## 2. Where the build stands, and what is next

**Today the repo is at Phase 0, per SPEC Part F.** Phase 0 is the week of 11 to 17 August
2026 and it is the only August work beyond collection. As of 17 August 2026 the repo holds
the skeleton, the calendar scaffold, and the spec. No data collected, no result produced.

**The next deliverables, in order:**

- **D1, the data audit note. DELIVERED 17 August 2026. `docs/D1-data-audit.md`.**
  **THE GATE FAILED: 0 PASS markets against a floor of 2. THE PROJECT IS HALTED AND
  ESCALATED TO BRIAN.** WTI, Henry Hub, corn, and soybeans are all CUT for the same reason:
  CME's Data Terms of Use prohibit automated retrieval of the settlement pages and the
  settlements web service, and the request returns an explicit block saying so. TTF options
  DROPPED, confirmed per amendment C10.
  **Read that note before doing anything else in this repo.** Do not start a downstream
  deliverable, do not build a collection job, and do not treat the failure as a fallback
  case: SPEC Part I covers the scraping breaking or shallowing, and it assumes the path
  exists. It does not cover the path being prohibited. The decision on how to proceed is
  Brian's and has not been made.
- **D2, the DataMine academic email. SENT.** Confirmed sent from `brian.banna@epfl.ch` to
  `marketdata@cmegroup.com`, recorded 17 August 2026, spec target date 12 August 2026.
  Historical options end of day, EPFL supervised research framing, 150 EUR threshold.
  **Outcome pending: no reply, no quote, nothing granted.** Do not record any outcome until
  an actual reply arrives. The lab escalation path stays live if the quote lands above
  threshold. D1 has promoted this from a history upgrade to the project's primary data
  path; see below.
- **The GCC clarification email. SENT, AND ANSWERED. Case 04698817, 17 August 2026.**
  Sent from `brian.banna@epfl.ch` to `gcc@cmegroup.com`, referencing the block encountered
  during D1 and the already sent DataMine request. **This was a clarification ask, not a
  data path, and the answer does not make it one.** What CME said:
    1. **DataMine is the only path.** Confirmed by the data owner directly.
    2. The block was automated IP scraping detection, as D1 read it.
    3. Dataset and pricing questions go to `cmedatasales@cmegroup.com`, not to GCC.
    4. A student or higher education discount is likely to apply.

  **This confirms section 3a of the D1 audit from the counterparty's own mouth: there is no
  compliant automated alternative.** The audit reached that independently on 17 August and
  CME's answer matches it exactly. Nothing in the D1 verdicts changes: still 0 PASS markets,
  still CUT on all 4, still halted. A confirmation that the door is closed is not an opening.

- **The CME Data Sales email. SENT.** Sent from `brian.banna@epfl.ch` to
  `cmedatasales@cmegroup.com`, recorded 17 August 2026, following GCC's redirection.
  References case 04698817 and asks specifically about the CME DataMine for Education
  discount against the original 150 EUR budget request. **Outcome pending: no reply, no
  quote, nothing granted.** Do not record any outcome until an actual reply arrives.
- **D3, the daily collection jobs. BLOCKED, not started.** The design is scrapes of the
  settlement pages AND the option settlement tool, 2x daily. **D1 established on 17 August
  2026 that CME's Data Terms of Use prohibit automated retrieval, and the request returns
  an explicit block. Do not build this job, and do not work around the block.** Read
  `docs/D1-data-audit.md` in full before touching anything in `vol_trading/collection/`.

  **THE HALT CONDITION, in force as of 17 August 2026: write no project 3 collection code
  until either the DataMine reply or the GCC reply arrives AND Brian has decided how to
  proceed. Both conditions, not either.** A reply on its own does not release the halt. If
  you are asked to start collection work and neither has happened, say so and stop.

  **THE HALT IS NOT LIFTED. Status of the 2 conditions:**

  | Condition | Status |
  |---|---|
  | 1. A reply arrives | **SATISFIED.** The GCC reply, case 04698817, arrived 17 August 2026 |
  | 2. Brian has decided how to proceed | **OPEN. Not made.** |

  Condition 1 being satisfied changes nothing on its own; that is what the sentence above
  means by both conditions and not either. **Brian's standing instruction, recorded here
  verbatim so it is not paraphrased away: no collection code, no matter what these replies
  say, until every open reply is in and he has made the actual decision on how project 3
  proceeds.** A favorable reply is not a decision, a discount quote is not a decision, and
  neither is an instruction to start work that does not reference the decision having been
  made.

  **18 August 2026: CONDITION 2 IS NOW SATISFIED. The decision has been made.**

  | Condition | Status |
  |---|---|
  | 1. A reply arrives | SATISFIED, 17 August 2026 |
  | 2. Brian has decided how to proceed | **SATISFIED, 18 August 2026** |

  CME Data Sales replied with pricing: 43 USD per instrument per month standard, 426 USD
  per asset class per month basic, 50 percent academic discount both. **Decision: declined,
  on zero budget.** This closes the CME route entirely, not just the free automated one:
  not unavailable, not unauthorized, unaffordable. See `docs/D1-data-audit.md` section 7.

  **The decision that replaces the halted CME route is Track A**, verified 18 August 2026:
  CBOE OVX via FRED as a documented proxy for WTI implied volatility, the EIA daily spot
  series already verified for the relative value project and now shared through
  `commodity-data-platform`, and `statarb.pricing` for every option value and Greek, same
  as always. **Track B, a Euronext verification spike for a possible chain source, was
  checked the same day and failed at the terms of use step**, on a prohibition
  structurally identical to CME's. See `docs/D1-data-audit.md` sections 7 through 10 for
  the full record, and section 10 specifically for what Track A does and does not support:
  3 of the 4 ranked goals, in proxy or modified form, none of the chain dependent work.

  **What this does NOT do: it does not authorize collection code in this session.** The
  session that made this decision was scoped to verification, routing, and scope only, and
  no ingestion job for OVX or anything else was written under it. The halt as originally
  written, no collection code until the reply and the decision both land, is satisfied. A
  future session building the OVX ingest job or wiring the platform import should read this
  entry and `docs/D1-data-audit.md` sections 7 to 10 as its starting brief, not treat
  D1 to D3 above as still open questions: they are answered, and what remains is
  implementation, not decision.

  **The CME and Euronext prohibitions are permanent findings, not part of what got
  decided.** No future session reopens either search. Both are recorded identically in
  `commodity-data-platform/config/sources.yaml` under `rejected`, so this is not the only
  place that record lives.

  **Do not spend time searching for a free automated CME path. There is not one.** See
  section 6 of the D1 note. When a permitted path exists, the original gate applies: raw
  files immutable and checksummed, 7 consecutive clean days per market. Until then the
  history clock has not started, and every day that passes is permanently absent from every
  backtest window this project will ever run.
- **D4, futures legs, physical data, and the event calendar. Due 25 August 2026.**

Then Phase 1, 25 August 2026 to 8 January 2027, is dormancy by design. Collection runs
itself and the weekly platform exceptions check, 15 minutes, is the only touch. Phase 2,
9 January to 6 February 2027, is the frozen window: nothing. Do not start work in either
window. The build resumes in February 2027 with D5 and D6.

## 3. Hard rules. SPEC Part H, restated in full

These are not guidelines and they are not summarized here. Apply them mechanically.

1. **Zero content from the prior employer, ever.** The employer is named in the master
   specification and is deliberately not named anywhere in this repo, which is why you will
   not find the name here or in `SPEC.md`. Nothing sourced from that employment enters this
   project in any form: no data, no document, no figure, no recollected number, no
   paraphrase. Where provenance is unclear, it is excluded and the exclusion is flagged,
   not resolved by guessing.

2. **`statarb.pricing` is imported, never reimplemented, never forked.** All option maths
   and every Greek comes from the engine frozen 20 December 2026 in the relative value
   project, imported at a pinned tag. Gaps become additive pull requests to that package
   with the harness green, a tag bump, and a deliberate repin here. Not a local copy, not a
   vendored file, not a quick private version to unblock something.

3. **Raw settlement files are immutable. Fixes regenerate processed data from raw and
   never edit raw.** Raw is checksummed and it is the record. Settlement tables are never
   republished anywhere, in any artifact, public or private.

4. **Point in time vintages.** WASDE and EIA figures as published on the day. Revised
   history is lookahead and is refused. Not adjusted for, not caveated, refused.

5. **The test set runs once.** A rerun request is flagged, requires explicit confirmation,
   and every execution is logged.

6. **Event timestamps are UTC internally.** `config/event_calendar.yaml` is the single
   source of truth and daylight saving lives there and nowhere else. No module computes a
   release timestamp, applies an offset, or hardcodes a session boundary.

7. **Honest negatives ship.** An unharvestable volatility risk premium, unsupported skew
   trading, a thin window: all of these ship as findings. The window honesty sentence
   appears verbatim in every backtest note, written before the results are looked at.

8. **WRDS: futures history block only**, academic use, never republished, never a daily
   dependency. Splice dates recorded in the manifest.

9. **Style: numerals, no hyphens in prose, no marketing language, no emojis, no conduct
   language about any market participant.** Expanded in section 4 below.

Additional standing constraints from Part K, which have the same force:

- The data is the scarce asset. Protect the collection jobs above everything else in this
  project, including analysis with a nearer deadline. Treat a manifest gap as the highest
  priority incident.
- The research first rule on skew is binding. See section 6.

## 4. Style

- Numerals, not words, for numbers. Write 3, not three.
- No hyphens in prose. Code, CLI flags, file names, and kebab case identifiers keep the
  hyphens they syntactically need.
- No emojis. Anywhere, including commit messages.
- No marketing language. Banned outright: leverage, comprehensive, robust, seamless,
  holistic, streamline, supercharge, unlock, journey, paradigm, best in class, dive in,
  delve.
- No conduct language about any market participant.
- Lead with the result. Limitations are a first class section, written before the results
  section, not appended to it.

## 5. The 3 refusal points

If a task asks for 1 of these, stop and ask the user. Do not proceed, do not find a
workaround, do not do it and mention it afterward. Say which refusal point was hit and
what confirmation you need.

1. **Reimplementing or forking a shared component instead of importing it.** This is Part
   H rule 2 and it is the single most likely thing to go wrong in this repo, because a
   missing Greek during a Saturday afternoon of work looks like a 20 line fix. It is not. A
   local Black 76, a local delta, a copied Margrabe, a vendored `pricing.py`: all refusals.
   The path is an additive pull request to the engine package.

2. **Using revised or lookahead data vintages.** EIA and USDA figures as published on the
   day. A revised inventory series in the skew research, or a restated storage number in
   the event study, is lookahead. Refuse it; do not caveat it.

3. **Rerunning a locked test set without explicit confirmation.** The D16 full book test
   set runs once. The D9 HAR winner is frozen after the training window evaluation. The
   D15 thresholds are frozen before the test. Any rerun is flagged, requires explicit
   confirmation from the user, and is logged.

## 6. Specific to this repo

- **Raw is immutable.** `data/raw/` holds the collected settlement and option tool files.
  Nothing rewrites them, ever. A bug in parsing is fixed by regenerating
  `data/processed/` from raw under the new code. A bug in collection is fixed forward. A
  raw file is never edited to make a downstream step work, and a bad raw file is retained
  with its flag rather than deleted.
- **D15, the skew trade layer, ships only if the D14 research supports it.** D14 is 3
  layers: contemporaneous, lead and lag with the multiple testing caveat, and regime
  dependence on the bottom quintile of stocks. The acceptance gate names layers 1 and 2
  specifically. If the research does not support a tradable lead, the research note ships
  alone and says so plainly, and that is success. Do not weaken a layer, extend a window,
  or add a specification search to manufacture support for building D15.
- **As of 18 August 2026, D5 to D7, D14, and D15 are dropped for a data reason, not a
  research reason, and these are 2 different findings.** D14 cannot run without a strike
  chain; Track A supplies no chain, and Track B, the Euronext verification spike, found the
  only candidate chain source prohibited under terms of use structurally identical to
  CME's. The distinction matters: D14 finding no support after running is a research
  negative and ships as 1; D14 never running because no chain data exists is a data gap and
  ships as that instead. Do not blur the 2 into 1 sentence. `docs/D1-data-audit.md` section
  10.3 states this in full. If a future chain source is identified and verified, this
  reopens as originally specified; nothing about the research first rule changes.
- **D11, the VRP backtest, and D12, the event study, run in modified form.** D11 as
  literally specified enters and exits a real straddle against real settlement prices,
  which needs a chain. Without one, it is a level based proxy using CBOE OVX as the implied
  input and `statarb.pricing` for theoretical valuation, not a backtest against quoted
  markets, and every output says so. D12 substitutes OVX for the spec's literal spanning
  straddle priced move. Both substitutions are recorded, not silent; see the D1 note
  section 10.1.
- **The pre committed cut order**, if the schedule compresses: D15 first, then D13. D12 the
  event study and D10 the decomposition are protected because they carry the research
  weight alone. Do not improvise a different cut.
- **The 2026 crisis walkthrough in D16 is a required exhibit**, including where the book
  loses. A short volatility book looking bad in a crisis is the designed content of that
  section, not a problem to solve before writing it.

## 7. Working habits in this repo

- Read the config before the code. Release timings, costs, thresholds, and windows live in
  `config/` and load through `vol_trading/utils`. A science module that opens a yaml
  directly, or hardcodes a threshold or a timestamp, is a defect.
- **The EIA daily spot series, `wti_cushing` and `henry_hub`, is imported from
  `commodity-data-platform`, never re-ingested here.** That includes the 4 business day
  publication lag rule: it is applied as recorded in the platform repo's
  `config/sources.yaml`, not re-derived locally. `vol_trading/collection/` and
  `vol_trading/realized/` read this through the platform import; a local scraper for the
  same series is the same class of error as reimplementing a shared pricing component and
  is a refusal point, not a shortcut. CBOE OVX is the 1 verified source that stays local:
  a single consumer, project 3 only, ingested here directly.
- An entry in `config/event_calendar.yaml` marked `verified: false` does not feed a signal.
  Flipping those flags is the D4 spot check. Do not invent an exception date to fill a gap.
- Every backtest note carries the history window honesty sentence verbatim, written before
  the results are looked at.
- The 1x, 2x, 4x cost sensitivity table is mandatory in every backtest. If the Sharpe sign
  flips between 1x and 2x, the strategy is labeled not robust to costs and excluded from
  every headline, and the table ships regardless.
- Python 3.11 or later, type hints on public functions, Polars and NumPy and statsmodels as
  the default stack. Validate inputs and fail loudly.
- Never commit or push unless the user asks.
