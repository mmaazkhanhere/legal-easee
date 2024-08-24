from dotenv import load_dotenv
import os
import streamlit as st
from langchain_ibm import WatsonxLLM

from features.draft_generation import draft_contract

from features.draft_generation import draft_contract

# from helpers.pdf_conversion import save_to_pdf

# Load environment variables
load_dotenv()

if 'operation' not in st.session_state:
        st.session_state.operation = ''
        st.session_state.operation = ''

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

# Initialize the WatsonxLLM with the specific model
watsonx_llm = WatsonxLLM(
    model_id="ibm/granite-13b-chat-v2",
    url=ibm_url,
    project_id=ibm_project_id,
    params=parameters,
)

# Streamlit UI setup
st.title('AI Contract Assistant')
st.text('Generate a standard legal contract based on your input')

sidebar = st.sidebar
st.sidebar.header('Select your operation')

contract_drafting = sidebar.button('Contract Drafting')

if contract_drafting:
    generated_contract = draft_contract(ibm_url, ibm_project_id, parameters)
    st.write(generated_contract)

    # pdf_file =  save_to_pdf(generated_contract)
    # st.download_button(label="Download Contract", data=pdf_file, file_name="contract.pdf", mime="application/pdf")
    generated_contract = draft_contract(ibm_url, ibm_project_id, parameters)
    st.write(generated_contract)

    # pdf_file =  save_to_pdf(generated_contract)
    # st.download_button(label="Download Contract", data=pdf_file, file_name="contract.pdf", mime="application/pdf")
