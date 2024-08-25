from langchain_ibm import WatsonxLLM 

def review_contract(url, project_id, max_tokens, contract_text):

    """
    Reviews the provided contract text to identify key clauses and potential legal issues using IBM's WatsonxLLM.

    This function utilizes the WatsonxLLM model to analyze the text of a contract, identifying key clauses and any potential legal issues. The function provides a comprehensive summary that highlights the critical components of the contract, identifies any ambiguities or risks, and offers recommendations for improvements.

    Parameters:
        url (str): The API endpoint URL to access the WatsonxLLM service.
        project_id (str): The project identifier for the WatsonxLLM instance.
        max_tokens (int): The maximum number of tokens to generate in the review summary.
        contract_text (str): The full text of the contract to be reviewed.

    Returns:
        str: A detailed summary of the contract

    """

    # Define the parameters for generating suggestions
    parameters = {
    "decoding_method": "sample",
    "max_new_tokens": max_tokens,
    "temperature": 0.7,
    "top_k": 50,
    "top_p": 0.9,
    }

    # Initialize the WatsonLLM model with the specified parameters and project details
    watsonx_llm = WatsonxLLM(
            model_id="ibm/granite-13b-chat-v2",
            url=url,
            project_id=project_id,
            params=parameters,
    )


    # Template for the model that define persona for the model and specify instructions
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
