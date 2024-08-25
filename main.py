from dotenv import load_dotenv
import solcx
import os
import streamlit as st
from web3 import Web3
from solcx import compile_source
from langchain_ibm import WatsonxLLM 

from helper_functions.pdf_text_extractor import extract_text_from_pdf

from features.draft_generation import draft_contract
from helper_functions.pdf_conversion import save_to_pdf
from features.contract_clause_suggestion import suggest_clauses
from features.contract_compliance_monitoring import monitor_compliance
from features.contract_review import review_contract
from features.document_comparison import compare_documents
from features.legal_document_categorization import categorize_document
# Load environment variables
load_dotenv()

# def verify_contract(contract_address, expected_terms):
#     contract = w3.eth.contract(address=contract_address, abi=contract_interface['abi'])
    
#     # Use getContractContent instead of getContractTerms
#     contract_content = contract.functions.getContractContent().call()
#     if contract_content != expected_terms:
#         return "Contract content does not match!"
    
#     return "Contract verification successful!"

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

with st.sidebar:
    st.header('Select Operations')
    if st.button('Contract Drafting'):
        st.session_state.operation = 'contract_drafting'
    if st.button('Contract Clause Suggestion'):
        st.session_state.operation = 'suggest_clauses'
    if st.button('Contract Compliance Monitoring'):
        st.session_state.operation = 'monitor_compliance'
    if st.button('Contract Review'):
        st.session_state.operation = 'review_contract'
    if st.button('Document Comparison'):
        st.session_state.operation = 'compare_documents'
    if st.button('Legal Document Categorization'):
        st.session_state.operation = 'categorize_document'
    if st.button('Verify Contract'):
        st.session_state.operation = 'verify_contract'

# Contract Drafting Feature

if st.session_state.operation == 'contract_drafting':
    if 'contract_type' not in st.session_state:
        st.session_state['contract_type'] = 'NDA'

    if 'country' not in st.session_state:
        st.session_state['country'] = 'United States'

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
            ['Australia', 'Canada', 'United Arab Emirates','United Kingdom', 'USA'], 
            index=['Australia', 'Canada', 'United Arab Emirates','United Kingdom', 'USA'].index(st.session_state['country'])
        )

        st.session_state['party_one'] = st.text_input('Enter the name of Party One', value=st.session_state['party_one'])
        st.session_state['party_two'] = st.text_input('Enter the name of Party Two', value=st.session_state['party_two'])
        st.session_state['contract_terms'] = st.text_area('Enter the key terms and conditions', value=st.session_state['contract_terms'])

        btn = st.form_submit_button('Draft')
        if btn:
            response = draft_contract(ibm_url, ibm_project_id, parameters, st.session_state['contract_type'], st.session_state['country'], st.session_state['party_one'], st.session_state['party_two'], st.session_state['contract_terms'])

            st.session_state['generated_contract'] = response  # Store response in session state

            # Deploy the contract with the generated content
            

            Contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
            nonce = w3.eth.get_transaction_count(account_address)
            gas_estimate = Contract.constructor(response).estimate_gas({
            'from': account_address})
            print(f"Estimated Gas: {gas_estimate}")
            transaction = Contract.constructor(response).build_transaction({
                'from':account_address,  # Mainnet; change to 3 for Ropsten or 4 for Rinkeby
                'gas': gas_estimate + 100000,
                'gasPrice': w3.to_wei('50', 'gwei'),
                'nonce': nonce,
            })

            signed_txn = w3.eth.account.sign_transaction(transaction, private_key='6836910e078248b4c4b30c4602bb99740394eed480a5df27afd558625faa5a2d')
            tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            st.success(f"Contract successfully deployed to Ethereum with transaction hash: {tx_hash.hex()} and contract address: {tx_receipt.contractAddress}")
            # verification_result = verify_contract(tx_receipt.contractAddress, st.session_state['contract_terms'])
            # st.write(verification_result)

    # Display the generated contract and download button outside the form
    if st.session_state['generated_contract']:
        st.write(st.session_state['generated_contract'])

        pdf_file = save_to_pdf(st.session_state['generated_contract'])
        st.download_button(label="Download Contract", data=pdf_file, file_name=f"{tx_receipt.contractAddress}.pdf", mime="application/pdf")


# Suggest Clause Feature


elif st.session_state.operation == 'suggest_clauses':
    if 'contract_text' not in st.session_state:
        st.session_state['contract_text'] = ''

    if 'suggested_clauses' not in st.session_state:
        st.session_state['suggested_clauses'] = ''

    if 'max_tokens' not in st.session_state:
        st.session_state['max_tokens'] = 100

    st.write('<p style="font-size:16px;">Adjust the maximum tokens. Larger max token value will result in a detailed report.</p>', unsafe_allow_html=True)

    max_tokens = st.slider('Max Tokens', 100, 1000 )

    contract_file = st.file_uploader('Upload a contract file', type=['pdf'])
    btn = st.button('Suggest Clauses')

    if btn and contract_file and max_tokens:

        contract_text = extract_text_from_pdf(contract_file)

        st.session_state['contract_text'] = contract_text

        response = suggest_clauses(ibm_url, ibm_project_id, int(max_tokens), st.session_state['contract_text'])
        st.session_state['suggested_clauses'] = response  # Store response in session state
        st.write(st.session_state['suggested_clauses'])


# Contract Compliance Monitoring


elif st.session_state.operation == 'monitor_compliance':
    if 'contract_text' not in st.session_state:
        st.session_state['contract_text'] = ''

    if 'compliance_summary' not in st.session_state:
        st.session_state['compliance_summary'] = ''


    st.write('<p style="font-size:16px;">Adjust the maximum tokens. Larger max token value will result in a detailed report.</p>', unsafe_allow_html=True)

    max_tokens = st.slider('Max Tokens', 100, 1000 )

    contract_file = st.file_uploader('Upload a contract file', type=['pdf'])
    btn = st.button('Check Compliance')

    if contract_file and btn and max_tokens:
        text_extracted = extract_text_from_pdf(contract_file)
        st.session_state['contract_text'] = text_extracted

        response = monitor_compliance(ibm_url, ibm_project_id, int(max_tokens), st.session_state['contract_text'])
        st.session_state['compliance_summary'] = response  # Store response in session state
        st.write(st.session_state['compliance_summary'])


# Contract Review


elif st.session_state.operation == 'review_contract':
    if 'contract_text' not in st.session_state:
        st.session_state['contract_text'] = ''

    if 'review_summary' not in st.session_state:
        st.session_state['review_summary'] = ''

    st.write('<p style="font-size:16px;">Adjust the maximum tokens. Larger max token value will result in a detailed report.</p>', unsafe_allow_html=True)

    max_tokens = st.slider('Max Tokens', 100, 1000 )

    contract_file = st.file_uploader('Upload a contract file', type=['pdf'])
    btn = st.button('Review Contract')

    if contract_file and btn and max_tokens:

        text_extracted = extract_text_from_pdf(contract_file)
        st.session_state['contract_text'] = text_extracted

        response = review_contract(ibm_url, ibm_project_id, int(max_tokens), st.session_state['contract_text'])
        st.session_state['review_summary'] = response
        st.write(st.session_state['review_summary'])


# Document Comparison


elif st.session_state.operation == 'compare_documents':
    if 'original_contract' not in st.session_state:
        st.session_state['original_contract'] = ''

    if 'new_contract' not in st.session_state:
        st.session_state['new_contract'] = ''

    if 'comparison_summary' not in st.session_state:
        st.session_state['comparison_summary'] = ''

    st.write('<p style="font-size:16px;">Adjust the maximum tokens. Larger max token value will result in a detailed report.</p>', unsafe_allow_html=True)

    max_tokens = st.slider('Max Tokens', 100, 1000 )

    contract_file_first = st.file_uploader('Upload a contract file', type=['pdf'])
    contract_file_second = st.file_uploader('Upload another contract file to compare with', type=['pdf'])
    btn = st.button('Compare Documents')

    if contract_file_first and contract_file_second and btn and max_tokens:

        original_contract = extract_text_from_pdf(contract_file_first)
        st.session_state['original_contract'] = original_contract

        new_contract = extract_text_from_pdf(contract_file_first)
        st.session_state['new_contract'] = new_contract

        response = compare_documents(ibm_url, ibm_project_id, int(max_tokens), st.session_state['original_contract'], st.session_state['new_contract'])

        st.session_state['comparison_summary'] = response  # Store response in session state
        st.write(st.session_state['comparison_summary'])


# Legal Document Categorization


elif st.session_state.operation == 'categorize_document':
    if 'document_text' not in st.session_state:
        st.session_state['document_text'] = ''

    if 'document_type' not in st.session_state:
        st.session_state['document_type'] = ''

    st.write('<p style="font-size:16px;">Adjust the maximum tokens. Larger max token value will result in a detailed report.</p>', unsafe_allow_html=True)

    max_tokens = st.slider('Max Tokens', 100, 1000 )

    contract_file = st.file_uploader('Upload a contract file', type=['pdf'])
    btn = st.button('Check Compliance')


    # Form for legal document categorization input
    if contract_file and btn:
        text_extracted = extract_text_from_pdf(contract_file)
        st.session_state['document_text'] = text_extracted

        response = categorize_document(ibm_url, ibm_project_id, int(max_tokens), st.session_state['document_text'])
        st.session_state['document_type'] = response  # Store response in session state
        st.write(st.session_state['document_type'])


# Verify Contract


elif st.session_state.operation == 'verify_contract':
    contract_address = st.text_input("Enter the contract address to verify")

    if st.button("Verify"):
        try:
            # Retrieve the bytecode of the contract at the given address
            deployed_code = w3.eth.get_code(contract_address).hex()

            if deployed_code != "0x":
                st.write("Contract code found at the address.")
                
                # Print the full deployed bytecode for debugging
                st.write(f"Full Deployed code: {deployed_code}")

                # Compare with expected bytecode
                expected_bytecode = contract_interface['bin']

                # Print the first and last parts of both bytecodes for comparison
                st.write(f"Expected code (first 20 chars): {expected_bytecode[:20]}")
                st.write(f"Expected code (last 20 chars): {expected_bytecode[-20:]}")

                # Compare the main part of the bytecode
                if deployed_code[:len(expected_bytecode)] == expected_bytecode:
                    st.success("The contract code matches the expected smart contract bytecode.")
                else:
                    st.warning("The contract code does not match the expected bytecode.")
            else:
                st.error("No contract code found at this address. The address might not be a smart contract.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")



