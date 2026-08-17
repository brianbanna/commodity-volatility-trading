"""Hedge simulator and the P&L decomposition. SPEC Part D deliverable D10.

Greeks are imported from `statarb.pricing`. They are never reimplemented here, never
copied here, never forked. If a payoff or a Greek is missing, the answer is an additive
pull request to that package with its harness green, a tag bump, and a deliberate repin
here. It is never a local implementation.

Base case: delta hedging daily at settlement. Sensitivities reported at every 2 days and
at a 0.1 delta band. Futures hedge costs come from the project 2 cost model.

THE DECOMPOSITION, which is the point of this deliverable:

    total P&L = theta collected
              + gamma against implied
              + vega mark to market
              + hedge friction
              + residual

Gate: the decomposition sums to total P&L within rounding on every closed position. Not
on average, not on most, on every one. A position where it does not sum is a defect in the
decomposition, not an acceptable residual.

This deliverable is protected under the pre committed cut order in SPEC Part I: if the
schedule compresses, D15 is cut first, then D13. D10 and D12 carry the research weight
alone and are not cut.
"""
