from langchain_ibm import WatsonxLLM 

def monitor_compliance(url, project_id, max_tokens, contract_text):

    """
    Summarizes and evaluates compliance with the terms of a specified contract using IBM's WatsonxLLM.

    This function utilizes the WatsonxLLM model to review a given contract's text and assess compliance with its terms and conditions. The model generates a detailed summary indicating areas of full compliance, partial compliance, and any breaches or deviations, along with recommendations for rectification.

    Parameters:
        url (str): The API endpoint URL to access the WatsonxLLM service.
        project_id (str): The project identifier for the WatsonxLLM instance.
        max_tokens (int): The maximum number of tokens to generate in the compliance summary.
        contract_text (str): The full text of the contract to be analyzed for compliance.

    Returns:
        str: A detailed summary that includes:
            - An overview of fully compliant areas.
            - Details of any partial compliance, with recommendations for addressing concerns.
            - Identification of any non-compliance, specifying breached clauses and potential legal implications.
            - Additional observations or recommendations to ensure full compliance.

    """

    # Define parameters for generating suggestions using WatsonLLM
    parameters = {
        "decoding_method": "sample",
        "max_new_tokens": max_tokens,
        "temperature": 0.7,
        "top_k": 50,
        "top_p": 0.9,
    }

    # Initialize the WatsonLLM model with the specified parameters
    watsonx_llm = WatsonxLLM(
            model_id="ibm/granite-13b-chat-v2",
            url=url,
            project_id=project_id,
            params=parameters,
    )

    # Template for instructing the model to generate suggestions.

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
