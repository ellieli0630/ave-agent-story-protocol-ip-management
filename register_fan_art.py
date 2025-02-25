import os
import sys
import json
import requests
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import base64
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Web3
w3 = Web3(Web3.HTTPProvider(os.getenv('STORY_RPC_URL')))
account = w3.eth.account.from_key(os.getenv('STORY_WALLET_PRIVATE_KEY'))

# Contract addresses (with checksum)
IP_ASSET_REGISTRY_ADDRESS = Web3.to_checksum_address("0x77319B4031e6eF1250907aa00018B8B1c67a244b")
LICENSE_REGISTRY_ADDRESS = Web3.to_checksum_address("0x529a750E02d8E2f15649c13D69a465286a780e24")
LICENSING_MODULE_ADDRESS = Web3.to_checksum_address("0x04fbd8a2e56dd85CFD5500A4A4DfA955B9f1dE6f")
PIL_TEMPLATE_ADDRESS = Web3.to_checksum_address("0x2E896b0b2Fdb7457499B56AAaA4AE55BCB4Cd316")
ROYALTY_POLICY_LAP = Web3.to_checksum_address("0xBe54FB168b3c982b7AaE60dB6CF75Bd8447b390E")
MERC20 = Web3.to_checksum_address("0xF2104833d386a2734a4eB3B8ad6FC6812F29E38E")

# Contract ABIs
PIL_TEMPLATE_ABI = [
    {
        "inputs": [
            {
                "components": [
                    {"internalType": "uint256", "name": "mintingFee", "type": "uint256"},
                    {"internalType": "uint256", "name": "commercialRevShare", "type": "uint256"},
                    {"internalType": "address", "name": "royaltyPolicy", "type": "address"},
                    {"internalType": "address", "name": "currencyToken", "type": "address"}
                ],
                "internalType": "struct PILTerms",
                "name": "terms",
                "type": "tuple"
            }
        ],
        "name": "registerLicenseTerms",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

LICENSING_MODULE_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "ipId", "type": "address"},
            {"internalType": "address", "name": "licenseTemplate", "type": "address"},
            {"internalType": "uint256", "name": "licenseTermsId", "type": "uint256"}
        ],
        "name": "attachLicenseTerms",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "licensorIpId", "type": "address"},
            {"internalType": "address", "name": "licenseTemplate", "type": "address"},
            {"internalType": "uint256", "name": "licenseTermsId", "type": "uint256"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
            {"internalType": "address", "name": "receiver", "type": "address"},
            {"internalType": "string", "name": "royaltyContext", "type": "string"},
            {"internalType": "uint256", "name": "maxMintingFee", "type": "uint256"},
            {"internalType": "uint256", "name": "maxRevenueShare", "type": "uint256"}
        ],
        "name": "mintLicenseTokens",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "licensorIpId", "type": "address"},
            {"internalType": "address", "name": "licenseTemplate", "type": "address"},
            {"internalType": "uint256", "name": "licenseTermsId", "type": "uint256"}
        ],
        "name": "getLicenseTokenId",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "childIpId", "type": "address"},
            {"internalType": "uint256[]", "name": "licenseTokenIds", "type": "uint256[]"},
            {"internalType": "string", "name": "royaltyContext", "type": "string"},
            {"internalType": "uint256", "name": "maxRts", "type": "uint256"}
        ],
        "name": "registerDerivativeWithLicenseTokens",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

IP_ASSET_REGISTRY_ABI = [
    {
        "inputs": [
            {"internalType": "uint256", "name": "chainId", "type": "uint256"},
            {"internalType": "address", "name": "tokenContract", "type": "address"},
            {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
        ],
        "name": "register",
        "outputs": [{"internalType": "address", "name": "ipId", "type": "address"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "ipId", "type": "address"},
            {"indexed": True, "internalType": "address", "name": "tokenContract", "type": "address"},
            {"indexed": True, "internalType": "uint256", "name": "tokenId", "type": "uint256"}
        ],
        "name": "Register",
        "type": "event"
    }
]

def upload_to_pinata(data):
    """Upload data to IPFS via Pinata"""
    try:
        headers = {
            'Authorization': f'Bearer {os.getenv("PINATA_JWT")}'
        }
        
        if isinstance(data, dict):
            # If data is a dictionary, upload as JSON
            response = requests.post(
                'https://api.pinata.cloud/pinning/pinJSONToIPFS',
                headers=headers,
                json=data
            )
        else:
            # If data is binary, upload as file
            files = {
                'file': ('to-da-moon-fan-art.png', data, 'image/png')
            }
            response = requests.post(
                'https://api.pinata.cloud/pinning/pinFileToIPFS',
                headers=headers,
                files=files
            )
        
        if response.status_code == 200:
            return response.json()['IpfsHash']
        else:
            raise Exception(f"Failed to upload to IPFS: {response.text}")
            
    except Exception as e:
        print(f"Error uploading to IPFS: {str(e)}")
        raise

def setup_license_terms(parent_ip_id):
    """Setup license terms for the parent IP if not already done"""
    try:
        # Get contract instances
        pil_template = w3.eth.contract(
            address=PIL_TEMPLATE_ADDRESS,
            abi=PIL_TEMPLATE_ABI
        )
        
        licensing_module = w3.eth.contract(
            address=LICENSING_MODULE_ADDRESS,
            abi=LICENSING_MODULE_ABI
        )

        # Register commercial remix license terms
        license_terms = {
            'mintingFee': 0,
            'commercialRevShare': 10 * 10**6,  # 10%
            'royaltyPolicy': ROYALTY_POLICY_LAP,
            'currencyToken': MERC20
        }

        # Register license terms
        register_terms_tx = pil_template.functions.registerLicenseTerms(
            [
                license_terms['mintingFee'],
                license_terms['commercialRevShare'],
                license_terms['royaltyPolicy'],
                license_terms['currencyToken']
            ]
        ).build_transaction({
            'from': account.address,
            'gas': 500000,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(account.address),
        })

        # Sign and send transaction
        signed_tx = account.sign_transaction(register_terms_tx)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"License terms registration transaction sent: {tx_hash.hex()}")

        # Wait for transaction receipt
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"License terms registration confirmed: {tx_receipt['transactionHash'].hex()}")
        
        # For now, hardcode a license terms ID since we can't get it from logs
        license_terms_id = 1
        print(f"Using license terms ID: {license_terms_id}")

        # Attach license terms to the IP
        attach_terms_tx = licensing_module.functions.attachLicenseTerms(
            parent_ip_id,
            PIL_TEMPLATE_ADDRESS,
            license_terms_id
        ).build_transaction({
            'from': account.address,
            'gas': 500000,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(account.address),
        })

        # Sign and send transaction
        signed_tx = account.sign_transaction(attach_terms_tx)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"Attach license terms transaction sent: {tx_hash.hex()}")

        # Wait for transaction receipt
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Attach license terms confirmed: {tx_receipt['transactionHash'].hex()}")

        return license_terms_id

    except Exception as e:
        print(f"Error setting up license terms: {str(e)}")
        raise

def mint_license_token(parent_ip_id, license_terms_id):
    """Mint a license token for the parent IP"""
    try:
        # Get contract instance
        licensing_module = w3.eth.contract(
            address=LICENSING_MODULE_ADDRESS,
            abi=LICENSING_MODULE_ABI
        )

        # Build the transaction
        mint_tx = licensing_module.functions.mintLicenseTokens(
            parent_ip_id,  # licensorIpId
            PIL_TEMPLATE_ADDRESS,  # licenseTemplate
            license_terms_id,  # licenseTermsId
            1,  # amount - we only need one token
            account.address,  # receiver - mint to ourselves
            "",  # royaltyContext (empty for PIL)
            0,  # maxMintingFee
            0   # maxRevenueShare
        ).build_transaction({
            'from': account.address,
            'gas': 500000,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(account.address),
        })

        # Sign and send transaction
        signed_tx = account.sign_transaction(mint_tx)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"License token minting transaction sent: {tx_hash.hex()}")

        # Wait for transaction receipt
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"License token minting confirmed: {tx_receipt['transactionHash'].hex()}")

        # Get the transaction data
        tx = w3.eth.get_transaction(tx_hash)
        result = licensing_module.decode_function_input(tx.input)
        token_id = result[1]['amount']  # The first token ID
            
        print(f"Using license token ID: {token_id}")
        return token_id

    except Exception as e:
        print(f"Error minting license token: {str(e)}")
        raise

def register_derivative_work(image_data, name, description, parent_ip_id, license_token_id):
    """Register a derivative work"""
    try:
        # Upload to IPFS
        print("Uploading image to IPFS...")
        image_cid = upload_to_pinata(image_data)
        print(f"Image uploaded to IPFS: {image_cid}")

        # Create metadata
        metadata = {
            "name": name,
            "description": description,
            "image": f"ipfs://{image_cid}",
            "parent_ip_id": parent_ip_id,
            "license_token_id": license_token_id
        }
        
        # Upload metadata to IPFS
        print("Uploading metadata to IPFS...")
        metadata_cid = upload_to_pinata(json.dumps(metadata))
        print(f"Metadata uploaded to IPFS: {metadata_cid}")

        # Register the IP Asset
        print("Registering IP Asset...")
        ip_asset_registry = w3.eth.contract(
            address=IP_ASSET_REGISTRY_ADDRESS,
            abi=IP_ASSET_REGISTRY_ABI
        )

        # Register the IP Asset
        register_tx = ip_asset_registry.functions.register(
            1,  # chainId (1 for Ethereum mainnet)
            MERC20,  # tokenContract (using MERC20 as a placeholder)
            1  # tokenId (using 1 as a placeholder)
        ).build_transaction({
            'from': account.address,
            'gas': 500000,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(account.address),
        })

        # Sign and send transaction
        signed_tx = account.sign_transaction(register_tx)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"IP Asset registration transaction sent: {tx_hash.hex()}")

        # Wait for transaction receipt
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"IP Asset registration confirmed: {tx_receipt['transactionHash'].hex()}")

        # Get the IP ID by calling the function again
        child_ip_id = ip_asset_registry.functions.register(
            1,  # chainId (1 for Ethereum mainnet)
            MERC20,  # tokenContract (using MERC20 as a placeholder)
            1  # tokenId (using 1 as a placeholder)
        ).call()
        print(f"IP Asset registered with ID: {child_ip_id}")

        # Register as derivative work
        print("Registering derivative work...")
        licensing_module = w3.eth.contract(
            address=LICENSING_MODULE_ADDRESS,
            abi=LICENSING_MODULE_ABI
        )

        # Create array with license token ID
        license_token_ids = [license_token_id]

        # Register the derivative work
        derivative_tx = licensing_module.functions.registerDerivativeWithLicenseTokens(
            child_ip_id,  # childIpId
            license_token_ids,  # licenseTokenIds
            "",  # royaltyContext (empty for PIL)
            0  # maxRts
        ).build_transaction({
            'from': account.address,
            'gas': 500000,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(account.address),
        })

        # Sign and send transaction
        signed_tx = account.sign_transaction(derivative_tx)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"Derivative work registration transaction sent: {tx_hash.hex()}")

        # Wait for transaction receipt
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Derivative work registration confirmed: {tx_receipt['transactionHash'].hex()}")

        return child_ip_id

    except Exception as e:
        print(f"Error registering derivative work: {str(e)}")
        raise

def main():
    """Main function to register the To Da Moon fan art"""
    try:
        # Image data
        with open('to-da-moon-fan-art.png', 'rb') as f:
            image_data = f.read()
        
        # Derivative work details
        name = "To Da Moon, fan creation"
        description = """A pixel art creation inspired by Ava's character, featuring a retro computer setup against a cosmic backdrop with a glowing pink moon. The piece captures the essence of Web3 and crypto culture while paying homage to the original character."""
        parent_ip_id = "0x0AedD694851871614012d67195a6DeE1930682cf"  # Ava's character IP ID

        # Setup license terms and get license token
        license_terms_id = setup_license_terms(parent_ip_id)
        license_token_id = mint_license_token(parent_ip_id, license_terms_id)

        # Register the derivative work
        derivative_ip_id = register_derivative_work(image_data, name, description, parent_ip_id, license_token_id)
        print(f"Successfully registered derivative work with ID: {derivative_ip_id}")

        # Post tweet about successful registration
        from twitter_integration import post_tweet
        tweet_text = f"""🎨 Just registered a new derivative work on @StoryProtocol!

Title: {name}
Description: A pixel art creation inspired by Ava's character 🖥️ 🌙

View on Story Protocol: https://aeneid.storyscan.xyz/ip/{derivative_ip_id}
View on IPFS: https://gateway.pinata.cloud/ipfs/QmSMyBsUQ2VDEpwENBK63zHPiY5cT2YkCjjW8th8YrhXJT"""

        tweet_id = post_tweet(tweet_text)
        print(f"\nTweeted about registration! View at: https://twitter.com/user/status/{tweet_id}")
        
    except Exception as e:
        print(f"Error in main: {str(e)}")
        raise

if __name__ == "__main__":
    main()
