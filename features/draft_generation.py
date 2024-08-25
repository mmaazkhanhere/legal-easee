from langchain_ibm import WatsonxLLM

def draft_contract(url, project_id, contract_type, party_one, party_two, contract_terms, country):

    """
    Drafts a legal contract based on the specified type, parties involved, contract terms, and country-specific legal requirements using IBM's WatsonxLLM.

    This function leverages the WatsonxLLM model to create a comprehensive contract tailored to the given details. The contract is drafted in accordance with the legal standards and practices of the specified country, ensuring that all necessary clauses and provisions are included.

    Parameters:
        url (str): The API endpoint URL to access the WatsonxLLM service.
        project_id (str): The project identifier for the WatsonxLLM instance.
        contract_type (str): The type of contract to be drafted (e.g., Employment Agreement, Lease Contract).
        party_one (str): The name of the first party involved in the contract.
        party_two (str): The name of the second party involved in the contract.
        contract_terms (str): A description of the key terms and conditions to be included in the contract.
        country (str): The country in which the contract will be executed, to ensure compliance with local laws and regulations.

    Returns:
        str: A fully drafted contract that includes all relevant clauses, structured in a clear and legally sound format, ready for review and execution by both parties.
    """

    parameters = {
        "decoding_method": "sample",
        "max_new_tokens": 800,
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


    template = f"""
    
    You are a legal expert tasked with drafting a {contract_type} contract that adheres to the legal standards and practices of {country}. Below are the details to be included in the contract:

    - Party One: {party_one}
    - Party Two: {party_two}
    - Key Terms: {contract_terms}

    Instructions:
    1. Draft a comprehensive {contract_type} contract based on the provided details, ensuring that it conforms to the legal requirements and customary practices of {country}.
    2. Ensure that all necessary clauses and provisions specific to {country} are included, such as governing law, dispute resolution, and any mandatory legal disclosures.
    3. Structure the contract in a clear, logical format, including sections for definitions, obligations, terms, conditions, and signatures.
    4. Use precise and legally sound language suitable for a formal legal document.

    Deliver a complete and professional contract ready for review and execution by both parties.
    """

    response = watsonx_llm.invoke(template)

    return response