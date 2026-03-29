### Simple Python implementation of AIVSS proposal by Ken Huang.
The user can easily assess different vulnerabilities by providing inputs through a series of command-line prompts

<img width="759" alt="Screenshot 2024-12-18 at 3 08 15 PM" src="https://github.com/user-attachments/assets/25870bd2-1f25-4b22-a26b-4cfc3a09b603" />

### Instructions
- Run the Python file from your terminal using `python aivss_calculatorV4.py` (recommended)
- Select your industry profile when prompted (7 options available)
- Provide the appropriate values for each parameter being assessed — V4 breaks each AI metric into sub-categories for more precise scoring
- This will print the calculated AIVSS score and a full component breakdown to the console.

> **Note:** V1 and V2 are deprecated. V3 is spec-compliant but does not support industry-specific weights or sub-category scoring. Use V4 for all new assessments.

### Calculator versions at a glance

| Version | AI Metrics | Weights | Temporal | Env. | Industry Mode | Sub-categories |
|---|---|---|---|---|---|---|
| V1 | 5 / 9 | Incorrect | No | No | No | No |
| V2 | 5 / 9 | Incorrect | No | No | No | No |
| V3 | 9 / 9 | Correct | Yes | Yes | No | No |
| **V4** | **9 / 9** | **Industry-specific** | **Yes** | **Yes** | **Yes (7)** | **Yes (39)** |

### Note
This code provides a basic implementation of the AIVSS framework. You can further customize it by:
- Creating a user interface for easier input and output
- Integrating the code with other security tools.

---

### V2 Updates
Key changes:
- Updated parameter values: The scoring rubric for each parameter (AV, AC, PR, etc.) has been updated to match the values in the GitHub repository.
- New parameter value dictionaries: Dictionaries for the new AI-specific metrics (MR, DS, EI, DC, AD) have been added with their corresponding values and descriptions.
- Updated weights: The weights assigned to the base metrics (w1), AI-specific metrics (w2), and impact metrics (w3) have been updated to 0.25, 0.45, and 0.30, respectively, as per the new scoring methodology.
- Interactive input for all parameters: The code now prompts the user to select values for all parameters, including the AI-specific metrics, using the get_user_input function.

---

### V3 Updates
Full spec-compliant implementation. Key changes (addresses issue #15):
- All 9 AI-specific metrics implemented: adds AA (Adversarial Attack Surface), LL (Lifecycle Vulnerabilities), GV (Governance and Validation), and CS (Cloud/LLM-Specific Security) — V1/V2 only covered 5/9.
- ModelComplexityMultiplier added (1.0–1.5) per spec Section 3.2.
- Corrected weights to spec values: w1=0.3, w2=0.5, w3=0.2.
- Temporal Metrics added: Exploitability (E), Remediation Level (RL), Report Confidence (RC).
- Environmental Requirement Metrics added: CR, IR, AR, SIR.
- MitigationMultiplier added (1.0–1.5).
- "Safety Impact" label corrected to "Societal Impact" per spec.
- Full score breakdown output showing each component and the formula applied.

---

### V4 Updates
Industry mode + sub-category scoring. Key changes:

#### Industry Mode — 7 profiles
Instead of a single global weight set, V4 selects weights and mitigation ranges based on the deployment sector:

| # | Industry | w1 | w2 | w3 | Mitigation range |
|---|---|---|---|---|---|
| 1 | General | 0.30 | 0.50 | 0.20 | 0.70–1.00 |
| 2 | Financial Services | 0.25 | 0.60 | 0.15 | 0.60–1.00 |
| 3 | Healthcare | 0.20 | 0.50 | 0.30 | 0.65–1.00 |
| 4 | Critical Infrastructure | 0.35 | 0.45 | 0.20 | 0.75–1.00 |
| 5 | Automotive / Transport | 0.20 | 0.45 | 0.35 | 0.70–1.00 |
| 6 | Legal / Justice | 0.20 | 0.45 | 0.35 | 0.65–1.00 |
| 7 | Government / Public | 0.25 | 0.50 | 0.25 | 0.70–1.00 |

#### Sub-category scoring — 39 questions across 9 AI metrics
Instead of selecting a single severity level per metric, V4 scores each sub-category individually and averages them — catching hidden critical risks that a top-level selection would smooth over:

| Metric | Sub-categories |
|---|---|
| MR — Model Robustness | Adversarial robustness, distribution shift, output consistency |
| DS — Data Sensitivity | PII exposure, training data sensitivity, data provenance |
| EI — Ethical Impact | Bias/fairness, privacy violation, autonomy impact, societal harm |
| DC — Decision Criticality | Reversibility, human oversight, stakes, deployment scope |
| AD — Adaptability | Concept drift handling, retraining frequency, domain generalization, edge case coverage |
| AA — Agentic Autonomy | Decision authority, goal misalignment risk, multi-step action chains |
| LL — LLM-specific risks | Prompt injection, hallucination rate, jailbreak susceptibility, context window leakage |
| GV — Governance & Visibility | Model documentation, audit logging, explainability, incident response, compliance |
| CS — Contextual Sensitivity | Deployment context, user vulnerability, cultural sensitivity, regulatory environment, data freshness, feedback loops, cascading failures, irreversibility, scale |

#### Other V4 improvements
- Corrected temporal metric values to match the spec precisely (Unproven=0.90, PoC=0.95, OfficialFix=0.95, TempFix=0.96, Workaround=0.97)
- Fixed Impact Medium value: 0.55 (was 0.56 in V3)
- Added "Not Defined" (X) option for temporal, environmental, and modified base metrics
- ASCII-safe output — compatible with Windows cp1252 terminals

#### Running the demonstration test suite
`test_aivss_calculatorV4.py` contains 10 real-world scenarios that demonstrate V4's capabilities:

```
python test_aivss_calculatorV4.py
```

Scenarios covered:
1. Same vulnerability scored across all 7 industry profiles
2. Sub-category scoring catching a hidden critical risk that V3 would miss
3. Severity progression from None to Critical — full score range
4. Financial Services — biased credit scoring LLM
5. Healthcare — diagnostic AI with PHI data breach
6. Critical Infrastructure — power grid adversarial attack
7. Automotive / Transport — AV perception model evasion
8. Legal / Justice — predictive policing bias
9. Government / Public — benefits fraud detection failure
10. Side-by-side V4 vs V3 mathematical score comparison
