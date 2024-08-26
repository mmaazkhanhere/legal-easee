from dotenv import load_dotenv
import solcx
import os
import streamlit as st
from web3 import Web3
from solcx import compile_source
import difflib

from helper_functions.pdf_text_extractor import extract_text_from_pdf
from helper_functions.normalization import normalize_text
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

st.set_page_config(
    page_title="LegalEase",  
    page_icon="📝", 
)

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


# Streamlit UI setup
st.title('LegalChain')
st.write('<p style="font-size:22px;">Revolutize contract management with smart technology</p>', unsafe_allow_html=True)
st.divider()

if 'operation' not in st.session_state:
    st.session_state.operation = None

with st.sidebar:
    st.header('Select Operations')
    if st.button('Upload to Blockchain'):
        st.session_state.operation = 'smart_contract'
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

    st.header('Contract Drafting')
    st.write('<p style="font-size:20px;">Use AI technology to draft a contract.</p>', unsafe_allow_html=True)

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
            with st.spinner('Drafting contract...'):
                response = draft_contract(ibm_url, ibm_project_id, st.session_state['contract_type'], st.session_state['country'], st.session_state['party_one'], st.session_state['party_two'], st.session_state['contract_terms'])

                st.session_state['generated_contract'] = response  # Store response in session state

    # Display the generated contract and download button outside the form
    if st.session_state['generated_contract']:
        st.header('Generated Contract')
        st.write(st.session_state['generated_contract'])
        pdf_file = save_to_pdf(st.session_state['generated_contract'])
        st.download_button(label="Download Contract", data=pdf_file, file_name="draft.pdf", mime="application/pdf")


# Suggest Clause Feature


elif st.session_state.operation == 'suggest_clauses':

    st.header('Contract Clause Suggestion')
    st.write('<p style="font-size:20px; text_color:"green">Use AI technology suggest additional clauses for an uploaded contract.</p>', unsafe_allow_html=True)

    if 'contract_text' not in st.session_state:
        st.session_state['contract_text'] = ''

    if 'suggested_clauses' not in st.session_state:
        st.session_state['suggested_clauses'] = ''

    if 'max_tokens' not in st.session_state:
        st.session_state['max_tokens'] = 100

    st.write('<p style="font-size:16px; margin-top:20px">Adjust the maximum tokens. Larger max token value will result in a detailed report.</p>', unsafe_allow_html=True)

    max_tokens = st.slider('Max Tokens', 100, 1000 )

    contract_file = st.file_uploader('Upload a contract file', type=['pdf'])
    btn = st.button('Suggest Clauses')

    if btn and contract_file and max_tokens:
        with st.spinner('Suggesting clauses...'):
            contract_text = extract_text_from_pdf(contract_file)

            st.session_state['contract_text'] = contract_text

            response = suggest_clauses(ibm_url, ibm_project_id, int(max_tokens), st.session_state['contract_text'])
            st.session_state['suggested_clauses'] = response  # Store response in session state

        st.header("Suggested Clauses")
        st.write(st.session_state['suggested_clauses'])


# Contract Compliance Monitoring


elif st.session_state.operation == 'monitor_compliance':
    if 'contract_text' not in st.session_state:
        st.session_state['contract_text'] = ''

    if 'conditions' not in st.session_state:
        st.session_state['conditions'] = ''

    if 'compliance_summary' not in st.session_state:
        st.session_state['compliance_summary'] = ''

    st.header('Contract Compliance Monitoring')
    st.write('<p style="font-size:20px;">Use AI technology access compliance with terms and conditions.</p>', unsafe_allow_html=True)

    st.write('<p style="font-size:16px; margin-top:20px">Adjust the maximum tokens. Larger max token value will result in a detailed report.</p>', unsafe_allow_html=True)
    max_tokens = st.slider('Max Tokens', 100, 1000 )

    contract_file = st.file_uploader('Upload a contract file', type=['pdf'])
    st.session_state['conditions'] = st.text_area('Enter the terms and conditions to check compliance')
    btn = st.button('Check Compliance')

    if contract_file  and btn and max_tokens:
        with st.spinner('Checking compliance...'):
            text_extracted = extract_text_from_pdf(contract_file)
            st.session_state['contract_text'] = text_extracted

            response = monitor_compliance(ibm_url, ibm_project_id, int(max_tokens), st.session_state['contract_text'], st.session_state['conditions'])

            st.session_state['compliance_summary'] = response  # Store response in session state
        st.header("Generated Summary")
        st.write(st.session_state['compliance_summary'])


# Contract Review

elif st.session_state.operation == 'review_contract':
    if 'contract_text' not in st.session_state:
        st.session_state['contract_text'] = ''

    if 'review_summary' not in st.session_state:
        st.session_state['review_summary'] = ''

    st.header('Contract Review')
    st.write('<p style="font-size:20px;">Upload a contract file and our AI system will review and generate a detailed summary.</p>', unsafe_allow_html=True)

    st.write('<p style="font-size:16px; margin-top:20px">Adjust the maximum tokens. Larger max token value will result in a detailed report.</p>', unsafe_allow_html=True)
    max_tokens = st.slider('Max Tokens', 100, 1000 )

    contract_file = st.file_uploader('Upload a contract file', type=['pdf'])
    btn = st.button('Review Contract')

    if contract_file and btn and max_tokens:
        with st.spinner('Reviewing contract...'):
            text_extracted = extract_text_from_pdf(contract_file)
            st.session_state['contract_text'] = text_extracted

            response = review_contract(ibm_url, ibm_project_id, int(max_tokens), st.session_state['contract_text'])
            st.session_state['review_summary'] = response
        st.header('Generated Summary')
        st.write(st.session_state['review_summary'])


# Smart Contract
elif st.session_state.operation == 'smart_contract':

    st.header('Upload to Blockchain')
    st.write('<p style="font-size:20px;">Secure your contracts by uploading it to blockchain.</p>', unsafe_allow_html=True)

    contract_file = st.file_uploader('Upload a contract file', type=['pdf'])
    bt = st.button('Upload')


    if bt:
        contract_textd = extract_text_from_pdf(contract_file)
        Contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
        nonce = w3.eth.get_transaction_count(account_address)
        gas_estimate = Contract.constructor(contract_textd).estimate_gas({
            'from': account_address})
        print(f"Estimated Gas: {gas_estimate}")
        transaction = Contract.constructor(contract_textd).build_transaction({
        'from':account_address,  
                'gas': gas_estimate + 100000,
                'gasPrice': w3.to_wei('50', 'gwei'),
                'nonce': nonce,
        })

        signed_txn = w3.eth.account.sign_transaction(transaction, private_key=os.getenv('PRIVATE_KEY'))
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        st.success(f"Contract successfully deployed to Ethereum with transaction hash: {tx_hash.hex()} and contract address: {tx_receipt.contractAddress}.\n Keep your contract address safe for future use. ")



# Document Comparison


elif st.session_state.operation == 'compare_documents':

    st.header('Document Comparison')
    st.write('<p style="font-size:20px;">Upload different contracts and compare them smartly.</p>', unsafe_allow_html=True)

    if 'original_contract' not in st.session_state:
        st.session_state['original_contract'] = ''

    if 'new_contract' not in st.session_state:
        st.session_state['new_contract'] = ''

    if 'comparison_summary' not in st.session_state:
        st.session_state['comparison_summary'] = ''

    st.write('<p style="font-size:16px; margin-top:20px">Adjust the maximum tokens. Larger max token value will result in a detailed report.</p>', unsafe_allow_html=True)

    max_tokens = st.slider('Max Tokens', 100, 1000 )

    contract_file_first = st.file_uploader('Upload a contract file', type=['pdf'])
    contract_file_second = st.file_uploader('Upload another contract file to compare with', type=['pdf'])
    btn = st.button('Compare Documents')

    if contract_file_first and contract_file_second and btn and max_tokens:
        with st.spinner('Comparing Contracts...'):
            original_contract = extract_text_from_pdf(contract_file_first)
            st.session_state['original_contract'] = original_contract

            new_contract = extract_text_from_pdf(contract_file_second)
            st.session_state['new_contract'] = new_contract

            response = compare_documents(ibm_url, ibm_project_id, int(max_tokens), st.session_state['original_contract'], st.session_state['new_contract'])

            st.session_state['comparison_summary'] = response  # Store response in session state
        st.header('Comparison Summary')
        st.write(st.session_state['comparison_summary'])


# Legal Document Categorization


elif st.session_state.operation == 'categorize_document':
    if 'document_text' not in st.session_state:
        st.session_state['document_text'] = ''

    if 'document_type' not in st.session_state:
        st.session_state['document_type'] = ''

    st.header('Legal Document Categorization')
    st.write('<p style="font-size:20px;">Categorize your legal documents smartly.</p>', unsafe_allow_html=True)

    st.write('<p style="font-size:16px; margin-top:20px">Adjust the maximum tokens. Larger max token value will result in a detailed report.</p>', unsafe_allow_html=True)
    max_tokens = st.slider('Max Tokens', 100, 1000 )

    contract_file = st.file_uploader('Upload a contract file', type=['pdf'])
    btn = st.button('Check Category')


    # Form for legal document categorization input
    if contract_file and btn:
        with st.spinner('Categorizing Contract...'):
            text_extracted = extract_text_from_pdf(contract_file)
            st.session_state['document_text'] = text_extracted

            response = categorize_document(ibm_url, ibm_project_id, int(max_tokens), st.session_state['document_text'])
            st.session_state['document_type'] = response  # Store response in session state
        st.header('Document Type')
        st.write(st.session_state['document_type'])


# Verify Contract


elif st.session_state.operation == 'verify_contract':

    st.header('Verify Contract')
    st.write('<p style="font-size:20px;">Verify that your contract is uploaded to blockchain.</p>', unsafe_allow_html=True)

    uploaded_contract = st.file_uploader('Upload the contract file', type=['pdf'])
    contract_address = st.text_input("Enter the contract address to verify")

    def is_valid_eth_address(address):
        return Web3.is_address(address)
    if st.button("Verify"):
        if uploaded_contract and contract_address:
            # Validate the contract address
            if not is_valid_eth_address(contract_address):
                st.error("The entered contract address is not valid. Please enter a valid Ethereum address.")
            else:
                checksum_address = Web3.to_checksum_address(contract_address)

                # Extract text from the uploaded PDF
                uploaded_contract_content = extract_text_from_pdf(uploaded_contract)

                # Normalize the uploaded contract content
                normalized_uploaded_content = normalize_text(uploaded_contract_content)

                try:
                    # Load the deployed contract
                    Contract = w3.eth.contract(address=checksum_address, abi=contract_interface['abi'])

                    # Fetch the contract content stored on the blockchain
                    stored_contract_content = Contract.functions.getContractContent().call()

                    # Normalize the stored contract content
                    normalized_stored_content = normalize_text(stored_contract_content)

                    # Compare the normalized texts
                    if normalized_uploaded_content == normalized_stored_content:
                        st.success("The uploaded contract content matches the contract stored on the blockchain.")
                    else:
                        st.warning("The uploaded contract content does not match the contract stored on the blockchain.")

                        # Optionally, you can display the differences using difflib
                        diff = difflib.ndiff(normalized_uploaded_content.splitlines(), normalized_stored_content.splitlines())
                        st.text('\n'.join(diff))
                except Exception as e:
                    st.error(f"An error occurred while verifying the contract: {str(e)}")
        else:
            st.error("Please upload a contract file and enter a valid contract address.")

    


