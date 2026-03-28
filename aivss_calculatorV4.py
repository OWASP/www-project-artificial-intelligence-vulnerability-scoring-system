"""
AIVSS Calculator V4
===================
Full spec-compliant implementation with Industry Mode and sub-category scoring.

Improvements over V3:
  - 7 industry profiles with domain-correct weights and mitigation ranges
  - Sub-category scoring for all 9 AI-specific metrics (39 sub-questions)
  - Modified Base Metrics (MAV, MAC, MPR, MUI, MS) with Not Defined option
  - Environmental Multiplier (per spec Section 5.4)
  - Corrected temporal metric values (per spec Section 5)
  - Fixed Impact Medium value: 0.55 (was 0.56 in V3)
  - Not Defined (1.00) option for all temporal metrics

Industries supported:
  1. General               — Standard AIVSS spec weights
  2. Financial Services    — Fraud detection, trading, credit scoring (GDPR, GLBA, SOX)
  3. Healthcare            — Diagnostics, PHI, patient safety (HIPAA, GDPR)
  4. Critical Infrastructure — Power, water, nuclear, ICS (NERC CIP, IEC 62443)
  5. Automotive / Transport — Autonomous vehicles, ADAS (ISO 26262, SOTIF)
  6. Legal / Justice       — Predictive policing, sentencing AI (EU AI Act, Civil Rights)
  7. Government / Public   — Citizen services, benefits AI (FedRAMP, Privacy Act)

Formula (per spec Section 5):
  AIVSS_Score = [(w1 × ModifiedBaseScore) + (w2 × AISpecificMetrics) + (w3 × ImpactScore)]
                × TemporalMetrics × MitigationMultiplier

  AISpecificMetrics = [MR × DS × EI × DC × AD × AA × LL × GV × CS] × ModelComplexityMultiplier

  Each AI metric score = average of its scored sub-categories

Author: BSec (Bhasker) — https://www.linkedin.com/in/bhaskerkpatel/
"""

# ---------------------------------------------------------------------------
# Industry configurations
# ---------------------------------------------------------------------------

INDUSTRIES = {
    "1": {
        "name": "General",
        "description": "Standard AIVSS spec weights — suitable for any AI system",
        "regulations": "General AI security best practices",
        "w1": 0.30, "w2": 0.50, "w3": 0.20,
        "mitigation_levels": [
            ("Strong mitigation in place (1.00)", 1.00),
            ("Partial mitigation (1.20)", 1.20),
            ("Minimal / weak mitigation (1.35)", 1.35),
            ("No mitigation — fully exploitable (1.50)", 1.50),
        ],
    },
    "2": {
        "name": "Financial Services",
        "description": "Fraud detection, algorithmic trading, credit scoring, AML/KYC",
        "regulations": "GDPR, CCPA, GLBA, SOX, Fair Lending Laws",
        "w1": 0.25, "w2": 0.60, "w3": 0.15,
        "mitigation_levels": [
            ("Strong mitigation — mature security program (1.00)", 1.00),
            ("Moderate mitigation (1.10)", 1.10),
            ("Weak / no mitigation (1.30)", 1.30),
        ],
    },
    "3": {
        "name": "Healthcare",
        "description": "Diagnostics, patient monitoring, drug discovery, PHI processing",
        "regulations": "HIPAA, GDPR, FDA AI/ML guidance, Belmont Report",
        "w1": 0.20, "w2": 0.50, "w3": 0.30,
        "mitigation_levels": [
            ("Strong mitigation (1.00)", 1.00),
            ("Moderate mitigation (1.20)", 1.20),
            ("Weak / no mitigation (1.40)", 1.40),
        ],
    },
    "4": {
        "name": "Critical Infrastructure",
        "description": "Power grids, water systems, nuclear, oil & gas, industrial control",
        "regulations": "NERC CIP, IEC 62443, NIST CSF, Presidential Policy Directive 21",
        "w1": 0.35, "w2": 0.45, "w3": 0.20,
        "mitigation_levels": [
            ("Strong mitigation (1.00)", 1.00),
            ("Moderate mitigation (1.20)", 1.20),
            ("Minimal mitigation (1.40)", 1.40),
            ("No mitigation — critical exposure (1.50)", 1.50),
        ],
    },
    "5": {
        "name": "Automotive / Transportation",
        "description": "Autonomous vehicles, ADAS, traffic management, fleet AI",
        "regulations": "ISO 26262, SOTIF (ISO 21448), UN R155/R156, SAE J3016",
        "w1": 0.20, "w2": 0.45, "w3": 0.35,
        "mitigation_levels": [
            ("Strong mitigation — certified systems (1.00)", 1.00),
            ("Moderate mitigation (1.20)", 1.20),
            ("Minimal mitigation (1.40)", 1.40),
            ("No mitigation — safety critical exposure (1.50)", 1.50),
        ],
    },
    "6": {
        "name": "Legal / Justice",
        "description": "Predictive policing, sentencing/parole AI, case prediction, eDiscovery",
        "regulations": "GDPR, EU AI Act (High-Risk), Civil Rights Laws, Due Process",
        "w1": 0.20, "w2": 0.45, "w3": 0.35,
        "mitigation_levels": [
            ("Strong mitigation (1.00)", 1.00),
            ("Moderate mitigation (1.20)", 1.20),
            ("Minimal mitigation (1.40)", 1.40),
            ("No mitigation (1.50)", 1.50),
        ],
    },
    "7": {
        "name": "Government / Public Sector",
        "description": "Citizen services, benefits determination, border control, public safety AI",
        "regulations": "GDPR, EU AI Act, OMB AI Guidance, FedRAMP, Privacy Act",
        "w1": 0.25, "w2": 0.50, "w3": 0.25,
        "mitigation_levels": [
            ("Strong mitigation (1.00)", 1.00),
            ("Moderate mitigation (1.15)", 1.15),
            ("Minimal mitigation (1.35)", 1.35),
            ("No mitigation (1.50)", 1.50),
        ],
    },
}

# ---------------------------------------------------------------------------
# Base metric tables
# ---------------------------------------------------------------------------

AV_OPTIONS = {
    "1": ("Network (0.85)", 0.85),
    "2": ("Adjacent Network (0.62)", 0.62),
    "3": ("Local (0.55)", 0.55),
    "4": ("Physical (0.20)", 0.20),
}

AC_OPTIONS = {
    "1": ("Low (0.77)", 0.77),
    "2": ("High (0.44)", 0.44),
}

PR_OPTIONS = {
    "1": ("None (0.85)", 0.85),
    "2": ("Low (0.62)", 0.62),
    "3": ("High (0.27)", 0.27),
}

UI_OPTIONS = {
    "1": ("None (0.85)", 0.85),
    "2": ("Required (0.62)", 0.62),
}

S_OPTIONS = {
    "1": ("Unchanged (1.00)", 1.00),
    "2": ("Changed (1.50)", 1.50),
}

# Modified Base Metrics — same options with "X = Not Defined" added
def _add_not_defined(opts):
    return {"X": ("Not Defined — keep base value", None), **opts}

MAV_OPTIONS = _add_not_defined(AV_OPTIONS)
MAC_OPTIONS = _add_not_defined(AC_OPTIONS)
MPR_OPTIONS = _add_not_defined(PR_OPTIONS)
MUI_OPTIONS = _add_not_defined(UI_OPTIONS)
MS_OPTIONS  = _add_not_defined(S_OPTIONS)

MODEL_COMPLEXITY_OPTIONS = {
    "1": ("Simple — narrow, rule-based model (1.00)", 1.00),
    "2": ("Moderate — standard ML / classical model (1.20)", 1.20),
    "3": ("Complex — deep network / transformer (1.35)", 1.35),
    "4": ("Highly Complex — frontier LLM / agentic AI (1.50)", 1.50),
}

# Sub-category severity scale (higher = more severe, per spec Section 4)
SEVERITY = {
    "1": ("Critical — little/no mitigation (0.90)", 0.90),
    "2": ("High — significant weaknesses (0.70)", 0.70),
    "3": ("Medium — some mitigation (0.50)", 0.50),
    "4": ("Low — strong mitigation (0.20)", 0.20),
    "5": ("None — formally proven / no vulnerability (0.00)", 0.00),
}

# Impact metrics (spec: Medium = 0.55)
IMPACT_OPTIONS = {
    "1": ("None (0.00)", 0.00),
    "2": ("Low (0.22)", 0.22),
    "3": ("Medium (0.55)", 0.55),
    "4": ("High (0.85)", 0.85),
    "5": ("Critical (1.00)", 1.00),
}

# Temporal metrics — corrected values per spec Section 5
EXPLOITABILITY_OPTIONS = {
    "X": ("Not Defined (1.00)", 1.00),
    "1": ("Unproven — theoretical only (0.90)", 0.90),
    "2": ("Proof-of-Concept — PoC exists (0.95)", 0.95),
    "3": ("Functional — working exploit (1.00)", 1.00),
    "4": ("High — automated / weaponized (1.00)", 1.00),
}

REMEDIATION_LEVEL_OPTIONS = {
    "X": ("Not Defined (1.00)", 1.00),
    "1": ("Official Fix available (0.95)", 0.95),
    "2": ("Temporary Fix available (0.96)", 0.96),
    "3": ("Workaround available (0.97)", 0.97),
    "4": ("Unavailable — no fix exists (1.00)", 1.00),
}

REPORT_CONFIDENCE_OPTIONS = {
    "X": ("Not Defined (1.00)", 1.00),
    "1": ("Unknown — unconfirmed report (0.92)", 0.92),
    "2": ("Reasonable — corroborated (0.96)", 0.96),
    "3": ("Confirmed — vendor-confirmed (1.00)", 1.00),
}

ENV_REQ_OPTIONS = {
    "X": ("Not Defined — inherits base score (1.00)", 1.00),
    "1": ("Low requirement (0.50)", 0.50),
    "2": ("Medium requirement (1.00)", 1.00),
    "3": ("High requirement (1.50)", 1.50),
}

ENV_MULTIPLIER_OPTIONS = {
    "1": ("None — no additional environmental factors (0.00)", 0.00),
    "2": ("Low — minor environmental amplification (0.05)", 0.05),
    "3": ("Medium — moderate environmental amplification (0.15)", 0.15),
    "4": ("High — significant environmental amplification (0.30)", 0.30),
}

# ---------------------------------------------------------------------------
# AI-Specific Metric Sub-categories (per spec Section 4)
# ---------------------------------------------------------------------------

AI_SUBCATEGORIES = [
    ("MR", "Model Robustness", [
        "Evasion Resistance",
        "Gradient Masking / Obfuscation",
        "Robustness Certification",
    ]),
    ("DS", "Data Sensitivity", [
        "Data Confidentiality",
        "Data Integrity",
        "Data Provenance",
    ]),
    ("EI", "Ethical Implications", [
        "Bias and Discrimination",
        "Transparency and Explainability",
        "Accountability",
        "Societal Impact",
    ]),
    ("DC", "Decision Criticality", [
        "Safety-Critical Applications",
        "Financial Impact",
        "Reputational Damage",
        "Operational Disruption",
    ]),
    ("AD", "Adaptability", [
        "Continuous Monitoring",
        "Retraining Capabilities",
        "Threat Intelligence Integration",
        "Adversarial Training",
    ]),
    ("AA", "Adversarial Attack Surface", [
        "Model Inversion",
        "Model Extraction",
        "Membership Inference",
    ]),
    ("LL", "Lifecycle Vulnerabilities", [
        "Development Security",
        "Training Security",
        "Deployment Security",
        "Operational Security",
    ]),
    ("GV", "Governance and Validation", [
        "Regulatory Compliance",
        "Auditing",
        "Risk Management",
        "Human Oversight",
        "Ethical Framework Alignment",
    ]),
    ("CS", "Cloud / LLM Security (CSA Taxonomy)", [
        "Model Manipulation / Prompt Injection",
        "Data Poisoning",
        "Sensitive Data Disclosure",
        "Model Stealing",
        "Failure / Malfunctioning",
        "Insecure Supply Chain",
        "Insecure Apps / Plugins",
        "Denial of Service (DoS)",
        "Loss of Governance / Compliance",
    ]),
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_choice(label, options):
    """Prompt for a menu choice. Returns the numeric value associated with the key."""
    print(f"\n  {label}:")
    for key, (desc, _val) in options.items():
        print(f"    {key}. {desc}")
    choice = input("  Choice: ").strip().upper()
    while choice not in options:
        print("  Invalid — please enter one of: " + ", ".join(options.keys()))
        choice = input("  Choice: ").strip().upper()
    return options[choice][1]


def score_metric(code, label, subcats):
    """Score one AI metric by averaging its sub-category severity scores."""
    print(f"\n  [{code}] {label}  ({len(subcats)} sub-categories)")
    scores = []
    for idx, subcat in enumerate(subcats, 1):
        val = get_choice(f"{idx}/{len(subcats)}  {subcat}", SEVERITY)
        scores.append(val)
    avg = sum(scores) / len(scores)
    print(f"    >> {code} score: {avg:.3f}  (avg of {len(subcats)} sub-categories)")
    return avg, scores


def severity_label(score):
    if score >= 9.0:
        return "Critical"
    elif score >= 7.0:
        return "High"
    elif score >= 4.0:
        return "Medium"
    elif score > 0.0:
        return "Low"
    return "None"


# ---------------------------------------------------------------------------
# Main calculator
# ---------------------------------------------------------------------------

def calculate_aivss_score():
    print("=" * 68)
    print("  AIVSS Calculator V4")
    print("  AI Vulnerability Scoring System — Industry Mode + Sub-category Scoring")
    print("=" * 68)

    # ── Industry Mode ────────────────────────────────────────────────────────
    print("\n[0] SELECT INDUSTRY MODE")
    print(f"  {'#':<4} {'Industry':<30} Description")
    print("  " + "-" * 64)
    for key, cfg in INDUSTRIES.items():
        print(f"  {key:<4} {cfg['name']:<30} {cfg['description']}")

    ind = input("\n  Choice: ").strip()
    while ind not in INDUSTRIES:
        print("  Invalid — enter 1–7.")
        ind = input("  Choice: ").strip()

    industry = INDUSTRIES[ind]
    w1, w2, w3 = industry["w1"], industry["w2"], industry["w3"]

    print(f"\n  Mode      : {industry['name']}")
    print(f"  Weights   : w1={w1} (Base)  w2={w2} (AI-Specific)  w3={w3} (Impact)")
    print(f"  Key Regs  : {industry['regulations']}")

    # ── Base Metrics ─────────────────────────────────────────────────────────
    print("\n[1] BASE METRICS")
    av = get_choice("Attack Vector (AV)", AV_OPTIONS)
    ac = get_choice("Attack Complexity (AC)", AC_OPTIONS)
    pr = get_choice("Privileges Required (PR)", PR_OPTIONS)
    ui = get_choice("User Interaction (UI)", UI_OPTIONS)
    s  = get_choice("Scope (S)", S_OPTIONS)

    base_score = min(10.0, av * ac * pr * ui * s)

    # ── Modified Base Metrics ────────────────────────────────────────────────
    print("\n[2] MODIFIED BASE METRICS  (X = Not Defined, keeps base value)")
    raw_mav = get_choice("Modified Attack Vector (MAV)", MAV_OPTIONS)
    raw_mac = get_choice("Modified Attack Complexity (MAC)", MAC_OPTIONS)
    raw_mpr = get_choice("Modified Privileges Required (MPR)", MPR_OPTIONS)
    raw_mui = get_choice("Modified User Interaction (MUI)", MUI_OPTIONS)
    raw_ms  = get_choice("Modified Scope (MS)", MS_OPTIONS)

    mav = raw_mav if raw_mav is not None else av
    mac = raw_mac if raw_mac is not None else ac
    mpr = raw_mpr if raw_mpr is not None else pr
    mui = raw_mui if raw_mui is not None else ui
    ms  = raw_ms  if raw_ms  is not None else s

    modified_base_score = min(10.0, mav * mac * mpr * mui * ms)

    # ── AI-Specific Metrics (sub-category scoring) ───────────────────────────
    print("\n[3] AI-SPECIFIC METRICS — Sub-category scoring")
    print("    Severity scale: Critical(0.90) High(0.70) Medium(0.50) Low(0.20) None(0.00)")
    print("    Higher score = more severe vulnerability")

    metric_scores = {}
    subcat_detail = {}
    for code, label, subcats in AI_SUBCATEGORIES:
        avg, scores = score_metric(code, label, subcats)
        metric_scores[code] = avg
        subcat_detail[code] = (label, subcats, scores)

    mc = get_choice("\n  Model Complexity Multiplier", MODEL_COMPLEXITY_OPTIONS)

    ai_score = (
        metric_scores["MR"] * metric_scores["DS"] * metric_scores["EI"] *
        metric_scores["DC"] * metric_scores["AD"] * metric_scores["AA"] *
        metric_scores["LL"] * metric_scores["GV"] * metric_scores["CS"]
    ) * mc

    # ── Impact Metrics ───────────────────────────────────────────────────────
    print("\n[4] IMPACT METRICS")
    c  = get_choice("Confidentiality Impact (C)", IMPACT_OPTIONS)
    i  = get_choice("Integrity Impact (I)", IMPACT_OPTIONS)
    a  = get_choice("Availability Impact (A)", IMPACT_OPTIONS)
    si = get_choice("Societal Impact (SI)", IMPACT_OPTIONS)

    impact_score = (c + i + a + si) / 4.0

    # ── Temporal Metrics ─────────────────────────────────────────────────────
    print("\n[5] TEMPORAL METRICS  (X = Not Defined)")
    e  = get_choice("Exploitability (E)", EXPLOITABILITY_OPTIONS)
    rl = get_choice("Remediation Level (RL)", REMEDIATION_LEVEL_OPTIONS)
    rc = get_choice("Report Confidence (RC)", REPORT_CONFIDENCE_OPTIONS)

    temporal_score = (e + rl + rc) / 3.0

    # ── Environmental Metrics ────────────────────────────────────────────────
    print("\n[6] ENVIRONMENTAL REQUIREMENT METRICS  (X = Not Defined)")
    cr  = get_choice("Confidentiality Requirement (CR)", ENV_REQ_OPTIONS)
    ir  = get_choice("Integrity Requirement (IR)", ENV_REQ_OPTIONS)
    ar  = get_choice("Availability Requirement (AR)", ENV_REQ_OPTIONS)
    sir = get_choice("Societal Impact Requirement (SIR)", ENV_REQ_OPTIONS)
    env_mult = get_choice("Environmental Multiplier", ENV_MULTIPLIER_OPTIONS)

    env_component = (cr * ir * ar * sir) * ai_score
    env_score = min(10.0,
        ((modified_base_score + env_component) * temporal_score) * (1 + env_mult)
    )

    # ── Mitigation ───────────────────────────────────────────────────────────
    print(f"\n[7] MITIGATION  [{industry['name']} scale]")
    mit_opts = {str(i + 1): opt for i, opt in enumerate(industry["mitigation_levels"])}
    mit = get_choice("Mitigation Level", mit_opts)

    # ── Score Calculation ────────────────────────────────────────────────────
    aivss_score = min(10.0, (
        (w1 * modified_base_score) +
        (w2 * ai_score) +
        (w3 * impact_score)
    ) * temporal_score * mit)

    # ── Output ───────────────────────────────────────────────────────────────
    print("\n" + "=" * 68)
    print(f"  AIVSS V4 — SCORE BREAKDOWN  [{industry['name'].upper()}]")
    print("=" * 68)
    print(f"  Industry          : {industry['name']}")
    print(f"  Regulations       : {industry['regulations']}")
    print(f"  Weights           : w1={w1}  w2={w2}  w3={w3}")
    print()
    print(f"  Base Score        : {base_score:.4f}")
    print(f"  Modified Base     : {modified_base_score:.4f}")
    print()
    print("  AI-Specific Sub-scores:")
    for code, label, subcats in AI_SUBCATEGORIES:
        score = metric_scores[code]
        _, _, scores = subcat_detail[code]
        sub_str = "  ".join(f"{sc}={sv:.2f}" for sc, sv in zip(subcats, scores))
        print(f"    {code}  {label:<38}: {score:.3f}")
        print(f"         {sub_str}")
    print(f"  Model Complexity  : ×{mc:.2f}")
    print(f"  AI-Specific Score : {ai_score:.6f}")
    print()
    print(f"  Impact Score      : {impact_score:.4f}")
    print(f"  Temporal Score    : {temporal_score:.4f}")
    print(f"  Env Score         : {env_score:.4f}")
    print(f"  Mitigation        : ×{mit:.2f}")
    print()
    print("-" * 68)
    print(f"  AIVSS SCORE       : {aivss_score:.2f}  [{severity_label(aivss_score)}]")
    print("=" * 68)
    print()
    print("  Formula applied:")
    print(f"  [({w1} × {modified_base_score:.4f}) + ({w2} × {ai_score:.6f}) + ({w3} × {impact_score:.4f})]")
    print(f"  × {temporal_score:.4f} × {mit:.2f}  =  {aivss_score:.2f}")
    print()

    return aivss_score, env_score


if __name__ == "__main__":
    calculate_aivss_score()
