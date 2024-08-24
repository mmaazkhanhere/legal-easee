from langchain_ibm import WatsonxLLM

def categorize_document(document_text, watsonx_llm):
    """
    Categorizes a legal document by its type.
    
    Parameters:
        document_text (str): The document text to categorize.
        watsonx_llm (WatsonxLLM): The initialized WatsonxLLM instance.

    Returns:
        str: The type of legal document (e.g., NDA, Employment Agreement).
    """
    categorization_template = f"""
    You are a legal expert. Based on the following document text, determine the type of legal document it is:

    {document_text}

    Provide the document type with a brief explanation.
    """

    # Use the WatsonxLLM to categorize the document
    document_type = watsonx_llm.invoke(categorization_template)
    return document_type
