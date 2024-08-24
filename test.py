import streamlit as st
import logging
from web3 import Web3
import solcx
from web3.exceptions import TransactionNotFound
from requests.exceptions import HTTPError
from eth_account import Account
import os
from dotenv import load_dotenv

load_dotenv()

# Configure logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Check and install solc if necessary
try:
    solcx.set_solc_version('0.8.0')
except solcx.exceptions.SolcNotInstalled:
    st.write("Solc is not installed. Installing Solc 0.8.0...")
    solcx.install_solc('0.8.0')
    solcx.set_solc_version('0.8.0')

# Replace with your correct Alchemy URL for Sepolia
alchemy_url = 'https://eth-sepolia.g.alchemy.com/v2/OMrPcGI7yKVdXztYMqMclJwCmSZihaAU'
w3 = Web3(Web3.HTTPProvider(alchemy_url))

# Set the default account (replace with your account address)
default_account = '0xe62244f4e29cb4848027eec72AEAae8d375036f4'  # Replace with your actual account address
w3.eth.default_account = default_account

# Test connection and basic network information
try:
    if w3.is_connected():
        st.success(f'Connected to Sepolia testnet via Alchemy with account {default_account}')
        latest_block = w3.eth.block_number
        st.write(f'Latest Block: {latest_block}')
        logger.info(f'Connected to Sepolia testnet. Latest Block: {latest_block}')
    else:
        st.error('Failed to connect to Sepolia testnet')
        logger.error('Failed to connect to Sepolia testnet')
except HTTPError as http_err:
    st.error(f"HTTP error occurred: {http_err}")
    logger.error(f"HTTP error occurred: {http_err}")
except Exception as e:
    st.error(f"Unexpected error during connection: {str(e)}")
    logger.error(f"Unexpected error during connection: {str(e)}")

# Check account balance
try:
    balance = w3.eth.get_balance(default_account)
    st.write(f'Account Balance: {w3.from_wei(balance, "ether")} ETH')
    logger.info(f'Account Balance: {w3.from_wei(balance, "ether")} ETH')
except Exception as e:
    st.error(f"Error fetching balance: {str(e)}")
    logger.error(f"Error fetching balance: {str(e)}")

# Solidity source code
contract_source_code = '''
pragma solidity ^0.8.0;

contract ContractManager {
    struct Contract {
        uint id;
        string content;
        address owner;
    }

    mapping(uint => Contract) public contracts;
    uint public contractCount = 0;

    function createContract(string memory _content) public {
        contractCount++;
        contracts[contractCount] = Contract(contractCount, _content, msg.sender);
    }

    function getContract(uint _id) public view returns (string memory) {
        require(contracts[_id].owner == msg.sender, "Not the owner of the contract");
        return contracts[_id].content;
    }
}
'''

# Compile the contract
try:
    compiled_sol = solcx.compile_source(contract_source_code)
    contract_interface = compiled_sol['<stdin>:ContractManager']
    st.write(f'Contract ABI: {contract_interface["abi"]}')
    st.write(f'Contract Bytecode: {contract_interface["bin"]}')
    logger.info('Contract compiled successfully')
except Exception as e:
    st.error(f"Compilation error: {str(e)}")
    logger.error(f"Compilation error: {str(e)}")
    st.stop()


def deploy_contract_manager():
    try:
        # Create contract instance
        ContractManager = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
        
        # Create a transaction dictionary
        nonce = w3.eth.get_transaction_count(w3.eth.default_account)
        transaction = ContractManager.constructor().build_transaction({
            'nonce': nonce,
            'gas': 3000000,
            'gasPrice': w3.to_wei('30', 'gwei'),
            'from': w3.eth.default_account
        })

        # Sign the transaction locally with your private key
        private_key = os.environ['PRIVATE_KEY']  # Replace with your actual private key
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

        # Send the signed transaction
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        logger.info(f'Transaction hash: {tx_hash.hex()}')

        # Wait for transaction receipt
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        logger.info(f'Contract deployed at address: {tx_receipt.contractAddress}')
        return tx_receipt.contractAddress
    except ValueError as e:
        st.error(f"ValueError: {str(e)}")
        logger.error(f"ValueError: {str(e)}")
    except Exception as e:
        st.error(f"Unexpected error during contract deployment: {str(e)}")
        logger.error(f"Unexpected error during contract deployment: {str(e)}")
    return None

contract_manager_address = deploy_contract_manager()

if contract_manager_address:
    st.write(f'ContractManager deployed at address: {contract_manager_address}')
else:
    st.error("ContractManager deployment failed.")

# Test a simple transaction to ensure everything is working
def test_transaction():
    try:
        tx_hash = w3.eth.send_transaction({
            'from': default_account,
            'to': '0xSomeOtherAddress',  # Replace with another valid address
            'value': w3.to_wei(0.01, 'ether'),
            'gas': 3000000,
            'gasPrice': w3.to_wei('30', 'gwei')
        })
        logger.info(f'Transaction hash: {tx_hash.hex()}')
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        st.write(f'Successful transaction with hash: {tx_receipt.transactionHash.hex()}')
        logger.info(f'Successful transaction with hash: {tx_receipt.transactionHash.hex()}')
    except Exception as e:
        st.error(f"Transaction error: {str(e)}")
        logger.error(f"Transaction error: {str(e)}")

# Uncomment the line below to test sending a transaction
# test_transaction()