
def monitor_compliance(contract_text, watsonx_llm):
    """
    Summarizes and evaluates compliance with the terms of a specified contract.

    Parameters:
        contract_text (str): The full text of the contract to be analyzed.
        watsonx_llm (WatsonxLLM): The initialized WatsonxLLM instance.

    Returns:
        str: A detailed summary indicating areas of compliance, partial compliance, and any breaches or deviations from the contract terms.
    """

    compliance_template = f"""
    As a legal analyst, your task is to review and assess the compliance of the following contract with its specified terms and conditions:

    Contract Text:
    {contract_text}

    Instructions:
    1. Identify and summarize each key term and obligation outlined in the contract.
    2. Evaluate the compliance status of each term:
    - Fully Compliant
    - Partially Compliant (Specify areas of concern)
    - Non-Compliant (Highlight breaches or deviations)
    3. Provide a comprehensive summary that includes:
    - An overview of fully compliant areas.
    - Details of any partial compliance, with recommendations for rectification.
    - A clear identification of any non-compliance, specifying the clauses breached and potential legal implications.
    4. Conclude with any additional observations or recommendations for ensuring full compliance.

    Deliver your analysis in a clear, structured format suitable for legal review.
    """

    # Use the WatsonxLLM to monitor contract compliance
    compliance_summary = watsonx_llm.invoke(compliance_template)
    return compliance_summary
