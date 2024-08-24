
def compare_documents(original_contract, new_contract, watsonx_llm):
    """
    Compares two versions of a contract and provides a detailed summary of the differences.

    Parameters:
        original_contract (str): The original contract text.
        new_contract (str): The updated contract text.
        watsonx_llm (WatsonxLLM): The initialized WatsonxLLM instance.

    Returns:
        str: A comprehensive summary that highlights and explains the differences between the two contract versions.
    """

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
