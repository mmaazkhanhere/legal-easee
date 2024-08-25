from langchain_ibm import WatsonxLLM 

def review_contract(url, project_id, max_tokens, contract_text):

    parameters = {
    "decoding_method": "sample",
    "max_new_tokens": max_tokens,
    "temperature": 0.7,
    "top_k": 50,
    "top_p": 0.9,
    }

    watsonx_llm = WatsonxLLM(
            model_id="ibm/granite-13b-chat-v2",
            url=url,
            project_id=project_id,
            params=parameters,
    )

    """
    Reviews the uploaded contract text to identify key clauses and potential issues.

    Parameters:
        contract_text (str): The full text of the contract to review.
        watsonx_llm (WatsonxLLM): The initialized WatsonxLLM instance.

    Returns:
        str: A comprehensive summary highlighting the key clauses and identifying any potential legal issues within the contract.
    """

    review_template = f"""
    You are a legal expert tasked with reviewing the following contract to identify its key clauses and any potential legal issues:

    Contract Text:
    {contract_text}

    Instructions:
    1. Carefully analyze the contract text to identify all key clauses, including but not limited to:
    - Parties Involved
    - Payment Terms
    - Confidentiality
    - Termination
    - Governing Law
    - Dispute Resolution
    - Liability and Indemnification
    2. For each key clause, provide a brief summary that explains its purpose and relevance in the context of the contract.
    3. Identify any potential legal issues, ambiguities, or areas of concern, including:
    - Inconsistent or unclear language
    - Missing or incomplete clauses
    - Unbalanced terms that may favor one party disproportionately
    - Any clauses that may not comply with relevant laws or regulations
    4. Offer recommendations for addressing the identified issues, suggesting revisions or additional clauses if necessary.
    5. Structure the summary in a clear and organized format, with sections dedicated to key clauses, potential issues, and recommendations.

    Deliver a detailed and professional summary that is ready for legal review.
    """


    # Use the WatsonxLLM to analyze the contract text
    review_summary = watsonx_llm.invoke(review_template)
    return review_summary
