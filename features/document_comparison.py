from langchain_ibm import WatsonxLLM 

def compare_documents(url, project_id, max_tokens, original_contract, new_contract):

    """
    Compares two versions of a contract and provides a detailed summary of the differences using IBM's WatsonxLLM.

    This function utilizes the WatsonxLLM model to compare an original contract with an updated version, identifying and analyzing any differences between the two. The function generates a comprehensive summary that highlights minor and significant changes, additions, removals, and their potential impact on the contract's terms and obligations.

    Parameters:
        url (str): The API endpoint URL to access the WatsonxLLM service.
        project_id (str): The project identifier for the WatsonxLLM instance.
        max_tokens (int): The maximum number of tokens to generate in the comparison summary.
        original_contract (str): The original contract text.
        new_contract (str): The updated contract text.

    Returns:
        str: A comprehensive summary highlighting the differences between the original and updated contracts.
    """
        
    # define the parameters for generating suggestions
    parameters = {
    "decoding_method": "sample",
    "max_new_tokens": max_tokens,
    "temperature": 0.7,
    "top_k": 50,
    "top_p": 0.9,
    }

    # Initialize the WatsonLLM with the specified parameters
    watsonx_llm = WatsonxLLM(
            model_id="ibm/granite-13b-chat-v2",
            url=url,
            project_id=project_id,
            params=parameters,
    )

    # Template for instructing the model for generation
    comparison_template = f"""
    You are a legal expert tasked with comparing two versions of a contract to identify and analyze any differences between them.

    Original Contract:
    {original_contract}

    Updated Contract:
    {new_contract}

    Instructions:
    1. Conduct a thorough comparison of the two contracts, focusing on changes in key terms, obligations, conditions, and any other critical provisions.
    2. Highlight each difference found, categorizing them as follows:
    - Minor changes (e.g., wording adjustments with no impact on the meaning)
    - Significant changes (e.g., alterations to terms, obligations, or legal implications)
    - Additions or removals of clauses
    3. For each significant difference, provide a brief analysis of its potential impact on the rights and obligations of the parties involved.
    4. Ensure that the summary is structured clearly, with sections dedicated to minor changes, significant changes, and an overall assessment of how the updated contract differs from the original.
    5. Conclude with any recommendations or considerations for further review, particularly if the changes could lead to legal or practical concerns.

    Deliver a well-organized and concise summary suitable for legal review.
    """


    # Use the WatsonxLLM to compare documents
    differences = watsonx_llm.invoke(comparison_template)
    return differences
