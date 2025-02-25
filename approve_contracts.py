from web3 import Web3
from eth_account import Account
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to Story Protocol testnet
w3 = Web3(Web3.HTTPProvider(os.getenv('STORY_RPC_URL')))
account = Account.from_key(os.getenv('STORY_WALLET_PRIVATE_KEY'))

# Contract addresses
AVA_CHARACTER = '0x0b3BcE84Da0F1F58177a3dAF434F0Ab0Baf1050D'
PIL_TEMPLATE = '0x2E896b0b2Fdb7457499B56AAaA4AE55BCB4Cd316'
LICENSING_MODULE = '0x04fbd8a2e56dd85CFD5500A4A4DfA955B9f1dE6f'

# ABI for approval function
ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "operator", "type": "address"},
            {"internalType": "bool", "name": "approved", "type": "bool"}
        ],
        "name": "setApprovalForAll",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "owner", "type": "address"},
            {"internalType": "address", "name": "operator", "type": "address"}
        ],
        "name": "isApprovedForAll",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    }
]

def approve_contract(contract_address, operator_address):
    contract = w3.eth.contract(address=contract_address, abi=ABI)
    
    # Check if already approved
    is_approved = contract.functions.isApprovedForAll(account.address, operator_address).call()
    if is_approved:
        print(f"Already approved for {operator_address}")
        return

    # Build the transaction
    nonce = w3.eth.get_transaction_count(account.address)
    gas_price = w3.eth.gas_price
    
    transaction = contract.functions.setApprovalForAll(
        operator_address,
        True
    ).build_transaction({
        'from': account.address,
        'gas': 100000,  # Adjust gas as needed
        'gasPrice': gas_price,
        'nonce': nonce,
    })
    
    # Sign and send the transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, account.key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    
    # Wait for transaction receipt
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Approved {operator_address}. Transaction hash: {receipt['transactionHash'].hex()}")

def main():
    print("Starting approvals...")
    
    # Approve PIL Template
    print("\nApproving PIL Template...")
    approve_contract(AVA_CHARACTER, PIL_TEMPLATE)
    
    # Approve Licensing Module
    print("\nApproving Licensing Module...")
    approve_contract(AVA_CHARACTER, LICENSING_MODULE)
    
    print("\nAll approvals completed!")

if __name__ == "__main__":
    main()
