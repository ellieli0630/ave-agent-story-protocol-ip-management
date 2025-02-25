import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def upload_to_ipfs():
    jwt = os.getenv('PINATA_JWT')
    if not jwt:
        raise ValueError("PINATA_JWT environment variable not set")

    headers = {
        'Authorization': f'Bearer {jwt}',
        'Content-Type': 'application/json'
    }

    # Character metadata
    character_metadata = {
        "name": "Ava Asher - The NFT Artist",
        "description": "Ava is a crypto-native digital artist who lives for the fusion of AI and Web3.",
        "external_url": "https://twitter.com/Moonchain_Ava",
        "image": "https://bafybeihpjhkeuiq3k6nqa3fkgeigeri2qnkn7nbjbwzxqe5vqdmyvtvs5i.ipfs.nftstorage.link/1.png",
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
        ],
        "attributes": [
            {
                "trait_type": "Character Type",
                "value": "NFT Artist"
            },
            {
                "trait_type": "Simulation",
                "value": "To Da Moon"
            }
        ],
        "created_at": datetime.utcnow().isoformat()
    }

    # Terms of use metadata
    terms_metadata = {
        "name": "Ava Character Terms of Use",
        "description": "Terms governing the use of Ava character IP in the To Da Moon simulation",
        "terms": [
            "1. Attribution required - Must credit 'Ava Asher from To Da Moon'",
            "2. Non-commercial use only without explicit permission",
            "3. Derivative works must maintain character integrity and core traits",
            "4. Must respect the character's role as an AI artist and NFT creator",
            "5. Any use must align with Web3 and crypto-native culture"
        ]
    }

    # Upload character metadata with name
    character_response = requests.post(
        'https://api.pinata.cloud/pinning/pinJSONToIPFS',
        headers=headers,
        json={
            "pinataContent": character_metadata,
            "pinataMetadata": {
                "name": "Ava_Character_Metadata"
            }
        }
    )
    character_result = character_response.json()
    print(f"Character metadata IPFS hash: {character_result['IpfsHash']}")

    # Upload terms metadata with name
    terms_response = requests.post(
        'https://api.pinata.cloud/pinning/pinJSONToIPFS',
        headers=headers,
        json={
            "pinataContent": terms_metadata,
            "pinataMetadata": {
                "name": "Ava_Terms_of_Use"
            }
        }
    )
    terms_result = terms_response.json()
    print(f"Terms metadata IPFS hash: {terms_result['IpfsHash']}")

    return character_result['IpfsHash'], terms_result['IpfsHash']

if __name__ == "__main__":
    character_hash, terms_hash = upload_to_ipfs()
