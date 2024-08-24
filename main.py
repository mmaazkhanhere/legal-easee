from dotenv import load_dotenv
import solcx
import os
import streamlit as st
from web3 import Web3
from solcx import compile_source
from langchain_ibm import WatsonxLLM 

from features.draft_generation import draft_contract
from helper_functions.pdf_conversion import save_to_pdf
from features.contract_clause_suggestion import suggest_clauses
from features.contract_compliance_monitoring import monitor_compliance
from features.contract_review import review_contract
from features.document_comparison import compare_documents
from features.legal_document_categorization import categorize_document
# Load environment variables
load_dotenv()

# Retrieve IBM API credentials from environment variables
ibm_key = os.environ["WATSONX_APIKEY"]
ibm_project_id = os.environ.get('PROJECT_ID')
ibm_url = os.environ.get('WATSONX_URL')

try:
    solcx.set_solc_version('0.8.0')
except solcx.exceptions.SolcNotInstalled:
    st.write("Solc is not installed. Installing Solc 0.8.0...")
    solcx.install_solc('0.8.0')
    solcx.set_solc_version('0.8.0')

# Ethereum blockchain configuration
eth_provider = os.environ.get("WEB3_PROVIDER")
private_key = os.environ.get("PRIVATE_KEY")
account_address = os.environ.get("DEFAULT_ACCOUNT")

w3 = Web3(Web3.HTTPProvider(eth_provider))

# Solidity source code
contract_source_code = '''
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ContractStorage {
    string public contractContent;

    constructor(string memory _content) {
        contractContent = _content;
    }

    function getContractContent() public view returns (string memory) {
        return contractContent;
    }
}
'''

compiled_sol = compile_source(contract_source_code)
contract_interface = compiled_sol['<stdin>:ContractStorage']

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
elif sidebar.button('Verify Contract'):
    st.session_state.operation = 'verify_contract'

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

            # Deploy the contract with the generated content
            Contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
            nonce = w3.eth.get_transaction_count(account_address)
            transaction = Contract.constructor(response).build_transaction({
                'from':account_address,  # Mainnet; change to 3 for Ropsten or 4 for Rinkeby
                'gas': 229944,
                'gasPrice': w3.to_wei('50', 'gwei'),
                'nonce': nonce,
            })

            signed_txn = w3.eth.account.sign_transaction(transaction, private_key='6836910e078248b4c4b30c4602bb99740394eed480a5df27afd558625faa5a2d')
            tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            st.success(f"Contract successfully deployed to Ethereum with transaction hash: {tx_hash.hex()} and contract address: {tx_receipt.contractAddress}")

    # Display the generated contract and download button outside the form
    if st.session_state['generated_contract']:
        st.write(st.session_state['generated_contract'])

        pdf_file = save_to_pdf(st.session_state['generated_contract'])
        st.download_button(label="Download Contract", data=pdf_file, file_name="contract.pdf", mime="application/pdf")
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
elif st.session_state.operation == 'verify_contract':
    contract_address = st.text_input("Enter the contract address to verify")

    if st.button("Verify"):
        try:
            # Retrieve the bytecode of the contract at the given address
            deployed_code = w3.eth.get_code(contract_address).hex()

            if deployed_code != "0x":
                st.write("Contract code found at the address.")
                
                # Here you can compare the deployed code with your contract's bytecode
                expected_bytecode = contract_interface['bin']

                # Trim the deployed code to match the length of expected bytecode (ignore constructor args)
                if deployed_code[:len(expected_bytecode)] == expected_bytecode:
                    st.success("The contract code matches the expected smart contract bytecode.")
                else:
                    st.warning("The contract code does not match the expected bytecode.")
            else:
                st.error("No contract code found at this address. The address might not be a smart contract.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

