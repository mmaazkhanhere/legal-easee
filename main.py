from dotenv import load_dotenv
import os
import streamlit as st

from features.draft_generation import draft_contract
from helper_functions.pdf_conversion import save_to_pdf

# Load environment variables
load_dotenv()

# Retrieve IBM API credentials from environment variables
ibm_key = os.environ["WATSONX_APIKEY"]
ibm_project_id = os.environ.get('PROJECT_ID')
ibm_url = os.environ.get('WATSONX_URL')

# Set parameters for the AI model
parameters = {
    "decoding_method": "sample",
    "max_new_tokens": 800,
    "temperature": 0.7,
    "top_k": 50,
    "top_p": 0.9,
}

# Streamlit UI setup
st.title('AI Contract Assistant')
st.text('Generate a standard legal contract based on your input')

if 'operation' not in st.session_state:
    st.session_state.operation = None

sidebar = st.sidebar
st.sidebar.header('Select your operation')

if sidebar.button('Contract Drafting'):
    st.session_state.operation = 'contract_drafting'

if st.session_state.operation == 'contract_drafting':
    if 'contract_type' not in st.session_state:
        st.session_state['contract_type'] = 'NDA'

    if 'party_one' not in st.session_state:
        st.session_state['party_one'] = ''

    if 'party_two' not in st.session_state:
        st.session_state['party_two'] = ''

    if 'contract_terms' not in st.session_state:
        st.session_state['contract_terms'] = ''

    if 'generated_contract' not in st.session_state:
        st.session_state['generated_contract'] = ''

    # Form for contract input
    with st.form(key='contract_form'):
        st.session_state['contract_type'] = st.selectbox(
            'Select Contract Type', 
            ['NDA', 'Employment Agreement', 'Service Agreement', 'Sales Agreement'], 
            index=['NDA', 'Employment Agreement', 'Service Agreement', 'Sales Agreement'].index(st.session_state['contract_type'])
        )

        st.session_state['party_one'] = st.text_input('Enter the name of Party One', value=st.session_state['party_one'])
        st.session_state['party_two'] = st.text_input('Enter the name of Party Two', value=st.session_state['party_two'])
        st.session_state['contract_terms'] = st.text_area('Enter the key terms and conditions', value=st.session_state['contract_terms'])

        btn = st.form_submit_button('Draft')
        if btn:
            response = draft_contract(ibm_url, ibm_project_id, parameters)
            st.session_state['generated_contract'] = response  # Store response in session state

    # Display the generated contract and download button outside the form
    if st.session_state['generated_contract']:
        st.write(st.session_state['generated_contract'])

        pdf_file = save_to_pdf(st.session_state['generated_contract'])
        st.download_button(label="Download Contract", data=pdf_file, file_name="contract.pdf", mime="application/pdf")
