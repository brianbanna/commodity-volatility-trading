"""Daily collection jobs. SPEC Part D deliverables D3 and D4.

D3  Scrapes of the CME delayed settlement pages AND the option settlement tool, which
    publishes settlement values and implied volatilities for the prior business day.
    Both targets, 2x daily, platform scheduled. The 2 targets are deliberate redundancy:
    the pages carry the top day only and are overwritten, so a missed day is a
    permanently missing day.
D4  Futures legs CL, NG, ZC, ZS via free sources; EIA petroleum, gas storage, Cushing,
    utilization; the USDA WASDE schedule; and config/event_calendar.yaml with release
    timestamps in UTC.

Rules that bind everything in here:
    Raw files are immutable and checksummed. Nothing rewrites a raw file, ever.
    A manifest gap is an incident, not a warning. Collection outranks every other task
        in this repo, including analysis with a nearer deadline.
    Settlement tables are never republished in any artifact, public or private.
    WRDS Datastream futures history is a spliced history block only, academic use, never
        republished, never a daily dependency, splice date recorded in the manifest.

Gate on D3: 7 consecutive clean days per market.
Gate on D4: the calendar spot checked against 3 known releases.
"""
