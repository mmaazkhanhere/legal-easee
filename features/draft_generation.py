import streamlit as st
from langchain_ibm import WatsonxLLM

def draft_contract(url, project_id, parameters, contract_type, party_one, party_two, contract_terms):

    watsonx_llm = WatsonxLLM(
        model_id="ibm/granite-13b-chat-v2",
        url=url,
        project_id=project_id,
        params=parameters,
    )

    template = f"""
    You are a legal expert generating a {contract_type} contract. Below are the details:

    - Party One: {party_one}
    - Party Two: {party_two}
    - Key Terms: {contract_terms}

    Please draft a comprehensive {contract_type} contract based on the provided details.
    """
    response = watsonx_llm.invoke(template)

    return response

