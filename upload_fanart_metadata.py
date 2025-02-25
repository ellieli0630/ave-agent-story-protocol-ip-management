import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def upload_fanart_to_ipfs():
    jwt = os.getenv('PINATA_JWT')
    if not jwt:
        raise ValueError("PINATA_JWT environment variable not set")

    headers = {
        'Authorization': f'Bearer {jwt}',
        'Content-Type': 'application/json'
    }

    # Upload the fan art image first
    with open('to-da-moon-fan-art.png', 'rb') as f:
        files = {
            'file': f
        }
        response = requests.post(
            'https://api.pinata.cloud/pinning/pinFileToIPFS',
            files=files,
            headers={'Authorization': f'Bearer {jwt}'}
        )
        image_result = response.json()
        print(f"Fan art image IPFS hash: {image_result['IpfsHash']}")
        image_url = f"ipfs://{image_result['IpfsHash']}"

    # Fan art metadata
    fanart_metadata = {
        "name": "To Da Moon - Ava Fan Art",
        "description": "Fan art inspired by Ava Asher from the To Da Moon simulation",
        "image": image_url,
        "external_url": "https://twitter.com/Moonchain_Ava",
        "attributes": [
            {
                "trait_type": "Type",
                "value": "Fan Art"
            },
            {
                "trait_type": "Original Character",
                "value": "Ava Asher"
            },
            {
                "trait_type": "Universe",
                "value": "To Da Moon"
            }
        ],
        "created_at": datetime.utcnow().isoformat()
    }

    # Upload fan art metadata
    metadata_response = requests.post(
        'https://api.pinata.cloud/pinning/pinJSONToIPFS',
        headers=headers,
        json={
            "pinataContent": fanart_metadata,
            "pinataMetadata": {
                "name": "To_Da_Moon_Fan_Art_Metadata"
            }
        }
    )
    metadata_result = metadata_response.json()
    print(f"Fan art metadata IPFS hash: {metadata_result['IpfsHash']}")
    return image_result['IpfsHash'], metadata_result['IpfsHash']

if __name__ == "__main__":
    image_hash, metadata_hash = upload_fanart_to_ipfs()
