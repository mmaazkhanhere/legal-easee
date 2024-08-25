from langchain_ibm import WatsonxLLM 

def categorize_document(url, project_id, max_tokens, document_text):

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
    Classifies a legal document by its type and provides a brief explanation for the categorization.

    Parameters:
        document_text (str): The text of the legal document to categorize.
        watsonx_llm (WatsonxLLM): The initialized WatsonxLLM instance.

    Returns:
        str: The type of legal document (e.g., NDA, Employment Agreement), along with a brief explanation of the classification.
    """

    categorization_template = f"""
    You are a legal expert tasked with identifying the type of legal document based on the following text:

    Document Text:
    {document_text}

    Instructions:
    1. Analyze the content, structure, and key terms within the document to determine its purpose and function.
    2. Identify the specific type of legal document (e.g., Non-Disclosure Agreement, Employment Agreement, Lease Contract) by considering the nature of the obligations, parties involved, and legal context.
    3. Provide a clear and concise explanation for the categorization, highlighting the features or clauses that led to your determination.
    4. If applicable, mention any nuances or specific elements that distinguish this document from similar types of legal documents.

    Deliver a precise categorization along with a reasoned explanation that supports your determination.
    """

    # Use the WatsonxLLM to categorize the document
    document_type = watsonx_llm.invoke(categorization_template)
    return document_type
