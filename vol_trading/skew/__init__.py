"""Skew against physical tightness. SPEC Part D deliverables D14 and D15, sub strategy 3.

D14 The research, in 3 layers:
      layer 1, contemporaneous: the 25 delta risk reversal against tightness, meaning
          Cushing stocks against the 5 year norm, gas storage against norm and pace, and
          stocks to use;
      layer 2, lead and lag, with the multiple testing caveat stated in the text, not in
          a footnote;
      layer 3, regime dependence, conditioning on the bottom quintile of stocks.
    Vintages as published, never revised. A revised inventory series is lookahead.

D15 The trade layer, CONDITIONAL. Weekly print moves tightness, the risk reversal sits
    outside its conditional band, trade the risk reversal delta hedged, exit on reversion
    or a time stop, thresholds frozen before the test.

THE RESEARCH FIRST RULE, which is binding and not a preference: D15 exists only if the
D14 research supports it, and the acceptance gate names layers 1 and 2 specifically. If
the research does not support a tradable lead, the research note ships alone and says so
plainly. That is success, not failure. Do not weaken a layer, do not extend a window, and
do not add a specification until something passes, to justify building D15.

D15 is also first in the pre committed cut order in SPEC Part I when the schedule
compresses.
"""
