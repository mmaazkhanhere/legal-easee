import streamlit as st
from langchain_ibm import WatsonxLLM

def draft_contract(url, project_id, parameters):

    watsonx_llm = WatsonxLLM(
        model_id="ibm/granite-13b-chat-v2",
        url=url,
        project_id=project_id,
        params=parameters,
    )

    template = f"""
    You are a legal expert generating a {st.session_state['contract_type']} contract. Below are the details:

    - Party One: {st.session_state['party_one']}
    - Party Two: {st.session_state['party_two']}
    - Key Terms: {st.session_state['contract_terms']}

    Please draft a comprehensive {st.session_state['contract_type']} contract based on the provided details.
    """
    response = watsonx_llm.invoke(template)

    return response

