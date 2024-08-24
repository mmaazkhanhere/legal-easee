from web3 import Web3
import json
import os
from dotenv import load_dotenv
import streamlit as st
from langchain_ibm import WatsonxLLM
load_dotenv()

# Connect to local Ethereum node (you can replace the provider URL with your own)
alchemy_url = os.environ['ALCHEMY_URL']
w3 = Web3(Web3.HTTPProvider(alchemy_url))

# Check and set the default account
default_account = os.getenv('DEFAULT_ACCOUNT')
w3.eth.default_account = default_account

#Validate the default account only if it is not empty and is a string
if isinstance(default_account, str) and default_account:
    if not Web3.is_checksum_address(default_account):
        default_account = Web3.to_checksum_address(default_account)
else:
    raise ValueError("Invalid Ethereum address. Please ensure the default account is correctly set.")

# Smart contract ABI and bytecode (replace with your actual ABI and bytecode)
contract_abi = json.loads('''
[
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "contractContent",
                "type": "string"
            }
        ],
        "name": "storeContract",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]
''')
contract_bytecode = '0x...'

# Function to deploy the ContractManager smart contract
def deploy_contract_manager():
    # Create contract instance
    ContractManager = w3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)

    # Get the nonce for the transaction
    nonce = w3.eth.get_transaction_count(default_account)

    # Build the transaction
    transaction = ContractManager.constructor().build_transaction({
        'chainId': 1,  # Ethereum mainnet, replace with your network ID
        'gas': 2000000,
        'gasPrice': w3.to_wei('20', 'gwei'),
        'nonce': nonce,
        'from': default_account
    })

    # Sign the transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key='YOUR_PRIVATE_KEY')

    # Send the transaction
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    # Wait for the transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    # Return the contract address
    return tx_receipt.contractAddress

# Function to draft a contract
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
# Sample usage of draft_contract function
if __name__ == "__main__":
    sample_contract_data = {
        "partyA": "Alice",
        "partyB": "Bob",
        "terms": "Sample contract terms"
    }
    
    receipt = draft_contract(sample_contract_data)
    print(f"Contract successfully created with transaction hash: {receipt.transactionHash.hex()}")
