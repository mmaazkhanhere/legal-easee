import streamlit as st
from langchain_ibm import WatsonxLLM

def draft_contract(url, project_id, parameters):

    watsonx_llm = WatsonxLLM(
        model_id="ibm/granite-13b-chat-v2",
        url=url,
        project_id=project_id,
        params=parameters,
    )

    st.title('Automated Contract Drafting')
    st.text('Generate a standard legal contract based on your input')

    # Initialize session state
    if 'contract_type' not in st.session_state:
        st.session_state['contract_type'] = 'NDA'  # Default to 'NDA'

    if 'party_one' not in st.session_state:
        st.session_state['party_one'] = ''

    if 'party_two' not in st.session_state:
        st.session_state['party_two'] = ''

    if 'contract_terms' not in st.session_state:
        st.session_state['contract_terms'] = ''

    if 'generated_contract' not in st.session_state:
        st.session_state['generated_contract'] = None

    with st.form(key='contract_form'):
        st.session_state['contract_type'] = st.selectbox(
            'Select Contract Type', 
            ['NDA', 'Employment Agreement', 'Service Agreement', 'Sales Agreement'], 
            index=['NDA', 'Employment Agreement', 'Service Agreement', 'Sales Agreement'].index(st.session_state['contract_type'])
        )

        st.session_state['party_one'] = st.text_input('Enter the name of Party One', value=st.session_state['party_one'])
        st.session_state['party_two'] = st.text_input('Enter the name of Party Two', value=st.session_state['party_two'])
        st.session_state['contract_terms'] = st.text_area('Enter the key terms and conditions', value=st.session_state['contract_terms'])

        # Define the template for the contract generation
        template = f"""
            You are a legal expert generating a {st.session_state['contract_type']} contract. Below are the details:

            - Party One: {st.session_state['party_one']}
            - Party Two: {st.session_state['party_two']}
            - Key Terms: {st.session_state['contract_terms']}

            Please draft a comprehensive {st.session_state['contract_type']} contract based on the provided details.
            """

        # Button to generate the contract
        submit_button = st.form_submit_button(label='Generate Contract')
        if submit_button:
            # Generate and display the contract
            st.session_state['generated_contract'] = watsonx_llm.invoke(template)
            return st.session_state['generated_contract']

    if st.session_state['generated_contract']:
        st.write(st.session_state['generated_contract'])
