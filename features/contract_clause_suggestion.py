from langchain_ibm import WatsonxLLM

def suggest_clauses(contract_text, watsonx_llm):
    """
    Suggests appropriate clauses for the given contract based on its context.
    
    Parameters:
        contract_text (str): The current contract text for which to suggest clauses.
        watsonx_llm (WatsonxLLM): The initialized WatsonxLLM instance.

    Returns:
        str: Suggested clauses to include in the contract.
    """
    suggestion_template = f"""
    You are a legal expert. Based on the following contract text, suggest any additional clauses that may be relevant:

    {contract_text}

    Provide a list of suggested clauses with a brief explanation for each.
    """

    # Use the WatsonxLLM to generate clause suggestions
    suggested_clauses = watsonx_llm.invoke(suggestion_template)
    return suggested_clauses
