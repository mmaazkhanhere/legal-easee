from langchain_ibm import WatsonxLLM 

def categorize_document(url, project_id, max_tokens, document_text):
    """
    Categorizes a legal document based on its content, structure, and key terms using IBM's WatsonxLLM.

    This function utilizes the WatsonxLLM model to analyze a legal document and determine its specific type (e.g., Non-Disclosure Agreement, Employment Agreement, Lease Contract). The function provides a clear and concise explanation of the categorization, highlighting the features or clauses that led to the determination.

    Parameters:
        url (str): The API endpoint URL to access the WatsonxLLM service.
        project_id (str): The project identifier for the WatsonxLLM instance.
        max_tokens (int): The maximum number of tokens to generate in the categorization output.
        document_text (str): The text of the document to be categorized.

    Returns:
        str: A precise categorization of the document type, along with an explanation that supports the determination. The explanation includes an analysis of the content, structure, and key terms, as well as any nuances or specific elements that distinguish this document from similar types.

    """

    # define the parameters for generating suggestions
    parameters = {
    "decoding_method": "sample",
    "max_new_tokens": max_tokens,
    "temperature": 0.7,
    "top_k": 50,
    "top_p": 0.9,
    }

    # Initialize the WatsonLLM model with the specified parameters
    watsonx_llm = WatsonxLLM(
            model_id="ibm/granite-13b-chat-v2",
            url=url,
            project_id=project_id,
            params=parameters,
    )

    # system message that defines the persona for the AI and gives intruction on how to act
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
