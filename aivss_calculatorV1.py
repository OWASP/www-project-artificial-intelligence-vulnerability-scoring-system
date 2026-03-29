import warnings

warnings.warn(
    "aivss_calculatorV1.py is deprecated and implements only 5 of the 9 required "
    "AI-specific metrics with incorrect weights. Use aivss_calculatorV3.py instead.",
    DeprecationWarning,
    stacklevel=2,
)


def calculate_aivss_score():
    """Calculates the AIVSS score interactively based on user input."""

    # Define the AIVSS parameter values with descriptions for user selection
    av_values = {
        "1": {"value": 0.85, "description": "Network"},
        "2": {"value": 0.62, "description": "Adjacent"},
        "3": {"value": 0.55, "description": "Local"},
        "4": {"value": 0.2, "description": "Physical"},
    }
    ac_values = {
        "1": {"value": 0.77, "description": "Low"},
        "2": {"value": 0.44, "description": "High"},
    }
    pr_values = {
        "1": {"value": 0.85, "description": "None"},
        "2": {"value": 0.62, "description": "Low"},
        "3": {"value": 0.27, "description": "High"},
    }
    ui_values = {
        "1": {"value": 0.85, "description": "None"},
        "2": {"value": 0.62, "description": "Required"},
    }
    s_values = {
        "1": {"value": 1.5, "description": "Changed"},
        "2": {"value": 1.0, "description": "Unchanged"},
    }

    # Get user input for each parameter
    def get_user_input(parameter_name, values):
        print(f"\nSelect {parameter_name}:")
        for key, value in values.items():
            print(f"{key}. {value['description']}")
        choice = input("Enter your choice: ")
        while choice not in values:
            print("Invalid choice. Please try again.")
            choice = input("Enter your choice: ")
        return values[choice]["value"]

    attack_vector = get_user_input("Attack Vector (AV)", av_values)
    attack_complexity = get_user_input("Attack Complexity (AC)", ac_values)
    privileges_required = get_user_input("Privileges Required (PR)", pr_values)
    user_interaction = get_user_input("User Interaction (UI)", ui_values)
    scope = get_user_input("Scope (S)", s_values)

    model_robustness = float(
        input("\nEnter Model Robustness (MR) (0.0 to 1.0): ")
    )
    data_sensitivity = float(input("Enter Data Sensitivity (DS) (0.0 to 1.0): "))
    ethical_impact = float(input("Enter Ethical Impact (EI) (0.0 to 1.0): "))
    decision_criticality = float(
        input("Enter Decision Criticality (DC) (0.0 to 1.0): ")
    )
    adaptability = float(input("Enter Adaptability (AD) (0.0 to 1.0): "))

    confidentiality_impact = float(
        input("\nEnter Confidentiality Impact (C) (0.0 to 1.0): ")
    )
    integrity_impact = float(
        input("\nEnter Integrity Impact (I) (0.0 to 1.0): ")
    )
    availability_impact = float(
        input("\nEnter Availability Impact (A) (0.0 to 1.0): ")
    )
    safety_impact = float(input("\nEnter Safety Impact (SI) (0.0 to 1.0): "))

    # Calculate the base metrics score
    base_metrics = (
        attack_vector
        * attack_complexity
        * privileges_required
        * user_interaction
        * scope
    )
    base_metrics = min(10, base_metrics)  # Cap the base metrics score at 10

    # Calculate the AI-specific metrics score
    ai_specific_metrics = (
        model_robustness
        * data_sensitivity
        * ethical_impact
        * decision_criticality
        * adaptability
    )

    # Calculate the impact metrics score
    impact_metrics = (
        confidentiality_impact
        + integrity_impact
        + availability_impact
        + safety_impact
    ) / 4

    # Calculate the final AIVSS score
    # Note: The weights (w1, w2, w3) and temporal metrics are not included in this
    # example. You can adjust the weights and add temporal metrics as needed.
    w1 = 0.4
    w2 = 0.4
    w3 = 0.2
    aivss_score = (
        w1 * base_metrics + w2 * ai_specific_metrics + w3 * impact_metrics
    )

    return aivss_score


# Example usage
aivss_score = calculate_aivss_score()
print(f"\nThe AIVSS score is: {aivss_score:.2f}")