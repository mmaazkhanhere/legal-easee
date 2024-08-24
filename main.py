from langchain_ibm import WatsonxLLM  # Import WatsonxLLM
from dotenv import load_dotenv
import os
import streamlit as st

from features.draft_generation import draft_contract
from features.contract_clause_suggestion import suggest_clauses
from features.contract_compliance_monitoring import monitor_compliance
from features.contract_review import review_contract
from features.document_comparison import compare_documents
from features.legal_document_categorization import categorize_document  # Import the categorize_document function
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
elif sidebar.button('Contract Clause Suggestion'):
    st.session_state.operation = 'suggest_clauses'
elif sidebar.button('Contract Compliance Monitoring'):
    st.session_state.operation = 'monitor_compliance'
elif sidebar.button('Contract Review'):
    st.session_state.operation = 'review_contract'
elif sidebar.button('Document Comparison'):
    st.session_state.operation = 'compare_documents'
elif sidebar.button('Legal Document Categorization'):
    st.session_state.operation = 'categorize_document'

# Contract Drafting
if st.session_state.operation == 'contract_drafting':
    if 'contract_type' not in st.session_state:
        st.session_state['contract_type'] = 'NDA'

    if 'country' not in st.session_state:
        st.session_state['country'] = 'USA'

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
            ['NDA', 'Employment Agreement', 'Service Agreement', 'Sales Agreement', 'Lease Agreement', 'Partnership Agreement', 'Loan Agreement', 'Franchise Agreement', 'Settlement Agreement', 'Indemnity Agreement', 'Licensing Agreement'], 
            index=['NDA', 'Employment Agreement', 'Service Agreement', 'Sales Agreement', 'Lease Agreement', 'Partnership Agreement', 'Loan Agreement', 'Franchise Agreement', 'Settlement Agreement', 'Indemnity Agreement', 'Licensing Agreement'].index(st.session_state['contract_type'])
        )

        st.session_state['country'] = st.selectbox(
            'Select Country', 
            ['Australia', 'Canada', 'United Arab Emirates','United Kingdom', 'United States'], 
            index=['Australia', 'Canada', 'United Arab Emirates','United Kingdom', 'United States'].index(st.session_state['country'])
        )

        st.session_state['party_one'] = st.text_input('Enter the name of Party One', value=st.session_state['party_one'])
        st.session_state['party_two'] = st.text_input('Enter the name of Party Two', value=st.session_state['party_two'])
        st.session_state['contract_terms'] = st.text_area('Enter the key terms and conditions', value=st.session_state['contract_terms'])

        btn = st.form_submit_button('Draft')
        if btn:
            response = draft_contract(ibm_url, ibm_project_id, parameters, st.session_state['contract_type']  , st.session_state['party_one'] ,  st.session_state['party_two'], st.session_state['contract_terms'])
            st.session_state['generated_contract'] = response  # Store response in session state

    # Display the generated contract and download button outside the form
    if st.session_state['generated_contract']:
        st.write(st.session_state['generated_contract'])

        pdf_file = save_to_pdf(st.session_state['generated_contract'])
        st.download_button(label="Download Contract", data=pdf_file, file_name="contract.pdf", mime="application/pdf")

# Contract Clause Suggestion
elif st.session_state.operation == 'suggest_clauses':
    if 'contract_text' not in st.session_state:
        st.session_state['contract_text'] = ''

    if 'suggested_clauses' not in st.session_state:
        st.session_state['suggested_clauses'] = ''

    # Form for contract clause suggestion input
    with st.form(key='clause_suggestion_form'):
        st.session_state['contract_text'] = st.text_area('Enter the contract text for clause suggestions', value=st.session_state['contract_text'])

        btn = st.form_submit_button('Suggest Clauses')
        if btn:
            # Initialize WatsonxLLM instance
            watsonx_llm = WatsonxLLM(
                model_id="ibm/granite-13b-chat-v2",
                url=ibm_url,
                project_id=ibm_project_id,
                params=parameters,
            )

            response = suggest_clauses(st.session_state['contract_text'], watsonx_llm)
            st.session_state['suggested_clauses'] = response  # Store response in session state

    # Display the suggested clauses
    if st.session_state['suggested_clauses']:
        st.write(st.session_state['suggested_clauses'])

# Contract Compliance Monitoring
elif st.session_state.operation == 'monitor_compliance':
    if 'contract_text' not in st.session_state:
        st.session_state['contract_text'] = ''

    if 'compliance_summary' not in st.session_state:
        st.session_state['compliance_summary'] = ''

    # Form for contract compliance monitoring input
    with st.form(key='compliance_monitoring_form'):
        st.session_state['contract_text'] = st.text_area('Enter the contract text for compliance monitoring', value=st.session_state['contract_text'])

        btn = st.form_submit_button('Check Compliance')
        if btn:
            # Initialize WatsonxLLM instance
            watsonx_llm = WatsonxLLM(
                model_id="ibm/granite-13b-chat-v2",
                url=ibm_url,
                project_id=ibm_project_id,
                params=parameters,
            )

            response = monitor_compliance(st.session_state['contract_text'], watsonx_llm)
            st.session_state['compliance_summary'] = response  # Store response in session state

    # Display the compliance summary
    if st.session_state['compliance_summary']:
        st.write(st.session_state['compliance_summary'])

# Contract Review
elif st.session_state.operation == 'review_contract':
    if 'contract_text' not in st.session_state:
        st.session_state['contract_text'] = ''

    if 'review_summary' not in st.session_state:
        st.session_state['review_summary'] = ''

    # Form for contract review input
    with st.form(key='review_contract_form'):
        st.session_state['contract_text'] = st.text_area('Enter the contract text for review', value=st.session_state['contract_text'])

        btn = st.form_submit_button('Review Contract')
        if btn:
            # Initialize WatsonxLLM instance
            watsonx_llm = WatsonxLLM(
                model_id="ibm/granite-13b-chat-v2",
                url=ibm_url,
                project_id=ibm_project_id,
                params=parameters,
            )

            response = review_contract(st.session_state['contract_text'], watsonx_llm)
            st.session_state['review_summary'] = response  # Store response in session state

    # Display the review summary
    if st.session_state['review_summary']:
        st.write(st.session_state['review_summary'])

# Document Comparison
elif st.session_state.operation == 'compare_documents':
    if 'original_contract' not in st.session_state:
        st.session_state['original_contract'] = ''

    if 'new_contract' not in st.session_state:
        st.session_state['new_contract'] = ''

    if 'comparison_summary' not in st.session_state:
        st.session_state['comparison_summary'] = ''

    # Form for document comparison input
    with st.form(key='document_comparison_form'):
        st.session_state['original_contract'] = st.text_area('Enter the original contract text', value=st.session_state['original_contract'])
        st.session_state['new_contract'] = st.text_area('Enter the updated contract text', value=st.session_state['new_contract'])

        btn = st.form_submit_button('Compare Documents')
        if btn:
            # Initialize WatsonxLLM instance
            watsonx_llm = WatsonxLLM(
                model_id="ibm/granite-13b-chat-v2",
                url=ibm_url,
                project_id=ibm_project_id,
                params=parameters,
            )

            response = compare_documents(st.session_state['original_contract'], st.session_state['new_contract'], watsonx_llm)
            st.session_state['comparison_summary'] = response  # Store response in session state

    # Display the comparison summary
    if st.session_state['comparison_summary']:
        st.write(st.session_state['comparison_summary'])

# Legal Document Categorization
elif st.session_state.operation == 'categorize_document':
    if 'document_text' not in st.session_state:
        st.session_state['document_text'] = ''

    if 'document_type' not in st.session_state:
        st.session_state['document_type'] = ''

    # Form for legal document categorization input
    with st.form(key='document_categorization_form'):
        st.session_state['document_text'] = st.text_area('Enter the document text to categorize', value=st.session_state['document_text'])

        btn = st.form_submit_button('Categorize Document')
        if btn:
            # Initialize WatsonxLLM instance
            watsonx_llm = WatsonxLLM(
                model_id="ibm/granite-13b-chat-v2",
                url=ibm_url,
                project_id=ibm_project_id,
                params=parameters,
            )

            response = categorize_document(st.session_state['document_text'], watsonx_llm)
            st.session_state['document_type'] = response  # Store response in session state

    # Display the document type
    if st.session_state['document_type']:
        st.write(st.session_state['document_type'])
