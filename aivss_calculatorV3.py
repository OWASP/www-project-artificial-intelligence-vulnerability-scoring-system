"""
AIVSS Calculator V3
===================
Implements the full AIVSS scoring formula as specified in the AIVSS README spec:

    AIVSS_Score = [(w1 × ModifiedBaseScore) + (w2 × AISpecificMetrics) + (w3 × ImpactScore)]
                  × TemporalMetrics × MitigationMultiplier

    AISpecificMetrics = [MR × DS × EI × DC × AD × AA × LL × GV × CS] × ModelComplexityMultiplier

    Weights: w1=0.3, w2=0.5, w3=0.2 (as recommended by spec)

Fixes vs V1/V2:
  - Adds the 4 missing AI-specific metrics: AA, LL, GV, CS
  - Adds ModelComplexityMultiplier
  - Uses spec-correct weights (w1=0.3, w2=0.5, w3=0.2)
  - Adds Temporal Metrics (E, RL, RC)
  - Adds Environmental Metrics (CR, IR, AR, SIR)
  - Adds MitigationMultiplier
  - Renames "Safety Impact" → "Societal Impact" (correct per spec)
  - Outputs a full score breakdown
"""


def get_choice(parameter_name, options):
    """Prompt user to pick from a numbered list of options. Returns the numeric value."""
    print(f"\n  {parameter_name}:")
    for key, (description, _value) in options.items():
        print(f"    {key}. {description}")
    choice = input("  Choice: ").strip()
    while choice not in options:
        print("  Invalid choice. Please try again.")
        choice = input("  Choice: ").strip()
    return options[choice][1]


# ---------------------------------------------------------------------------
# Metric option tables
# ---------------------------------------------------------------------------

AV_OPTIONS = {
    "1": ("Network (0.85)",          0.85),
    "2": ("Adjacent Network (0.62)", 0.62),
    "3": ("Local (0.55)",            0.55),
    "4": ("Physical (0.20)",         0.20),
}

AC_OPTIONS = {
    "1": ("Low (0.77)",  0.77),
    "2": ("High (0.44)", 0.44),
}

PR_OPTIONS = {
    "1": ("None (0.85)", 0.85),
    "2": ("Low (0.62)",  0.62),
    "3": ("High (0.27)", 0.27),
}

UI_OPTIONS = {
    "1": ("None (0.85)",     0.85),
    "2": ("Required (0.62)", 0.62),
}

S_OPTIONS = {
    "1": ("Unchanged (1.00)", 1.00),
    "2": ("Changed (1.50)",   1.50),
}

# AI-specific metrics: higher score = more severe vulnerability (per spec Section 4)
AI_SEVERITY_OPTIONS = {
    "1": ("Very High – little/no mitigation (1.00)", 1.00),
    "2": ("High – significant weaknesses (0.80)",    0.80),
    "3": ("Medium – some mitigation (0.60)",         0.60),
    "4": ("Low – strong mitigation (0.40)",          0.40),
    "5": ("Very Low / None – formally proven (0.20)", 0.20),
}

MODEL_COMPLEXITY_OPTIONS = {
    "1": ("Simple – narrow, rule-based (1.00)",            1.00),
    "2": ("Moderate – standard ML model (1.20)",           1.20),
    "3": ("Complex – deep network/transformer (1.35)",     1.35),
    "4": ("Highly Complex – frontier LLM/agent (1.50)",   1.50),
}

# Impact metrics: 0.0 (no impact) → 1.0 (critical impact)
IMPACT_OPTIONS = {
    "1": ("None (0.00)",     0.00),
    "2": ("Low (0.22)",      0.22),
    "3": ("Medium (0.56)",   0.56),
    "4": ("High (0.85)",     0.85),
    "5": ("Critical (1.00)", 1.00),
}

# Temporal metrics
EXPLOITABILITY_OPTIONS = {
    "1": ("Unproven – theoretical only (0.91)",     0.91),
    "2": ("Proof-of-Concept – PoC exists (0.94)",  0.94),
    "3": ("Functional – working exploit (0.97)",   0.97),
    "4": ("High – automated/weaponized (1.00)",    1.00),
}

REMEDIATION_LEVEL_OPTIONS = {
    "1": ("Official Fix available (0.87)",   0.87),
    "2": ("Temporary Fix available (0.90)",  0.90),
    "3": ("Workaround available (0.95)",     0.95),
    "4": ("Unavailable – no fix (1.00)",     1.00),
}

REPORT_CONFIDENCE_OPTIONS = {
    "1": ("Unknown – unconfirmed report (0.92)", 0.92),
    "2": ("Reasonable – corroborated (0.96)",    0.96),
    "3": ("Confirmed – vendor-confirmed (1.00)", 1.00),
}

# Environmental requirement metrics
ENV_REQ_OPTIONS = {
    "1": ("Not Defined – inherits base score (1.00)", 1.00),
    "2": ("Low requirement (0.50)",                   0.50),
    "3": ("Medium requirement (1.00)",                1.00),
    "4": ("High requirement (1.50)",                  1.50),
}

MITIGATION_OPTIONS = {
    "1": ("Strong mitigation in place (1.00)",         1.00),
    "2": ("Partial mitigation (1.20)",                 1.20),
    "3": ("Minimal / weak mitigation (1.35)",          1.35),
    "4": ("No mitigation – fully exploitable (1.50)", 1.50),
}


# ---------------------------------------------------------------------------
# Score severity label
# ---------------------------------------------------------------------------

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
    print("=" * 60)
    print("  AIVSS Calculator V3")
    print("  AI Vulnerability Scoring System — Full Spec Implementation")
    print("=" * 60)

    # --- Base Metrics ---
    print("\n[1] BASE METRICS")
    av = get_choice("Attack Vector (AV)", AV_OPTIONS)
    ac = get_choice("Attack Complexity (AC)", AC_OPTIONS)
    pr = get_choice("Privileges Required (PR)", PR_OPTIONS)
    ui = get_choice("User Interaction (UI)", UI_OPTIONS)
    s  = get_choice("Scope (S)", S_OPTIONS)

    base_score = min(10.0, av * ac * pr * ui * s)

    # --- AI-Specific Metrics ---
    print("\n[2] AI-SPECIFIC METRICS  (higher score = more severe vulnerability)")
    mr = get_choice("Model Robustness (MR)", AI_SEVERITY_OPTIONS)
    ds = get_choice("Data Sensitivity (DS)", AI_SEVERITY_OPTIONS)
    ei = get_choice("Ethical Implications (EI)", AI_SEVERITY_OPTIONS)
    dc = get_choice("Decision Criticality (DC)", AI_SEVERITY_OPTIONS)
    ad = get_choice("Adaptability / Monitoring (AD)", AI_SEVERITY_OPTIONS)
    aa = get_choice("Adversarial Attack Surface (AA)", AI_SEVERITY_OPTIONS)
    ll = get_choice("Lifecycle Vulnerabilities (LL)", AI_SEVERITY_OPTIONS)
    gv = get_choice("Governance and Validation (GV)", AI_SEVERITY_OPTIONS)
    cs = get_choice("Cloud/LLM-Specific Security (CS)", AI_SEVERITY_OPTIONS)
    mc = get_choice("Model Complexity Multiplier", MODEL_COMPLEXITY_OPTIONS)

    ai_score = (mr * ds * ei * dc * ad * aa * ll * gv * cs) * mc

    # --- Impact Metrics ---
    print("\n[3] IMPACT METRICS")
    c  = get_choice("Confidentiality Impact (C)", IMPACT_OPTIONS)
    i  = get_choice("Integrity Impact (I)", IMPACT_OPTIONS)
    a  = get_choice("Availability Impact (A)", IMPACT_OPTIONS)
    si = get_choice("Societal Impact (SI)", IMPACT_OPTIONS)

    impact_score = (c + i + a + si) / 4.0

    # --- Temporal Metrics ---
    print("\n[4] TEMPORAL METRICS")
    e   = get_choice("Exploitability (E)", EXPLOITABILITY_OPTIONS)
    rl  = get_choice("Remediation Level (RL)", REMEDIATION_LEVEL_OPTIONS)
    rc  = get_choice("Report Confidence (RC)", REPORT_CONFIDENCE_OPTIONS)

    temporal_score = (e + rl + rc) / 3.0

    # --- Environmental Metrics ---
    print("\n[5] ENVIRONMENTAL REQUIREMENT METRICS  (select 'Not Defined' if unsure)")
    cr  = get_choice("Confidentiality Requirement (CR)", ENV_REQ_OPTIONS)
    ir  = get_choice("Integrity Requirement (IR)", ENV_REQ_OPTIONS)
    ar  = get_choice("Availability Requirement (AR)", ENV_REQ_OPTIONS)
    sir = get_choice("Societal Impact Requirement (SIR)", ENV_REQ_OPTIONS)

    env_component = (cr * ir * ar * sir) * ai_score

    # --- Mitigation Multiplier ---
    print("\n[6] MITIGATION")
    mitigation_multiplier = get_choice("Overall Mitigation Level", MITIGATION_OPTIONS)

    # --- Score Calculations ---
    w1, w2, w3 = 0.3, 0.5, 0.2

    # Final AIVSS score (primary formula from spec Section 5)
    aivss_score = (
        (w1 * base_score) + (w2 * ai_score) + (w3 * impact_score)
    ) * temporal_score * mitigation_multiplier

    aivss_score = min(10.0, aivss_score)

    # Environmental score (contextual, from spec Section 5.4)
    modified_base_score = base_score  # no MAV/MAC/etc. adjustments in this version
    env_score = min(10.0,
        ((modified_base_score + env_component) * temporal_score) * mitigation_multiplier
    )

    # --- Output ---
    print("\n" + "=" * 60)
    print("  AIVSS SCORE BREAKDOWN")
    print("=" * 60)
    print(f"  Base Score          : {base_score:.4f}")
    print(f"  AI-Specific Score   : {ai_score:.4f}")
    print(f"  Impact Score        : {impact_score:.4f}")
    print(f"  Temporal Score      : {temporal_score:.4f}")
    print(f"  Environmental Score : {env_score:.4f}")
    print(f"  Mitigation Multiplier: {mitigation_multiplier:.2f}")
    print("-" * 60)
    print(f"  AIVSS Score         : {aivss_score:.2f}  [{severity_label(aivss_score)}]")
    print("=" * 60)
    print()
    print("  Formula applied:")
    print(f"  AIVSS = [(0.3 × {base_score:.4f}) + (0.5 × {ai_score:.4f}) + (0.2 × {impact_score:.4f})]")
    print(f"          × {temporal_score:.4f} × {mitigation_multiplier:.2f}")
    print(f"        = {aivss_score:.2f}")
    print()

    return aivss_score, env_score


if __name__ == "__main__":
    aivss_score, env_score = calculate_aivss_score()
