from langchain_ibm import WatsonxLLM

def draft_contract(url, project_id, parameters, contract_type, party_one, party_two, contract_terms, country):

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

