"""
AIVSS Calculator V4 — Test Cases & Demonstration Suite
=======================================================
Demonstrates the capabilities and benefits of aivss_calculatorV4.py
through 10 real-world scenarios covering all 7 industry modes.

Run with:  python test_aivss_calculatorV4.py

What this demonstrates:
  1. Same vulnerability scored across all 7 industry modes
     → shows how weights shift severity by sector
  2. Sub-category scoring catches hidden risk
     → one critical sub-category elevates an otherwise medium metric
  3. Severity progression — Low to Critical
     → shows the full score range in practice
  4. Real-world scenarios per industry:
        Financial   — Biased credit scoring LLM
        Healthcare  — Diagnostic imaging AI data breach
        Critical Infra — Adversarial attack on grid control AI
        Automotive  — AV perception model evasion
        Legal/Justice — Predictive policing bias incident
        Government  — Benefits fraud detection AI failure
  5. V4 vs V3 comparison
     → shows additional metrics and corrected values produce different scores

Author: BSec (Bhasker) — https://www.linkedin.com/in/bhaskerkpatel/
"""

import importlib.util
import io
import sys

# ---------------------------------------------------------------------------
# Load V4 module
# ---------------------------------------------------------------------------

def load_v4():
    spec = importlib.util.spec_from_file_location("aivss_v4", "aivss_calculatorV4.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

# ---------------------------------------------------------------------------
# Silent runner — feeds predefined inputs, captures score
# ---------------------------------------------------------------------------

def run_scenario(mod, inputs_str):
    """Run calculator with predefined inputs. Returns (aivss_score, env_score)."""
    old_stdin  = sys.stdin
    old_stdout = sys.stdout
    sys.stdin  = io.StringIO(inputs_str)
    sys.stdout = io.StringIO()
    try:
        score, env = mod.calculate_aivss_score()
        output = sys.stdout.getvalue()
    finally:
        sys.stdin  = old_stdin
        sys.stdout = old_stdout
    return score, env, output

# ---------------------------------------------------------------------------
# Input builders
# ---------------------------------------------------------------------------

def B(av, ac, pr, ui, s):
    """Base metrics: av/ac/pr/ui/s as option numbers (strings)."""
    return f"{av}\n{ac}\n{pr}\n{ui}\n{s}\n"

def MB():
    """Modified base: all Not Defined (inherit from base)."""
    return "X\nX\nX\nX\nX\n"

def AI(scores):
    """39 AI sub-category scores as list of option keys (1=Critical..5=None)."""
    assert len(scores) == 39, f"Expected 39 AI sub-scores, got {len(scores)}"
    return "".join(f"{s}\n" for s in scores)

def AI_uniform(level):
    """All 39 AI sub-categories at the same level."""
    return AI([level] * 39)

def IM(c, i, a, si):
    """Impact metrics."""
    return f"{c}\n{i}\n{a}\n{si}\n"

def TM(e="X", rl="X", rc="X"):
    """Temporal metrics (X = Not Defined)."""
    return f"{e}\n{rl}\n{rc}\n"

def ER(cr="X", ir="X", ar="X", sir="X"):
    """Environmental requirement metrics."""
    return f"{cr}\n{ir}\n{ar}\n{sir}\n"

def scenario(industry, base_opts, ai_scores, mc, impact_opts,
             temporal="X\nX\nX\n", env_req="X\nX\nX\nX\n",
             env_mult="1", mitigation="1", modified_base=None):
    """Compose a full scenario input string."""
    mb = modified_base if modified_base else MB()
    return (
        f"{industry}\n"
        + B(*base_opts)
        + mb
        + AI(ai_scores)
        + f"{mc}\n"
        + IM(*impact_opts)
        + temporal
        + env_req
        + f"{env_mult}\n"
        + f"{mitigation}\n"
    )

# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

SEP  = "=" * 72
SEP2 = "-" * 72

def header(title):
    print()
    print(SEP)
    print(f"  {title}")
    print(SEP)

def result_line(label, score, env, note=""):
    sev = severity_label(score)
    note_str = f"  ({note})" if note else ""
    print(f"  {label:<45}  {score:>5.2f}  [{sev:<8}]{note_str}")

def severity_label(score):
    if score >= 9.0: return "Critical"
    if score >= 7.0: return "High"
    if score >= 4.0: return "Medium"
    if score > 0.0:  return "Low"
    return "None"

def subheader(text):
    print(f"\n  -- {text}")

# ---------------------------------------------------------------------------
# Test scenarios
# ---------------------------------------------------------------------------

def test_cross_industry_same_vulnerability(mod):
    """
    SCENARIO 1: Same AI system scored across all 7 industry modes.

    Vulnerability profile: An LLM-based decision support system with:
      - Network-accessible, low complexity attack
      - Medium AI-specific risk across all dimensions
      - High confidentiality and integrity impact
      - Functional exploit available, no official fix

    Shows: How industry weights shift the risk score for the same system.
    """
    header("SCENARIO 1: Same Vulnerability — All 7 Industry Modes")
    print("  Vulnerability: Network-accessible LLM decision support system")
    print("  Base: Network/Low complexity | AI: all Medium | Impact: High C+I, Medium A+SI")
    print("  Temporal: Functional exploit / No fix / Confirmed")
    print()
    print(f"  {'Industry':<35} {'Score':>6}  Severity    Weights (w1/w2/w3)")
    print(f"  {'-'*35} {'-'*6}  {'-'*8}    {'-'*20}")

    industries = {
        "1": ("General",                "0.30 / 0.50 / 0.20"),
        "2": ("Financial Services",     "0.25 / 0.60 / 0.15"),
        "3": ("Healthcare",             "0.20 / 0.50 / 0.30"),
        "4": ("Critical Infrastructure","0.35 / 0.45 / 0.20"),
        "5": ("Automotive/Transport",   "0.20 / 0.45 / 0.35"),
        "6": ("Legal / Justice",        "0.20 / 0.45 / 0.35"),
        "7": ("Government / Public",    "0.25 / 0.50 / 0.25"),
    }

    for ind_key, (ind_name, weights) in industries.items():
        inp = scenario(
            industry    = ind_key,
            base_opts   = ("1", "1", "1", "1", "1"),    # Network/Low/None/None/Unchanged
            ai_scores   = [3] * 39,                      # all Medium
            mc          = "1",                           # Simple model
            impact_opts = ("4", "4", "3", "3"),          # High C+I, Medium A+SI
            temporal    = TM("3", "4", "3"),             # Functional/Unavailable/Confirmed
            mitigation  = "2",                           # Partial mitigation
        )
        score, env, _ = run_scenario(mod, inp)
        sev = severity_label(score)
        print(f"  {ind_name:<35} {score:>6.2f}  {sev:<10}  {weights}")

    print()
    print("  Insight: Healthcare and Automotive score highest due to elevated w3")
    print("           (impact weight) — patient safety and life-critical decisions")
    print("           amplify identical technical risk.")


def test_subcategory_hidden_risk(mod):
    """
    SCENARIO 2: Sub-category scoring catches hidden risk.

    Two identical systems except one has a critical Data Poisoning
    vulnerability buried within its CS (Cloud/LLM Security) metric.
    V4 catches this; V3's single-score approach would average it away.
    """
    header("SCENARIO 2: Sub-category Scoring Catches Hidden Risk")
    print("  Two systems, identical except one has a critical Data Poisoning flaw.")
    print("  V4 sub-category scoring surfaces this; a single-score approach hides it.")
    print()

    # CS sub-categories (9): all Low except Data Poisoning = Critical
    # Positions: MR(3) DS(3) EI(4) DC(4) AD(4) AA(3) LL(4) GV(5) CS(9) = 39
    # CS starts at index 30
    ai_clean    = [4] * 39                   # all Low (strong mitigation)
    ai_poisoned = [4] * 39
    ai_poisoned[31] = 1                      # CS[1] = Data Poisoning → Critical

    inp_clean = scenario("1", ("1","1","1","1","1"), ai_clean, "3",
                         ("3","3","3","3"), mitigation="1")
    inp_poison = scenario("1", ("1","1","1","1","1"), ai_poisoned, "3",
                          ("3","3","3","3"), mitigation="1")

    s_clean, _, _ = run_scenario(mod, inp_clean)
    s_poison, _, _ = run_scenario(mod, inp_poison)

    print(f"  {'System':<45}  {'Score':>5}  Severity")
    print(f"  {'-'*45}  {'-'*5}  {'-'*8}")
    print(f"  {'System A — all sub-categories Low risk':<45}  {s_clean:>5.2f}  {severity_label(s_clean)}")
    print(f"  {'System B — one critical Data Poisoning flaw':<45}  {s_poison:>5.2f}  {severity_label(s_poison)}")
    print()
    print(f"  Score increase from single hidden flaw: +{s_poison - s_clean:.2f}")
    print("  Insight: Sub-category scoring ensures one critical weakness")
    print("           raises the overall metric score even when other sub-")
    print("           categories are well-mitigated.")


def test_severity_progression(mod):
    """
    SCENARIO 3: Severity progression — None to Critical.

    Shows the full score range as AI risk severity increases
    uniformly across all 39 sub-categories.
    """
    header("SCENARIO 3: Severity Progression — None to Critical")
    print("  All 39 AI sub-categories set to the same severity level.")
    print("  Base: Network/Low, Impact: High, Temporal: Confirmed exploit.")
    print()
    print(f"  {'AI Severity Level':<30}  {'AI Score':>9}  {'AIVSS Score':>11}  Severity")
    print(f"  {'-'*30}  {'-'*9}  {'-'*11}  {'-'*8}")

    levels = [
        ("5 — None (0.00)",     5),
        ("4 — Low (0.20)",      4),
        ("3 — Medium (0.50)",   3),
        ("2 — High (0.70)",     2),
        ("1 — Critical (0.90)", 1),
    ]
    ai_vals = {5: 0.00, 4: 0.20, 3: 0.50, 2: 0.70, 1: 0.90}

    for label, lvl in levels:
        inp = scenario("1", ("1","1","1","1","2"), [lvl]*39, "4",
                       ("4","4","4","4"), temporal=TM("3","4","3"), mitigation="3")
        score, _, _ = run_scenario(mod, inp)
        ai_score = ai_vals[lvl] ** 9 * 1.50
        print(f"  {label:<30}  {ai_score:>9.5f}  {score:>11.2f}  {severity_label(score)}")

    print()
    print("  Insight: The multiplicative AI formula (9 metrics × multiplier)")
    print("           compresses scores toward zero at lower severities.")
    print("           Even all-Critical (0.90^9 x 1.5 = 0.58) stays below High.")
    print("           Maintainers may wish to consider geometric mean as an")
    print("           alternative aggregation method in a future spec revision.")


def test_financial_biased_credit_scoring(mod):
    """
    SCENARIO 4: Financial — Biased credit scoring LLM.

    A bank's LLM-based credit scoring system with documented bias
    against minority applicants, weak data governance, and no official fix.
    """
    header("SCENARIO 4 [Financial] — Biased Credit Scoring LLM")
    print("  System: LLM credit scoring model with documented bias,")
    print("          sensitive PII data, weak governance, no official fix.")
    print()

    # MR(3): Med/Low/Low | DS(3): High/High/Med | EI(4): Crit/High/High/High
    # DC(4): Low/Crit/High/Med | AD(4): Med/Low/Low/Low | AA(3): High/High/Med
    # LL(4): Med/Med/Low/Low | GV(5): Crit/Med/Med/High/Med | CS(9): Med*9
    ai = [
        3,4,4,           # MR
        2,2,3,           # DS
        1,2,2,2,         # EI — bias is Critical
        4,1,2,3,         # DC — financial impact Critical
        3,4,4,4,         # AD
        2,2,3,           # AA
        3,3,4,4,         # LL
        1,3,3,2,3,       # GV — compliance Critical
        3,3,3,3,3,3,3,3,3,  # CS
    ]
    assert len(ai) == 39

    inp = scenario(
        industry    = "2",
        base_opts   = ("1","1","1","1","1"),
        ai_scores   = ai,
        mc          = "3",                           # Complex LLM
        impact_opts = ("4","3","2","4"),             # High C, Med I, Low A, High SI
        temporal    = TM("2","4","3"),               # PoC/No fix/Confirmed
        mitigation  = "2",                           # Moderate
    )
    score, env, _ = run_scenario(mod, inp)
    print(f"  AIVSS Score  : {score:.2f}  [{severity_label(score)}]")
    print(f"  Env Score    : {env:.2f}")
    print()
    print("  Key risk drivers: EI (bias Critical), GV (compliance Critical),")
    print("  DC (financial impact Critical), DS (PII High risk).")
    print("  Remediation priority: bias audit, compliance program, explainability.")


def test_healthcare_diagnostic_breach(mod):
    """
    SCENARIO 5: Healthcare — Diagnostic AI data breach.

    Hospital diagnostic imaging AI with PHI exposure,
    compromised supply chain, and a functional exploit in the wild.
    """
    header("SCENARIO 5 [Healthcare] — Diagnostic AI PHI Data Breach")
    print("  System: Medical imaging diagnostic AI, PHI exposed,")
    print("          insecure supply chain, functional exploit confirmed.")
    print()

    ai = [
        2,3,3,           # MR
        1,2,2,           # DS — data confidentiality Critical (PHI)
        2,2,3,3,         # EI
        1,2,2,2,         # DC — safety critical
        3,4,3,3,         # AD
        2,3,3,           # AA
        3,2,3,3,         # LL
        2,3,3,3,2,       # GV
        2,1,1,3,2,2,3,3,2,  # CS — data poisoning + sensitive disclosure Critical
    ]
    assert len(ai) == 39

    inp = scenario(
        industry    = "3",
        base_opts   = ("2","1","2","1","2"),         # Adjacent/Low/Low/None/Changed
        ai_scores   = ai,
        mc          = "3",
        impact_opts = ("5","4","3","4"),             # Critical C, High I+SI, Med A
        temporal    = TM("3","4","3"),               # Functional/No fix/Confirmed
        env_req     = ER("X","X","X","3"),           # High societal requirement
        mitigation  = "2",
    )
    score, env, _ = run_scenario(mod, inp)
    print(f"  AIVSS Score  : {score:.2f}  [{severity_label(score)}]")
    print(f"  Env Score    : {env:.2f}")
    print()
    print("  Key risk drivers: DS (PHI Critical), CS (data poisoning + disclosure),")
    print("  DC (safety-critical), High societal impact requirement (SIR).")
    print("  Remediation priority: PHI encryption, supply chain audit, HIPAA review.")


def test_critical_infra_grid_attack(mod):
    """
    SCENARIO 6: Critical Infrastructure — Power grid AI attack.

    AI-controlled load balancing system with a functional adversarial
    attack that could trigger cascading grid failures.
    """
    header("SCENARIO 6 [Critical Infra] — Power Grid AI Adversarial Attack")
    print("  System: AI load balancing controller for power grid,")
    print("          adversarial attack can trigger cascading failures.")
    print()

    ai = [
        1,2,2,           # MR — evasion resistance Critical
        3,2,3,           # DS
        3,3,4,2,         # EI
        1,2,3,1,         # DC — safety Critical, operational disruption Critical
        2,3,2,2,         # AD
        1,2,2,           # AA — model inversion Critical
        2,2,2,2,         # LL
        2,2,2,3,3,       # GV
        1,2,3,3,2,2,3,2,2,  # CS — model manipulation Critical
    ]
    assert len(ai) == 39

    inp = scenario(
        industry    = "4",
        base_opts   = ("1","1","1","1","2"),         # Network/Low/None/None/Changed
        ai_scores   = ai,
        mc          = "2",
        impact_opts = ("4","5","5","5"),             # High C, Critical I+A+SI
        temporal    = TM("3","4","3"),               # Functional/No fix/Confirmed
        env_req     = ER("3","3","3","3"),           # All High requirements
        env_mult    = "3",
        mitigation  = "3",
    )
    score, env, _ = run_scenario(mod, inp)
    print(f"  AIVSS Score  : {score:.2f}  [{severity_label(score)}]")
    print(f"  Env Score    : {env:.2f}")
    print()
    print("  Key risk drivers: DC (safety + disruption Critical), MR (evasion"),
    print("  Critical), CS (model manipulation), all env requirements High.")
    print("  Remediation priority: adversarial hardening, air-gap deployment,")
    print("  IEC 62443 compliance, real-time anomaly detection.")


def test_automotive_av_evasion(mod):
    """
    SCENARIO 7: Automotive — AV perception model evasion.

    Autonomous vehicle perception model vulnerable to adversarial
    patch attacks on stop signs, no official patch available.
    """
    header("SCENARIO 7 [Automotive] — AV Perception Model Evasion Attack")
    print("  System: Autonomous vehicle object detection model,")
    print("          adversarial patches fool stop-sign recognition.")
    print()

    ai = [
        1,1,3,           # MR — evasion Critical, gradient masking Critical
        3,2,3,           # DS
        3,2,3,3,         # EI
        1,3,2,1,         # DC — safety Critical, operational Critical
        2,2,3,2,         # AD
        1,3,2,           # AA — model inversion Critical
        3,3,2,3,         # LL
        3,3,2,3,2,       # GV
        1,3,3,3,1,3,3,3,3,  # CS — manipulation + failure Critical
    ]
    assert len(ai) == 39

    inp = scenario(
        industry    = "5",
        base_opts   = ("3","1","1","1","2"),         # Local/Low/None/None/Changed
        ai_scores   = ai,
        mc          = "3",
        impact_opts = ("3","4","4","5"),             # Med C, High I+A, Critical SI
        temporal    = TM("3","4","3"),               # Functional/No fix/Confirmed
        env_req     = ER("X","3","3","3"),           # High I+A+SI requirements
        mitigation  = "3",
    )
    score, env, _ = run_scenario(mod, inp)
    print(f"  AIVSS Score  : {score:.2f}  [{severity_label(score)}]")
    print(f"  Env Score    : {env:.2f}")
    print()
    print("  Key risk drivers: MR (evasion Critical), DC (safety-critical),")
    print("  CS (manipulation + failure Critical), Critical societal impact.")
    print("  Remediation priority: adversarial training, certified robustness,")
    print("  ISO 26262 ASIL-D compliance, OTA patch process.")


def test_legal_predictive_policing_bias(mod):
    """
    SCENARIO 8: Legal/Justice — Predictive policing bias incident.

    Recidivism prediction tool with documented racial bias,
    opaque decision-making, and no human oversight mechanism.
    """
    header("SCENARIO 8 [Legal/Justice] — Predictive Policing Bias Incident")
    print("  System: Recidivism prediction AI with documented racial bias,")
    print("          black-box decisions, no human override mechanism.")
    print()

    ai = [
        3,3,4,           # MR
        2,3,2,           # DS
        1,1,1,1,         # EI — all Critical (bias, opacity, accountability, societal)
        3,2,1,2,         # DC — financial + operational impact
        3,3,3,3,         # AD
        3,3,3,           # AA
        3,3,3,3,         # LL
        2,2,2,1,1,       # GV — human oversight + ethics Critical
        3,3,2,3,3,3,3,3,2,  # CS
    ]
    assert len(ai) == 39

    inp = scenario(
        industry    = "6",
        base_opts   = ("2","1","2","1","2"),
        ai_scores   = ai,
        mc          = "2",
        impact_opts = ("3","3","3","5"),             # Critical societal impact
        temporal    = TM("2","3","3"),               # PoC/Workaround/Confirmed
        env_req     = ER("X","X","X","3"),           # High societal requirement
        mitigation  = "3",
    )
    score, env, _ = run_scenario(mod, inp)
    print(f"  AIVSS Score  : {score:.2f}  [{severity_label(score)}]")
    print(f"  Env Score    : {env:.2f}")
    print()
    print("  Key risk drivers: EI all Critical (bias, opacity, accountability,")
    print("  societal impact), GV (no human oversight), Critical SI requirement.")
    print("  Remediation priority: bias audit, explainability mandate,")
    print("  human-in-the-loop review, EU AI Act High-Risk compliance.")


def test_government_benefits_fraud_failure(mod):
    """
    SCENARIO 9: Government — Benefits fraud detection AI failure.

    Automated benefits denial system incorrectly flagging legitimate
    claimants, with weak audit trail and governance gaps.
    """
    header("SCENARIO 9 [Government] — Benefits Fraud Detection AI Failure")
    print("  System: Automated benefits eligibility/fraud detection AI,")
    print("          incorrectly denying legitimate claims, weak audit trail.")
    print()

    ai = [
        3,3,3,           # MR
        2,2,3,           # DS
        1,2,1,1,         # EI — bias + accountability + societal Critical
        3,3,2,2,         # DC
        3,3,3,3,         # AD
        3,3,3,           # AA
        3,3,3,3,         # LL
        2,1,2,1,1,       # GV — auditing + human oversight + ethics Critical
        3,3,3,3,3,3,3,3,2,  # CS
    ]
    assert len(ai) == 39

    inp = scenario(
        industry    = "7",
        base_opts   = ("2","2","2","1","1"),
        ai_scores   = ai,
        mc          = "2",
        impact_opts = ("3","3","2","5"),             # Critical societal impact
        temporal    = TM("2","3","2"),
        mitigation  = "3",
    )
    score, env, _ = run_scenario(mod, inp)
    print(f"  AIVSS Score  : {score:.2f}  [{severity_label(score)}]")
    print(f"  Env Score    : {env:.2f}")
    print()
    print("  Key risk drivers: EI (bias + societal Critical), GV (audit +")
    print("  oversight Critical), Critical societal impact score.")
    print("  Remediation priority: human review mandate, explainability,")
    print("  FedRAMP compliance, Privacy Act audit trail.")


def test_v4_vs_v3_comparison(mod):
    """
    SCENARIO 10: V4 vs V3 — impact of additional metrics and corrections.

    Same vulnerability assessed with V3 inputs (5 AI metrics, old temporal
    values, no sub-categories) vs V4 (9 AI metrics, corrected values,
    sub-category averaging). Shows where V3 under- or over-estimates.
    """
    header("SCENARIO 10: V4 vs V3 — Score Comparison")
    print("  Same vulnerability profile scored with V3 and V4 methodologies.")
    print()

    # Replicate V3 approach: 5 AI metrics at Medium, simple temporal
    # V3 formula: (0.30*base + 0.50*ai5 + 0.20*impact) * temporal * mitigation
    base_val = 0.85 * 0.77 * 0.85 * 0.85 * 1.0     # Network/Low/None/None/Unchanged
    ai5 = 0.60 ** 5                                   # 5 metrics at Medium (0.60)
    impact_val = (0.56 + 0.56 + 0.56 + 0.56) / 4    # V3 Medium = 0.56
    temporal_v3 = (0.91 + 0.87 + 0.96) / 3           # V3 temporal values
    v3_score = min(10.0, (0.30*base_val + 0.50*ai5 + 0.20*impact_val) * temporal_v3 * 1.0)

    # V4: all 9 AI metrics at Medium (0.50), corrected temporal, corrected Medium=0.55
    ai9 = 0.50 ** 9 * 1.0
    impact_v4 = (0.55 + 0.55 + 0.55 + 0.55) / 4    # V4 Medium = 0.55
    temporal_v4 = (0.90 + 0.95 + 1.00) / 3           # V4 corrected temporal
    v4_manual = min(10.0, (0.30*base_val + 0.50*ai9 + 0.20*impact_v4) * temporal_v4 * 1.0)

    # Also run actual V4 calculator
    inp = scenario("1", ("1","1","1","1","1"), [3]*39, "1",
                   ("3","3","3","3"), temporal=TM("2","1","3"), mitigation="1")
    v4_calc, _, _ = run_scenario(mod, inp)

    print(f"  {'Method':<40}  {'Score':>6}  Notes")
    print(f"  {'-'*40}  {'-'*6}  {'-'*30}")
    print(f"  {'V3 formula (5 metrics, old values)':<40}  {v3_score:>6.4f}  Unproven=0.91, OfficialFix=0.87")
    print(f"  {'V4 manual (9 metrics, corrected)':<40}  {v4_manual:>6.4f}  Corrected temporal & Medium=0.55")
    print(f"  {'V4 calculator (sub-category avg)':<40}  {v4_calc:>6.4f}  Full sub-category scoring")
    print()
    print(f"  V3 → V4 delta (manual): {v4_manual - v3_score:+.4f}")
    print()

    print("  Key differences:")
    print(f"  - AI score: V3 used 0.60^5={0.60**5:.4f}  V4 uses 0.50^9={0.50**9:.6f}")
    print(f"    (V4's 9-metric product is smaller — more metrics penalise equally)")
    print(f"  - Temporal: V3 Unproven=0.91/OfficialFix=0.87 → V4 0.90/0.95 (corrected)")
    print(f"  - Impact Medium: V3=0.56 → V4=0.55 (spec-correct)")
    print(f"  - V4 base weight unchanged (0.30) so base contribution identical")


# ---------------------------------------------------------------------------
# Summary table
# ---------------------------------------------------------------------------

def print_summary(results):
    header("SUMMARY — All Scenarios")
    print(f"  {'#':<4} {'Scenario':<48} {'Score':>6}  Severity")
    print(f"  {'-'*4} {'-'*48} {'-'*6}  {'-'*8}")
    for num, name, score in results:
        print(f"  {num:<4} {name:<48} {score:>6.2f}  {severity_label(score)}")
    print()
    print("  Score scale: None=0.0 | Low=0.1-3.9 | Medium=4.0-6.9 |")
    print("               High=7.0-8.9 | Critical=9.0-10.0")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print(SEP)
    print("  AIVSS V4 — Test Cases & Demonstration Suite")
    print("  Author: BSec (Bhasker) — https://www.linkedin.com/in/bhaskerkpatel/")
    print(SEP)

    mod = load_v4()
    summary = []

    def capture(num, name, fn):
        fn(mod)
        # Re-run silently to get score for summary
        return num, name

    # Run all scenarios
    test_cross_industry_same_vulnerability(mod)
    test_subcategory_hidden_risk(mod)
    test_severity_progression(mod)
    test_financial_biased_credit_scoring(mod)
    test_healthcare_diagnostic_breach(mod)
    test_critical_infra_grid_attack(mod)
    test_automotive_av_evasion(mod)
    test_legal_predictive_policing_bias(mod)
    test_government_benefits_fraud_failure(mod)
    test_v4_vs_v3_comparison(mod)

    # Collect scores for summary by re-running silently
    silent_runs = [
        ("S1", "Cross-industry (General)",
         scenario("1",("1","1","1","1","1"),[3]*39,"1",("4","4","3","3"),TM("3","4","3"),mitigation="2")),
        ("S4", "Financial — Biased credit scoring LLM",
         scenario("2",("1","1","1","1","1"),
                  [3,4,4,2,2,3,1,2,2,2,4,1,2,3,3,4,4,4,2,2,3,3,3,4,4,1,3,3,2,3,3,3,3,3,3,3,3,3,3],
                  "3",("4","3","2","4"),TM("2","4","3"),mitigation="2")),
        ("S5", "Healthcare — Diagnostic AI breach",
         scenario("3",("2","1","2","1","2"),
                  [2,3,3,1,2,2,2,2,3,3,1,2,2,2,3,4,3,3,2,3,3,3,3,2,3,3,3,3,2,3,3,2,1,1,3,2,2,3,3,2],
                  "3",("5","4","3","4"),TM("3","4","3"),ER("X","X","X","3"),mitigation="2")),
        ("S6", "Critical Infra — Power grid attack",
         scenario("4",("1","1","1","1","2"),
                  [1,2,2,3,2,3,3,3,4,2,1,2,3,1,2,3,2,2,1,2,2,2,2,2,2,2,2,3,3,1,2,3,3,2,2,3,2,2],
                  "2",("4","5","5","5"),TM("3","4","3"),ER("3","3","3","3"),env_mult="3",mitigation="3")),
        ("S7", "Automotive — AV perception evasion",
         scenario("5",("3","1","1","1","2"),
                  [1,1,3,3,2,3,3,2,3,3,1,3,2,1,3,2,1,2,2,3,3,3,3,2,3,3,3,2,1,3,3,3,1,3,3,3,3,3,3],
                  "3",("3","4","4","5"),TM("3","4","3"),ER("X","3","3","3"),mitigation="3")),
        ("S8", "Legal — Predictive policing bias",
         scenario("6",("2","1","2","1","2"),
                  [3,3,4,2,3,2,1,1,1,1,3,2,1,2,3,3,3,3,3,3,3,3,3,3,3,2,1,2,1,1,3,3,2,3,3,3,3,3,2],
                  "2",("3","3","3","5"),TM("2","3","3"),ER("X","X","X","3"),mitigation="3")),
        ("S9", "Government — Benefits AI failure",
         scenario("7",("2","2","2","1","1"),
                  [3,3,3,2,2,3,1,2,1,1,3,3,2,2,3,3,3,3,3,3,3,3,3,3,3,2,1,2,1,1,3,3,3,3,3,3,3,3,2],
                  "2",("3","3","2","5"),TM("2","3","2"),mitigation="3")),
    ]

    print()
    scores_for_summary = []
    for sid, sname, sinp in silent_runs:
        s, _, _ = run_scenario(mod, sinp)
        scores_for_summary.append((sid, sname, s))

    print_summary(scores_for_summary)

    print(SEP)
    print("  All scenarios completed successfully.")
    print(f"  Calculator: aivss_calculatorV4.py")
    print(f"  Author    : BSec (Bhasker) — https://www.linkedin.com/in/bhaskerkpatel/")
    print(SEP)
