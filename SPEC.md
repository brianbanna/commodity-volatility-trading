<!--
REDACTION NOTE. This file is PROJECT-3-COMPLETE-AZ.md reproduced verbatim with 1
token level redaction, at Part H rule 1, required by that rule itself: the prior
employer is not named anywhere in this repo. Nothing else is altered: no sentence
removed, no number changed, no deliverable dropped. The unredacted master lives
outside this repo.
-->

# PROJECT 3: COMMODITY VOLATILITY TRADING
## The complete standalone document, A to Z
### Version 2, 10 August 2026. Incorporates all master spec amendments (C1, C4, C5, C8, C10) and the WRDS addendum. Self contained.

---

# PART A. WHAT THIS PROJECT IS, IN PLAIN WORDS

Projects 1 and 2 trade the level of prices and the relationships between prices. This project trades how much prices move.

An option's price contains a forecast: the implied volatility, the amount of movement the market is charging for. Reality then delivers the realized volatility, the amount of movement that actually happened. The gap between the 2 is tradable. If the market persistently charges 35 volatility points for WTI options while WTI persistently realizes 28, then selling those options and hedging away the directional risk collects that 7 point gap, day after day. If the market charges too little before a known event, owning the options into the event pays. And the shape of the volatility surface, whether upside calls cost more than downside puts, carries information about physical scarcity: when Cushing's tanks run critically low, spike protection gets bid, and that skew can be measured against inventory data and traded when it lags.

The project runs those 3 as 1 book. Sub strategy 1, the volatility risk premium: a forecast of realized volatility against the implied level, sell the straddle delta hedged when implied is rich, buy it when cheap. Sub strategy 2, event volatility: the priced move into scheduled releases, EIA petroleum Wednesdays, EIA gas Thursdays, USDA WASDE, against the historical realized move around those exact releases, traded both directions. Sub strategy 3, skew against physical tightness: the 25 delta risk reversal regressed on and traded against Cushing stocks, gas storage, and stocks to use, research first and trade only if the research supports it.

Everything prices through the same engine project 2 froze in December. The audit's central finding governs the data plan: CME removed its free settlement file feed, so daily collection by scraping the delayed settlement pages and the free option settlement tool (which also publishes implied volatilities) is mandatory from day 1, every collected day is owned history, and there is no free backfill, which makes the DataMine academic email the single highest leverage action in the project.

**The 1 sentence the finished project supports:** "I trade commodity volatility 3 ways: systematic risk premium harvesting with daily delta hedging, event volatility around EIA and WASDE prints, and skew against physical inventory data, all running on the same pricing engine as my relative value book."

# PART B. GOALS, RANKED

1. **The collection infrastructure.** Daily chains and surfaces for every market that passes the audit, because in this project the data itself is the scarce asset.
2. **The event study.** Priced versus realized moves per release type across the full collected and purchased history, a standalone publishable artifact even if nothing else ships.
3. **The hedge simulator with the P&L decomposition.** Total P&L split into theta collected, gamma versus implied, vega mark to market, and hedge friction, per closed position. This decomposition is the interview conversation with any volatility trader.
4. **The VRP backtest** with its history window stated honestly.
5. **The event trades and the skew research**, with the skew trade layer shipping only if the 3 layer research supports it.
6. **The book note** with the cross correlation exhibit against projects 1 and 2 and the long form 2026 crisis walkthrough, including where the book loses.

# PART C. WORKED DATA SCENARIOS

**Scenario 1, a VRP entry.** March 2027. WTI 30 day constant maturity ATM implied sits at 34.1. The HAR forecast of the next 21 days' ex event realized volatility says 27.5. The spread, z scored on its trailing year, reads +1.4, above the +1 entry line. The system sells the 38 day straddle nearest ATM, delta hedges at settlement daily, and exits at 10 days to expiry. Over the holding period WTI realizes 26.8; the decomposition shows theta collected exceeding gamma losses, hedge friction small, and a modest vega loss as implied drifted down, net positive, exactly the mechanism the strategy exists to harvest.

**Scenario 2, an event straddle sale.** An EIA petroleum Wednesday. The shortest dated ATM straddle spanning the 10:30 ET release prices a 1 day move of 2.6 percent. The historical distribution of realized moves around this exact release, conditional on a routine week, centers on 1.3 percent with the priced figure in its top quartile. The system sells the straddle at Tuesday's settlement, hedges once, and buys back at Wednesday's settlement. The print lands close to consensus, WTI moves 0.9 percent, implied crushes 4 points, and the trade collects most of the premium. The IV crush series records the episode.

**Scenario 3, skew lagging the tanks.** Cushing stocks print 34 percent below the 5 year norm, deepening for a third straight week. Historically, at this depth of deficit, the WTI 25 delta risk reversal sits around +2.5 (calls over puts); today it reads +0.8, inside its unconditional range but far below its conditional band. Layer 2 of the research has shown tightness leads skew by roughly a week in deficit regimes. The trade buys the 25 delta call, sells the 25 delta put, delta hedges, and holds for the repricing or a time stop. If the research layers had not supported the lead, this scenario would exist only as a documented relationship, not a trade, per the research first rule.

# PART D. THE DELIVERABLES TABLE

| ID | Deliverable | Detail | Format | Acceptance gate | Target date |
|---|---|---|---|---|---|
| D1 | Data audit note | Per market: exact retrieval method for the delayed settlement pages and the option settlement tool, fields available (settlement, IV, OI, volume per strike per expiry), verified free history depth, license notes, PASS/CUT. TTF options DROP confirmed (C10). Minimum 2 PASS markets (WTI + 1) or the project halts and escalates | 1 page per market | Universe locked | 17 Aug 2026 |
| D2 | The DataMine academic email | Historical options EOD for the PASS products, EPFL supervised research framing, 150 EUR threshold, lab escalation as the next step if quoted above | Sent email + outcome logged | Sent | 12 Aug 2026 |
| D3 | Daily collection jobs | Scrapes of the settlement pages AND the option settlement tool (IV cross check), 2x daily, platform scheduled (C8), raw files immutable and checksummed | Platform jobs + data/raw/ | 7 consecutive clean days per market | 18 Aug 2026 |
| D4 | Futures legs + physical + calendar ingestion | CL, NG, ZC/ZS dailies via free sources (WRDS Datastream history spliced if subscribed); EIA petroleum + gas storage + Cushing + utilization; WASDE schedule; event_calendar.yaml with release timestamps in UTC and DST handled there only | Platform jobs + configs | Calendar spot checked against 3 known releases | 25 Aug 2026 |
| D5 | Chain builder | Parse raw into per day per market chains: strikes, expiries, settlements, IVs, OI, volume; moneyness filter 0.5 to 2.0 forward; OI floor 100 across the chain | Code + processed parquet | Rebuild from raw reproduces byte identical output | Jan 2027 |
| D6 | Surface builder | Black 76 inversion (Brent root finder wrapping the project 2 engine) cross checked against the tool's published IVs; ATM interpolated at forward; 25 delta RR and butterfly; delta space cubic spline smile with documented extrapolation; 30 and 60 day constant maturity by variance interpolation | Code + daily surface tables | Inversion vs published IV median absolute gap within tolerance; discrepancies logged | Jan 2027 |
| D7 | Quality flag layer | Arbitrage sanity (call spread monotonicity, butterfly non negativity), stale wing detection (T4 metrics: wing unchanged while ATM moves > 1 point, RR autocorrelation), warn days excluded from signals but retained raw | Code + flags | Deliberately corrupted chain caught | Jan 2027 |
| D8 | Realized volatility library | Close to close 10/21/63 day annualized; Parkinson and Garman Klass where OHLC exists; the event day split: ex event series and event only series, both first class | Code + series | Estimators agree within expected relationships on test data | Feb 2027 |
| D9 | The HAR forecast + comparisons | HAR on daily/weekly/monthly components, target = next 21 day ex event realized; GARCH(1,1) and 21 day naive alongside; out of sample RMSE and Mincer Zarnowitz per market; winner frozen thereafter | Code + evaluation note | Evaluation on the training window only; freeze documented | Feb 2027 |
| D10 | The hedge simulator | Greeks imported from statarb.pricing (never reimplemented); daily settlement hedging base, every 2 days and 0.1 delta band sensitivities; futures hedge costs from the project 2 cost model; THE DECOMPOSITION: theta + gamma vs implied + vega + hedge friction + residual per closed position | Code + decomposition tables | Decomposition sums to total P&L within rounding on every position | Feb 2027 |
| D11 | VRP backtest | Signal: 30 day CM ATM implied minus HAR forecast, z on trailing 252; entry beyond ±1, structure = nearest 25 to 45 day ATM straddle, roll/close at 10 DTE; vega targeted at 25 bps per point; 3x premium stop; no short vol entries within 5 days of a scheduled major release; history window stated verbatim | Backtest + tables | Point in time audit; the window honesty sentence present | Mar 2027 |
| D12 | The event study | Per release type: priced move (shortest straddle spanning, multi day adjusted, formula documented) vs realized settlement to settlement distribution; conditional splits (routine vs report heavy); IV run up and crush term structure exhibits | Standalone note | Publishable alone; every figure regenerable | Mar 2027 |
| D13 | Event trading backtest | Sell rich (top quartile conditional) / own cheap, hedge once at entry, exit post release settlement; fixed 15 bps premium at risk per event; the IV crush series as a reported exhibit | Backtest + tables | Same point in time discipline; per event accounting explicit | Apr 2027 |
| D14 | Skew research, 3 layers | Layer 1 contemporaneous (RR vs tightness), layer 2 lead/lag with the multiple testing caveat stated, layer 3 regime dependence (bottom quintile stocks); vintages as published, never revised | Research note | The research first rule: the trade layer exists only if layers 1 to 2 support it | Apr to May 2027 |
| D15 | Skew trade layer (conditional) | Weekly print moves tightness, RR outside its conditional band → trade the risk reversal delta hedged, reversion or time stop; thresholds frozen pre test | Backtest + tables | Only if D14 supports; frozen thresholds documented | May 2027 |
| D16 | The full book run | All sub strategies combined; test set ONCE, execution logged; Sharpe after costs, drawdowns, worst 5 trades dissected; cross correlations between the 3 sub strategies AND against projects 1 and 2 backtests; the 2026 crisis walkthrough long form including where the book loses | The book note | Protocol verbatim; the crisis walkthrough is a required exhibit, not optional | Jul to Aug 2027 (internship mode) |
| D17 | Portfolio site update | The Part A sentence live under the claims rule | Site | Every quoted number BUILT | Aug 2027 |

# PART E. DATA REGISTER

| Source | What | Verdict | Notes |
|---|---|---|---|
| CME delayed settlement pages | Daily options settlements per product, free to view after midnight CT, top day only, overwritten | PLAUSIBLE FRAGILE (C1) | Scraping, not files; 2x daily redundancy; manifest gap alarms; no free backfill exists |
| CME option settlement tool | Settlement values AND implied volatilities, free, prior business day | VERIFIED as a view | The IV cross check target; same fragility class |
| CME DataMine | Historical options EOD, paid (subscriptions from 105 USD/month observed) | UNVERIFIED PRICE | The D2 email; 150 EUR threshold; the collected window is the base case without it |
| Futures dailies (CL, NG, ZC, ZS) | Free aggregators | PLAUSIBLE | WRDS Datastream upgrade for history if subscribed; free feed remains the living source |
| EIA (petroleum, gas storage, Cushing, utilization) | Weekly + calendar | VERIFIED | US government, clear |
| USDA WASDE | Schedule + stocks to use | VERIFIED | Vintages as published only |
| AGSI+ | EU storage context | VERIFIED | Attribution |
| ICE TTF options | | DROPPED (C10) | Gas volatility carried by Henry Hub |
| WRDS OptionMetrics | Equity and index options only | NOT A FIX | Does not cover CME commodity options; methodology sandbox at most |

# PART F. THE STEP BY STEP PLAN, A TO Z

**Phase 0, week of 11 to 17 August (the only August work: audit + collection, ~1 hour/week thereafter).**
Step 1: the D1 audit per market against the real access paths (settlement pages + the tool), and the WRDS subscription check for Datastream futures history.
Step 2: the D2 DataMine email, sent the same day as project 1's EPEX email.
Step 3: D3 collection jobs live in the platform for every PASS market. From this day the history clock runs.
Step 4: D4 futures, physical, and calendar ingestion the following week.

**Phase 1, 25 August to 8 January: dormancy by design.** Collection runs itself; the weekly platform exceptions check (15 minutes, shared across projects) is the only touch. The semester, the Calvano gate, the engine sprint, and the report own these months.

**Phase 2, the frozen window, 9 January to 6 February: nothing.** (C4.)

**Phase 3, February (internship mode base case, ~1 hour/week here).**
Step 5: D5 chain builder and D6 surface builder on the collected (plus any purchased) history; the inversion cross check against the tool's IVs.
Step 6: D7 quality flags; T4 staleness metrics evaluated for the first time on real collected data.
Step 7: D8 realized library and D9 HAR evaluation, winner frozen.
Step 8: D10 hedge simulator; the decomposition identity verified position by position.

**Phase 4, March (~1 to 2 hours/week).**
Step 9: D11 VRP backtest, entries per the frozen thresholds, the history window sentence written before the results are looked at.
Step 10: D12 the event study across the full window (by now roughly 30+ EIA events per market collected even without a purchase).

**Phase 5, April to May (~1 to 2 hours/week).**
Step 11: D13 event trading backtest.
Step 12: D14 skew research, 3 layers, vintage discipline absolute.
Step 13: D15 only if D14 supports it; otherwise the research note ships alone and says so plainly.

**Phase 6, July to August (the close, ~3 hours/week).**
Step 14: D16 the full book run: test set once, logged; cross correlations against projects 1 and 2; the crisis walkthrough written long form.
Step 15: D17 site update; the Part A sentence goes live.

# PART G. METHODS CORE (COMPRESSED)

Inversion: Brent root finder around statarb.pricing black76, flat short rate from config, rate sensitivity documented as negligible at these tenors. Surface: ATM at forward by interpolation; RR = 25 delta call IV minus 25 delta put IV; butterfly standard; smile = cubic spline in delta space, SVI deferred; constant maturity by linear interpolation in variance. Realized: close to close primary, range estimators where OHLC exists; the ex event / event only split governs which series feeds which sub strategy. HAR: daily, weekly, monthly realized components regressed on next 21 day ex event realized; frozen after training evaluation. VRP: z of (30 day CM implied − HAR forecast) on trailing 252, ±1 entries, straddle 25 to 45 DTE, out at 10 DTE, vega targeted 25 bps per point, 3x premium stop, 5 day pre event exclusion for short entries. Events: priced move = spanning straddle cost / forward with the multi day adjustment; realized = settlement to settlement across the release; conditional quartiles gate the trades; 15 bps premium at risk each. Skew: RR on tightness (Cushing vs 5 year norm, storage vs norm and pace, stocks to use), 3 research layers, trade only on support. Costs: options bid ask as percent of premium per side (WTI ATM 1.5, wings 3; HH ATM 2, wings 4; ags ATM 2, wings 4), futures hedges per the project 2 model, 1x/2x/4x sensitivity mandatory (T5). Hedging: daily at settlement base, 2 day and 0.1 delta band sensitivities reported.

# PART H. RULES

1. Zero [prior employer redacted], ever; unclear provenance excluded.
2. statarb.pricing imported, never reimplemented, never forked; gaps become additive PRs to project 2's package with the harness green.
3. Raw settlement files immutable; fixes regenerate processed from raw, never edit raw; settlement tables never republished anywhere in any artifact.
4. Point in time vintages: WASDE and EIA as published on the day; revised history is lookahead and is refused.
5. The test set runs once; rerun requests are flagged and require explicit confirmation; executions logged.
6. Event timestamps UTC internally; the calendar yaml is the single source of truth; DST lives there and nowhere else.
7. Honest negatives ship: an unharvestable VRP, unsupported skew trading, a thin window. The window honesty sentence appears verbatim in every backtest note.
8. WRDS: futures history block only, academic use, never republished, never a daily dependency.
9. Style: numerals, no hyphens in prose, no marketing language, no emojis, no conduct language about any market participant.

# PART I. RISKS AND PRE COMMITTED FALLBACKS

| Risk | Trigger | Fallback |
|---|---|---|
| Settlement scraping breaks or shallows (C1) | Manifest gap alarm, or fields disappear | Dual target redundancy (pages + tool); 2x daily runs; worst case the universe narrows to the deepest market and the note says so |
| No affordable history | DataMine quote above threshold and the lab cannot help | The collected window IS the backtest: thin for VRP (stated verbatim), adequate for the event study (~35+ EIA events/market by spring), adequate for contemporaneous skew; deeper history is a labeled v2 |
| T4 wing staleness | Wing unchanged while ATM moves > 1 point on > 20 percent of days, or RR autocorrelation > 0.99 | 35 delta metrics, higher OI floor, volume > 0 requirement; sub strategy 3 demotes to research only |
| Short vol drawdown dominates optics | The crisis walkthrough looks bad | It is supposed to: the walkthrough is the designed credibility centerpiece; stops and pre event exclusions are already in the design |
| T5 cost flattery | Sharpe sign flips 1x → 2x | Labeled not robust to costs, excluded from headlines; the sensitivity table ships regardless |
| Internship compresses the tail | Feb to May budgets undershoot | The pre approved cut order: D15 first, then D13; D12 (the event study) and D10 (the decomposition) are protected because they carry the research weight alone |
| Engine gap discovered | A needed payoff or Greek missing | Additive PR to project 2, harness green, tag bumped, dependents repinned deliberately |

# PART J. DEFINITION OF DONE

Minimum viable (June 2027 in internship mode): D1 to D12: collection running since August, surfaces built, realized and HAR evaluated, the hedge simulator with its decomposition verified, the VRP backtest with its stated window, and the standalone event study.
Full (August 2027): D13 to D17: event trades, skew research and its conditional trade layer, the full book run with the test set executed once, the cross correlation exhibit, the crisis walkthrough, and the Part A sentence live with every number BUILT.

# PART K. EXECUTOR NOTES

The data is the scarce asset here: protect the collection jobs above everything else in this project, and treat a manifest gap as the highest priority incident. The 3 refusal points for an executing model: reimplementing or forking the pricing engine, using revised vintages, and rerunning the test set without explicit confirmation. The research first rule on skew is binding: no trade layer without the research support, and shipping the research alone is success, not failure.
