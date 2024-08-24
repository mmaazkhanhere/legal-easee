from dotenv import load_dotenv
import os
import streamlit as st
from langchain_ibm import WatsonxLLM

# from helpers.pdf_conversion import save_to_pdf

# Load environment variables
load_dotenv()

if 'operation' not in st.session_state:
        st.session_state['operation'] = ''

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

if 

# Streamlit UI setup
st.title('AI Contract Assistant')
st.text('Generate a standard legal contract based on your input')

sidebar = st.sidebar
st.sidebar.header('Select your operation')

contract_drafting = sidebar.button('Contract Drafting')

if contract_drafting:


# User input fields for contract generation
# contract_type = st.selectbox('Select Contract Type', ['NDA', 'Employment Agreement', 'Service Agreement', 'Sales Agreement'])
# party_one = st.text_input('Enter the name of Party One')
# party_two = st.text_input('Enter the name of Party Two')
# contract_terms = st.text_area('Enter the key terms and conditions')

# # Define the template for the contract generation
# template = f"""
# You are a legal expert generating a {contract_type} contract. Below are the details:

# - Party One: {party_one}
# - Party Two: {party_two}
# - Key Terms: {contract_terms}

# Please draft a comprehensive {contract_type} contract based on the provided details.
# """

# # Button to generate the contract
# btn = st.button('Generate Contract')
# if btn:
#     # Generate and display the contract
#     generated_contract = watsonx_llm.invoke(template)
#     pdf_file =  save_to_pdf(generated_contract)
#     st.download_button(label="Download Contract", data=pdf_file, file_name="contract.pdf", mime="application/pdf")
