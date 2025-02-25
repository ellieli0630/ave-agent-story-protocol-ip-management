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
LICENSING_MODULE = '0x04fbd8a2e56dd85CFD5500A4A4DfA955B9f1dE6f'
PIL_TEMPLATE = '0x2E896b0b2Fdb7457499B56AAaA4AE55BCB4Cd316'

# Known values
IP_ID = '0x2A953Bcd9B4813Ab9F3BBFcA47388d1d67f3603D'
TERMS_ID = 1  # Try with a small terms ID

# ABI
LICENSING_MODULE_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "ipId", "type": "address"},
            {"internalType": "address", "name": "licenseTemplate", "type": "address"},
            {"internalType": "uint256", "name": "termsId", "type": "uint256"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
            {"internalType": "address", "name": "receiver", "type": "address"},
            {"internalType": "string", "name": "metadata", "type": "string"},
            {"internalType": "uint64", "name": "timestamp", "type": "uint64"},
            {"internalType": "uint64", "name": "expiration", "type": "uint64"}
        ],
        "name": "mintLicenseTokens",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

def mint_license_token():
    """Mint a license token"""
    licensing_module = w3.eth.contract(address=LICENSING_MODULE, abi=LICENSING_MODULE_ABI)
    
    # Build transaction
    nonce = w3.eth.get_transaction_count(account.address)
    gas_price = w3.eth.gas_price
    
    transaction = licensing_module.functions.mintLicenseTokens(
        IP_ID,
        PIL_TEMPLATE,
        TERMS_ID,
        1,              # Mint 1 token
        account.address,  # Token receiver
        "",             # No metadata
        0,              # No timestamp
        0               # No expiration
    ).build_transaction({
        'from': account.address,
        'gas': 500000,
        'gasPrice': gas_price,
        'nonce': nonce,
    })
    
    # Sign and send transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, account.key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    
    # Wait for receipt
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    if len(receipt['logs']) > 0 and len(receipt['logs'][0]['topics']) > 3:
        token_id = int(receipt['logs'][0]['topics'][3].hex(), 16)
        print(f"Successfully minted token with ID: {token_id}")
    else:
        print("Transaction completed but couldn't find token ID in logs")
        print("Receipt:", receipt)

def main():
    print("Attempting to mint license token...")
    print(f"Using IP ID: {IP_ID}")
    print(f"Using Terms ID: {TERMS_ID}")
    mint_license_token()

if __name__ == "__main__":
    main()
