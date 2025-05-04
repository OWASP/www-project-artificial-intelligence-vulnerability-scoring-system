
# AIVSS Implementation Checklist #

**Phase 1: Preparation**

*   [ ] **1.1 Define Scope:**
    *   [ ] 1.1.1 Identify the AI system(s) to be assessed.
    *   [ ] 1.1.2 Determine the assessment boundaries (e.g., specific components, lifecycle stages).
    *   [ ] 1.1.3 Define the objectives of the assessment (e.g., identify vulnerabilities, improve security posture, compliance).
*   [ ] **1.2 Assemble Team:**
    *   [ ] 1.2.1 Form an assessment team with the necessary expertise:
        *   [ ] AI Security Specialist/Team Lead
        *   [ ] AI Developers/Data Scientists
        *   [ ] Security Engineers
        *   [ ] Compliance/Risk Officer
        *   [ ] Ethical AI Officer/Review Board (if applicable)
    *   [ ] 1.2.2 Define roles and responsibilities for each team member.
*   [ ] **1.3 Gather Information:**
    *   [ ] 1.3.1 Collect documentation on the AI system's architecture, data flows, dependencies, and functionalities.
    *   [ ] 1.3.2 Identify relevant threat models and AI threat taxonomies (see AIVSS Appendix).
    *   [ ] 1.3.3 Gather information on applicable regulations, standards, and ethical guidelines.

**Phase 2: Assessment**

*   [ ] **2.1 Base Metrics Evaluation:**
    *   [ ] 2.1.1 **Attack Vector (AV):** Determine how an attacker could exploit the vulnerability (Network, Adjacent, Local, Physical).
    *   [ ] 2.1.2 **Attack Complexity (AC):** Assess the difficulty of executing the attack (Low or High).
    *   [ ] 2.1.3 **Privileges Required (PR):** Determine the level of access needed (None, Low, High).
    *   [ ] 2.1.4 **User Interaction (UI):** Assess whether user interaction is required for the attack (None or Required).
    *   [ ] 2.1.5 **Scope (S):** Determine if the vulnerability impacts other components (Unchanged or Changed).
    *   [ ] 2.1.6 **Calculate Base Metrics Score** using the formula: `BaseMetrics = min(10, [AV × AC × PR × UI × S] × ScopeMultiplier)`

*   [ ] **2.2 AI-Specific Metrics Evaluation:**
    *   [ ] 2.2.1 **Model Robustness (MR):**
        *   [ ] **Evasion Resistance:** Assess susceptibility to evasion attacks.
        *   [ ] **Gradient Masking/Obfuscation:** Evaluate the use of gradient masking techniques.
        *   [ ] **Robustness Certification:** Determine if robustness testing or certification has been performed.
    *   [ ] 2.2.2 **Data Sensitivity (DS):**
        *   [ ] **Data Confidentiality:** Assess the protection of sensitive data.
        *   [ ] **Data Integrity:** Evaluate data integrity checks and tamper detection.
        *   [ ] **Data Provenance:** Determine the level of data lineage tracking.
    *   [ ] 2.2.3 **Ethical Implications (EI):**
        *   [ ] **Bias and Discrimination:** Assess the risk of biased or discriminatory outcomes.
        *   [ ] **Transparency and Explainability:** Evaluate the transparency of the system's decision-making.
        *   [ ] **Accountability:** Determine the lines of accountability for the system's actions.
        *   [ ] **Societal Impact:** Assess the potential impact on society.
    *   [ ] 2.2.4 **Decision Criticality (DC):**
        *   [ ] **Safety-Critical:** Evaluate if the system is used in safety-critical applications.
        *   [ ] **Financial Impact:** Assess the potential for financial loss.
        *   [ ] **Reputational Damage:** Determine the risk of reputational damage.
        *   [ ] **Operational Disruption:** Evaluate the potential for operational disruption.
    *   [ ] 2.2.5 **Adaptability (AD):**
        *   [ ] **Continuous Monitoring:** Assess monitoring for attacks and anomalies.
        *   [ ] **Retraining Capabilities:** Evaluate the system's ability to be retrained.
        *   [ ] **Threat Intelligence Integration:** Determine if threat intelligence is used.
        *   [ ] **Adversarial Training:** Assess the use of adversarial training techniques.
    *   [ ] 2.2.6 **Adversarial Attack Surface (AA):**
        *   [ ] **Model Inversion:** Evaluate the risk of model inversion attacks.
        *   [ ] **Model Extraction:** Assess the risk of model extraction attacks.
        *   [ ] **Membership Inference:** Determine the risk of membership inference attacks.
    *   [ ] 2.2.7 **Lifecycle Vulnerabilities (LL):**
        *   [ ] **Development:** Assess the security of the development environment.
        *   [ ] **Training:** Evaluate the security of the training environment and data.
        *   [ ] **Deployment:** Determine the security of the deployment environment.
        *   [ ] **Operations:** Assess security monitoring and incident response.
    *   [ ] 2.2.8 **Governance and Validation (GV):**
        *   [ ] **Compliance:** Evaluate compliance with regulations and standards.
        *   [ ] **Auditing:** Determine if regular audits are conducted.
        *   [ ] **Risk Management:** Assess AI-specific risk management processes.
        *   [ ] **Human Oversight:** Evaluate the level of human oversight.
        *   [ ] **Ethical Framework Alignment:** Determine alignment with ethical frameworks.
    *   [ ] 2.2.9 **Cloud Security Alliance LLM Taxonomy (CS):** (Especially relevant for LLMs and cloud deployments)
        *   [ ] **Model Manipulation:** Assess vulnerability to prompt injection and other manipulations.
        *   [ ] **Data Poisoning:** Evaluate the risk of data poisoning attacks.
        *   [ ] **Sensitive Data Disclosure:** Determine the risk of sensitive data leakage.
        *   [ ] **Model Stealing:** Assess the risk of model theft.
        *   [ ] **Failure/Malfunctioning:** Evaluate the system's reliability and fault tolerance.
        *   [ ] **Insecure Supply Chain:** Determine the security of the supply chain.
        *   [ ] **Insecure Apps/Plugins:** Assess the security of third-party integrations.
        *   [ ] **Denial of Service (DoS):** Evaluate vulnerability to DoS attacks.
        *   [ ] **Loss of Governance/Compliance:** Determine the risk of non-compliance.
    *   [ ] 2.2.10 **Assign scores (0.0-1.0) to each sub-category** based on the detailed rubric (higher score = more severe issue).
    *   [ ] 2.2.11 **Determine the Model Complexity Multiplier** (1.0-1.5) based on the complexity of the AI model.
    *   [ ] 2.2.12 **Calculate the AI-Specific Metrics Score:** `AISpecificMetrics = [MR × DS × EI × DC × AD × AA × LL × GV × CS] × ModelComplexityMultiplier`

*   [ ] **2.3 Impact Metrics Evaluation:**
    *   [ ] 2.3.1 **Confidentiality Impact (C):** Assess the impact on data confidentiality (None, Low, Medium, High, Critical).
    *   [ ] 2.3.2 **Integrity Impact (I):** Assess the impact on data and system integrity (None, Low, Medium, High, Critical).
    *   [ ] 2.3.3 **Availability Impact (A):** Assess the impact on system availability (None, Low, Medium, High, Critical).
    *   [ ] 2.3.4 **Societal Impact (SI):** Assess the broader societal impact (None, Low, Medium, High, Critical).
    *   [ ] 2.3.5 **Calculate the Impact Metrics Score:** `ImpactMetrics = (C + I + A + SI) / 4`

*   [ ] **2.4 Temporal Metrics Evaluation:**
    *   [ ] 2.4.1 **Exploitability (E):** Assess the likelihood of the vulnerability being exploited (Not Defined, Unproven, Proof-of-Concept, Functional, High).
    *   [ ] 2.4.2 **Remediation Level (RL):** Determine the availability of a fix (Not Defined, Official Fix, Temporary Fix, Workaround, Unavailable).
    *   [ ] 2.4.3 **Report Confidence (RC):** Assess the confidence in the vulnerability report (Not Defined, Unknown, Reasonable, Confirmed).
    *   [ ] 2.4.4 **Calculate Temporal Metrics Score** using the given values for each subcategory (e.g., average them).

*   [ ] **2.5 Mitigation Effectiveness Evaluation:**
    *   [ ] 2.5.1 Assess the effectiveness of implemented mitigations in reducing the identified vulnerabilities.
    *   [ ] 2.5.2 Assign a **Mitigation Multiplier** score: 1.0 (Strong Mitigation), 1.2 (Moderate Mitigation), 1.5 (Weak/No Mitigation).

**Phase 3: Scoring and Reporting**

*   [ ] **3.1 Calculate AIVSS Score:**
    *   [ ] 3.1.1 Use the formula: `AIVSS_Score = [(w₁ × BaseMetrics) + (w₂ × AISpecificMetrics) + (w₃ × ImpactMetrics)] × TemporalMetrics × MitigationMultiplier`
    *   [ ] 3.1.2 Use the suggested weights (w₁ = 0.3, w₂ = 0.5, w₃ = 0.2) or adjust them based on your organization's risk profile.
*   [ ] **3.2 Determine Risk Category:**
    *   [ ] **Critical:** 9.0 - 10.0
    *   [ ] **High:** 7.0 - 8.9
    *   [ ] **Medium:** 4.0 - 6.9
    *   [ ] **Low:** 0.1 - 3.9
    *   [ ] **None:** 0.0
*   [ ] **3.3 Generate Report:**
    *   [ ] 3.3.1 Document the assessment findings, including the AIVSS score, risk category, and detailed scores for each metric and sub-category.
    *   [ ] 3.3.2 Provide justification for the assigned scores, referencing the scoring rubric and evidence gathered.
    *   [ ] 3.3.3 Analyze the key vulnerabilities and their potential impact.
    *   [ ] 3.3.4 Recommend mitigation strategies, prioritized based on the severity of the vulnerabilities.
    *   [ ] 3.3.5 Include an executive summary for management and technical details for relevant teams.

**Phase 4: Remediation and Follow-up**

*   [ ] **4.1 Develop Remediation Plan:**
    *   [ ] 4.1.1 Prioritize vulnerabilities based on their AIVSS score and risk category.
    *   [ ] 4.1.2 Assign responsibility for implementing mitigations.
    *   [ ] 4.1.3 Define timelines for remediation.
*   [ ] **4.2 Implement Mitigations:**
    *   [ ] 4.2.1 Implement the recommended mitigation strategies.
    *   [ ] 4.2.2 Verify the effectiveness of the mitigations.
*   [ ] **4.3 Re-assess:**
    *   [ ] 4.3.1 Conduct a follow-up assessment to ensure that vulnerabilities have been adequately addressed.
    *   [ ] 4.3.2 Update the AIVSS score and report as needed.
*   [ ] **4.4 Continuous Monitoring:**
    *   [ ] 4.4.1 Implement continuous monitoring of the AI system for new vulnerabilities and emerging threats.
    *   [ ] 4.4.2 Regularly review and update the AIVSS assessment to reflect changes in the system, the threat landscape, and the organization's risk profile.

**Appendix: AI Threat Taxonomies**
https://github.com/kenhuangus/Artificial-Intelligence-Vulnerability-Scoring-System-AIVSS/blob/main/AI%20Threat%20Taxonomies.md


**Note:** This checklist is a starting point and should be adapted to the specific needs and context of your organization and the AI system being assessed. It's crucial to involve individuals with the right expertise and to document the assessment process thoroughly. Remember that securing AI systems is an ongoing process that requires continuous monitoring, adaptation, and improvement.
