from langchain_ibm import WatsonxLLM

def monitor_compliance(contract_text, watsonx_llm):
    """
    Summarizes compliance with the terms of a given contract.
    
    Parameters:
        contract_text (str): The contract text to check for compliance.
        watsonx_llm (WatsonxLLM): The initialized WatsonxLLM instance.

    Returns:
        str: A summary of compliance with the contract terms.
    """
    compliance_template = f"""
    As a legal expert, analyze the following contract for compliance with its terms:

    {contract_text}

    Provide a summary of compliance or any breaches found.
    """

    # Use the WatsonxLLM to monitor contract compliance
    compliance_summary = watsonx_llm.invoke(compliance_template)
    return compliance_summary
