from langchain_ibm import WatsonxLLM 

def suggest_clauses(url, project_id, max_tokens, contract_text):
    """
    Suggests additional clauses for a given contract based on its context and identified needs using IBM's WatsonxLLM.


    Parameters:
        url (str): The API endpoint URL to access the WatsonxLLM service.
        project_id (str): The project identifier for the WatsonxLLM instance.
        max_tokens (int): The maximum number of tokens to generate in the suggested clauses.
        contract_text (str): The current text of the contract for which additional clauses are needed.

    Returns:
        str: A list of suggested clauses, each accompanied by a brief explanation of its relevance and importance to the contract.
    """

    # Definig the parameters for generating suggestions using WatsonLLM

    parameters = {
        "decoding_method": "sample",
        "max_new_tokens": max_tokens,
        "temperature": 0.7,
        "top_k": 50,
        "top_p": 0.9,
    }

    # Initialize the WatsonxLLM instance with the specified parameters

    watsonx_llm = WatsonxLLM(
            model_id="ibm/granite-13b-chat-v2",
            url=url,
            project_id=project_id,
            params=parameters,
    )

    # system message for the model to define its persona and what it is expected to do
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
