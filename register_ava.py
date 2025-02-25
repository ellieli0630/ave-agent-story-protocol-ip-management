import os
import json
import requests
from web3 import Web3
from eth_account import Account
from dotenv import load_dotenv
import solcx

# Load environment variables
load_dotenv()

# Initialize web3 with Story Protocol RPC URL
w3 = Web3(Web3.HTTPProvider(os.getenv('STORY_RPC_URL')))

# Initialize account with private key
account = Account.from_key(os.getenv('STORY_WALLET_PRIVATE_KEY'))

# Contract addresses for Story Protocol Testnet (Sepolia)
ADDRESSES = {
    "IP_ASSET_REGISTRY": "0x77319B4031e6eF1250907aa00018B8B1c67a244b",
    "REGISTRATION_WORKFLOWS": "0xbe39E1C756e921BD25DF86e7AAa31106d1eb0424",
}

def compile_contract():
    """Compile the AvaCharacter contract"""
    print("\nCompiling contract...")
    
    # Install specific Solidity version if not installed
    solcx.install_solc('0.8.20')
    solcx.set_solc_version('0.8.20')
    
    # Compile contract
    contract_path = os.path.join(os.path.dirname(__file__), 'contracts/src/AvaCharacter.sol')
    base_path = os.path.dirname(__file__)
    
    # Compile with remappings
    compilation_result = solcx.compile_files(
        [contract_path],
        output_values=['abi', 'bin'],
        base_path=base_path,
        allow_paths=[base_path, os.path.join(base_path, "node_modules")],
        import_remappings=[f'@openzeppelin/contracts={os.path.join(base_path, "node_modules/@openzeppelin/contracts")}']
    )
    
    contract_id = f"{contract_path}:AvaCharacter"
    return compilation_result[contract_id]

def upload_to_pinata(data):
    """Upload data to IPFS via Pinata"""
    try:
        url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('PINATA_JWT')}"
        }
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()["IpfsHash"]
    except Exception as e:
        print(f"Error uploading to Pinata: {e}")
        raise

def debug_transaction(receipt):
    """Debug a transaction receipt"""
    print("\nTransaction Receipt Debug:")
    print(f"Status: {'Success' if receipt['status'] == 1 else 'Failed'}")
    print(f"Block Number: {receipt['blockNumber']}")
    print(f"Gas Used: {receipt['gasUsed']}")
    print("\nLogs:")
    for idx, log in enumerate(receipt['logs']):
        print(f"\nLog {idx}:")
        print(f"Address: {log['address']}")
        print(f"Topics: {[topic.hex() for topic in log['topics']]}")
        print(f"Data: {log['data']}")

def register_ava_ip():
    """Register Ava's character as an IP on Story Protocol"""
    try:
        print("\nInitializing registration...")
        print(f"Account address: {account.address}")

        # Compile contract
        compilation_output = compile_contract()
        contract_abi = compilation_output['abi']
        contract_bytecode = compilation_output['bin']

        # Deploy AvaCharacter contract
        print("\nDeploying AvaCharacter contract...")
        AvaCharacter = w3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
        
        # Estimate gas for deployment
        gas_estimate = AvaCharacter.constructor().estimate_gas({'from': account.address})
        print(f"Estimated gas for deployment: {gas_estimate}")

        # Create deployment transaction
        deploy_tx = AvaCharacter.constructor().build_transaction({
            'from': account.address,
            'nonce': w3.eth.get_transaction_count(account.address),
            'gas': int(gas_estimate * 1.2),  # Add 20% buffer
            'maxFeePerGas': w3.eth.max_priority_fee + (2 * w3.eth.get_block('latest')['baseFeePerGas']),
            'maxPriorityFeePerGas': w3.eth.max_priority_fee,
        })

        # Sign and send deployment transaction
        signed_tx = w3.eth.account.sign_transaction(deploy_tx, account.key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"Deployment transaction hash: {tx_hash.hex()}")

        # Wait for deployment receipt
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        contract_address = tx_receipt['contractAddress']
        print(f"AvaCharacter contract deployed at: {contract_address}")

        # Initialize contract instance
        ava_character = w3.eth.contract(address=contract_address, abi=contract_abi)

        # Prepare NFT metadata
        nft_metadata = {
            "name": "Ava Asher - The NFT Artist",
            "description": "Ava is a crypto-native digital artist who lives for the fusion of AI and Web3.",
            "external_url": "https://twitter.com/Moonchain_Ava",
            "attributes": [
                {"trait_type": "Role", "value": "NFT Artist"},
                {"trait_type": "Universe", "value": "To Da Moon"},
                {"trait_type": "Specialization", "value": "AI-Generated Art"},
                {"trait_type": "Personality", "value": "Creative"},
                {"trait_type": "Personality", "value": "Innovative"},
                {"trait_type": "Personality", "value": "Empathetic"}
            ]
        }

        # Upload NFT metadata to IPFS
        nft_metadata_hash = upload_to_pinata(nft_metadata)
        nft_metadata_url = f"ipfs://{nft_metadata_hash}"
        print(f"NFT Metadata uploaded to IPFS: {nft_metadata_url}")

        # Mint NFT
        print("\nMinting NFT...")
        mint_tx = ava_character.functions.mint(
            account.address,
            nft_metadata_url
        ).build_transaction({
            'from': account.address,
            'nonce': w3.eth.get_transaction_count(account.address),
            'gas': 500000,
            'maxFeePerGas': w3.eth.max_priority_fee + (2 * w3.eth.get_block('latest')['baseFeePerGas']),
            'maxPriorityFeePerGas': w3.eth.max_priority_fee,
        })

        # Sign and send mint transaction
        signed_tx = w3.eth.account.sign_transaction(mint_tx, account.key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"Mint transaction hash: {tx_hash.hex()}")

        # Wait for mint receipt
        mint_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        debug_transaction(mint_receipt)

        # Get token ID from mint event
        transfer_event = ava_character.events.Transfer().process_receipt(mint_receipt)[0]
        token_id = transfer_event.args.tokenId
        print(f"NFT minted with token ID: {token_id}")

        # Prepare IP metadata
        ip_metadata = {
            "title": "Ava Asher - The NFT Artist@To Da Moon",
            "description": "Ava is a crypto-native digital artist who lives for the fusion of AI and Web3. She believes that blockchain is a canvas, and NFTs are more than just collectibles - they're a movement.",
            "createdAt": "",
            "creators": [],
            "bio": [
                "Ava is a crypto-native digital artist who lives for the fusion of AI and Web3. She believes that blockchain is a canvas, and NFTs are more than just collectibles - they're a movement.",
                "AI artist in Web3 | NFTs = digital soul | Exploring generative art, surreal dreamscapes & memetic culture",
                "Ava is a character in the To Da Moon simulation where 6 AI agents interact with each other in a simulation shaping the next digital renaissance."
            ],
            "lore": [
                "Generates daily AI art and generate creative and artistic images",
                "Uses emojis and AI generated video by Luma API to express herself",
                "Creates pixel art style videos for her tweets to give them a retro-crypto aesthetic",
                "Loves debating 'Is AI art real art?'",
                "Critique art from @zora",
                "Relies on an AI generator to augment her NFT designs",
                "Post on thoughts about daily simulation results from TO Da Moon Simulation on Gitbook"
            ],
            "knowledge": [
                "AI-generated art (DALL-E, Stable Diffusion, ComfyUI)",
                "Generate AI videos using Luma API with pixel art style",
                "Follow @Zora and @opensea to critique on the latest NFT launches",
                "AI-assisted animation/video (HeyGen, RunwayML)",
                "NFT minting processes (ERC-721, ERC-1155) and metadata standards",
                "Smart contract best practices for digital art provenance and royalty splits"
            ]
        }

        # Upload IP metadata to IPFS
        ip_metadata_hash = upload_to_pinata(ip_metadata)
        ip_metadata_url = f"ipfs://{ip_metadata_hash}"
        print(f"IP Metadata uploaded to IPFS: {ip_metadata_url}")

        # Initialize IP Asset Registry contract
        ip_asset_registry = w3.eth.contract(
            address=Web3.to_checksum_address(ADDRESSES['IP_ASSET_REGISTRY']),
            abi=[{
                "inputs": [
                    {"internalType": "uint256", "name": "chainId", "type": "uint256"},
                    {"internalType": "address", "name": "tokenContract", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "register",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "nonpayable",
                "type": "function"
            }]
        )

        # Register IP
        print("\nRegistering IP...")
        register_tx = ip_asset_registry.functions.register(
            11155111,  # Sepolia chain ID
            contract_address,
            token_id
        ).build_transaction({
            'from': account.address,
            'nonce': w3.eth.get_transaction_count(account.address),
            'gas': 500000,
            'maxFeePerGas': w3.eth.max_priority_fee + (2 * w3.eth.get_block('latest')['baseFeePerGas']),
            'maxPriorityFeePerGas': w3.eth.max_priority_fee,
        })

        # Sign and send registration transaction
        signed_tx = w3.eth.account.sign_transaction(register_tx, account.key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"Registration transaction hash: {tx_hash.hex()}")

        # Wait for registration receipt
        registration_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        debug_transaction(registration_receipt)

        # Get IP ID from registration
        ip_id = ip_asset_registry.functions.ipId(
            11155111,  # Sepolia chain ID
            contract_address,
            token_id
        ).call()

        print(f"""
        Successfully registered Ava's character as an IP!
        Contract Address: {contract_address}
        Token ID: {token_id}
        IP ID: {ip_id}
        IP Metadata IPFS: {ip_metadata_url}
        NFT Metadata IPFS: {nft_metadata_url}
        """)

        # Save the registration info for future reference
        registration_info = {
            'contract_address': contract_address,
            'token_id': token_id,
            'ip_id': ip_id,
            'ip_metadata_url': ip_metadata_url,
            'nft_metadata_url': nft_metadata_url
        }
        with open('ava_registration.json', 'w') as f:
            json.dump(registration_info, f, indent=2)

    except Exception as e:
        print(f"Error registering IP: {e}")
        raise

if __name__ == "__main__":
    register_ava_ip()  # Register Ava's character as an IP
