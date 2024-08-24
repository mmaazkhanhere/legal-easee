from langchain_ibm import WatsonxLLM

def review_contract(contract_text, watsonx_llm):
    """
    Reviews the given contract text to identify key clauses and potential issues.
    
    Parameters:
        contract_text (str): The contract text to review.
        watsonx_llm (WatsonxLLM): The initialized WatsonxLLM instance.

    Returns:
        str: A summary of key clauses and potential issues in the contract.
    """
    review_template = f"""
    As a legal expert, review the following contract for key clauses and potential issues:

    {contract_text}

    Provide a summary of the key clauses and any potential legal issues.
    """

    # Use the WatsonxLLM to analyze the contract text
    review_summary = watsonx_llm.invoke(review_template)
    return review_summary
