# Comparable evidence and acceptance

Derive required invariants from the scoped contracts. Select performance metrics only when they answer the hypothesis. Reuse the native scorecard format and evaluator; [the JSON template](../assets/scorecard.template.json) is for projects without one. A template is not an executable gate: establish a project-native evaluator or explicit reproducible evaluation procedure before claiming results.

For each criterion record ID, contract or rationale, unit, scenario, measurement source, aggregation, operator, threshold, required/advisory status, and sampling plan. Choose thresholds from project requirements and the baseline, not the template. Configure required criteria before running; an empty or unconfigured scorecard cannot pass.

## Measurement protocol

- Record code identity including relevant uncommitted content, OS/runtime/tool versions, workload, concurrency, seed where applicable, warmup, sample count and raw sample location.
- Define repetition and aggregation before comparison. Keep baseline and candidate conditions comparable; distinguish within-run samples from independent repeated runs.
- For nearest-rank P95, sort n observations and select one-based rank ceil(0.95*n). If using a runner's other estimator, record it and use it consistently. Small samples yield weak tail evidence; do not imply precision from a single percentile.
- For binary outcomes, report successes and trials. Zero observed failures or 100% observed recovery describe tested cases, not universal guarantees.
- When independent Bernoulli trials are a defensible model, a two-sided Wilson interval for p-hat = successes/n uses center `(p-hat + z*z/(2*n))/(1 + z*z/n)` and half-width `z*sqrt(p-hat*(1-p-hat)/n + z*z/(4*n*n))/(1 + z*z/n)`. Record confidence level and z. For correlated trials, change the sampling design or explain why this interval is unsuitable.
- Required absent, malformed, nonfinite or insufficient observations are inconclusive, never zero or pass. Prespecify adequacy and uncertainty handling for the decision; do not rerun until a favorable sample appears.

Freeze the scorecard version and test protocol for a comparison. When a discovered test gap changes measurement meaning, version the protocol and rerun the baseline with the new method when possible; otherwise mark the comparison inconclusive. Never relax limits to rescue a candidate.

## Gate and improvement

Use `pass`, `fail`, and `inconclusive` per criterion. A required failure makes the gate fail; otherwise any required inconclusive result makes it inconclusive. Pass requires all required criteria and project checks to pass. Report advisory misses separately. Preserve the project's warning policy rather than imposing universal zero warnings.

Passing invariants establishes acceptability, not improvement. Judge the stated hypothesis using its predefined gain and tolerated regressions. Report no demonstrated gain when evidence does not discriminate. A Lyapunov-style descent claim requires a defined function and justified assumptions; do not apply that label to generic score improvements.

Use failure injection only when relevant and isolated: identify owned processes/files, provoke the real failure boundary, and inspect recovery and residue. Add assertions for demonstrated blind spots, not a quota of tests or metrics per round.

## Statistical reference

NIST/SEMATECH Engineering Statistics Handbook: [percentiles](https://www.itl.nist.gov/div898/handbook/prc/section2/prc262.htm) and [confidence intervals for a proportion](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm). These provide background, not a runtime dependency.
