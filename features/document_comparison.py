from langchain_ibm import WatsonxLLM

def compare_documents(original_contract, new_contract, watsonx_llm):
    """
    Compares two versions of a contract and highlights the differences.
    
    Parameters:
        original_contract (str): The original contract text.
        new_contract (str): The updated contract text.
        watsonx_llm (WatsonxLLM): The initialized WatsonxLLM instance.

    Returns:
        str: A summary highlighting the differences between the two contracts.
    """
    comparison_template = f"""
    As a legal expert, compare the following two versions of a contract and highlight the differences:

    Original Contract:
    {original_contract}

    Updated Contract:
    {new_contract}

    Provide a summary of the differences.
    """

    # Use the WatsonxLLM to compare documents
    differences = watsonx_llm.invoke(comparison_template)
    return differences
