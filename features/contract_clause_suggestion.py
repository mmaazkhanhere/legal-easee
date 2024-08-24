
def suggest_clauses(contract_text, watsonx_llm):
    """
    Suggests additional clauses for the given contract based on its context and identified needs.

    Parameters:
        contract_text (str): The current text of the contract for which to suggest additional clauses.
        watsonx_llm (WatsonxLLM): The initialized WatsonxLLM instance.

    Returns:
        str: A list of suggested clauses, each with a brief explanation of its relevance and importance.
    """

    suggestion_template = f"""
    You are a legal expert tasked with reviewing the following contract to identify any gaps and suggest additional clauses that may be necessary or beneficial:

    Contract Text:
    {contract_text}

    Instructions:
    1. Carefully review the provided contract text to understand its context, purpose, and key terms.
    2. Identify any areas where the contract may be lacking necessary clauses or where additional clauses could strengthen the agreement. Consider the following aspects:
    - Legal compliance based on jurisdiction
    - Protection of parties' rights and obligations
    - Risk mitigation and dispute resolution
    - Confidentiality, liability, and indemnification
    - Industry-specific requirements
    3. Before recommending each clause, provide a brief reasoning for its necessity, focusing on:
    - Identified gaps or vulnerabilities in the current contract
    - Potential legal risks or ambiguities that the clause would address
    - Enhancements to the clarity, enforceability, or balance of the contract
    4. Suggest each additional clause with a clear and concise explanation of its purpose and the benefits it would bring to the contract.

    Deliver a well-reasoned list of recommended clauses, ensuring that each suggestion is relevant and adds value to the contract.
    """


    # Use the WatsonxLLM to generate clause suggestions
    suggested_clauses = watsonx_llm.invoke(suggestion_template)
    return suggested_clauses
