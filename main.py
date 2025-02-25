import os
import secrets
import json
from dotenv import load_dotenv
from web3 import Web3
import tweepy
from crontab import CronTab
from contracts.abis import (
    IP_ASSET_REGISTRY_ABI,
    LICENSING_MODULE_ABI,
    PIL_TEMPLATE_ABI,
    ADDRESSES
)

# Load environment variables
load_dotenv()

# Initialize Web3
w3 = Web3(Web3.HTTPProvider(os.getenv('STORY_RPC_URL')))
account = w3.eth.account.from_key(os.getenv('STORY_WALLET_PRIVATE_KEY'))

# Initialize contracts
ip_asset_registry = w3.eth.contract(
    address=Web3.to_checksum_address(ADDRESSES['IP_ASSET_REGISTRY']),
    abi=IP_ASSET_REGISTRY_ABI
)

licensing_module = w3.eth.contract(
    address=Web3.to_checksum_address(ADDRESSES['LICENSING_MODULE']),
    abi=LICENSING_MODULE_ABI
)

pil_template = w3.eth.contract(
    address=Web3.to_checksum_address(ADDRESSES['PIL_TEMPLATE']),
    abi=PIL_TEMPLATE_ABI
)

# Initial IP metadata
initial_ip = {
    "name": "Devin - The DeFi Trading AI",
    "description": "Devin is a sophisticated AI agent in the 'To Da Moon' simulation ecosystem, where AI agents interact and audiences predict storyline developments. As a DeFi trading expert, Devin operates both within and outside the simulation, analyzing market trends, identifying trading opportunities, and sharing insights with his growing community of followers.",
    "image": "ipfs://Qmc5m94Gu7z62RC8waSKkZUrCCBJPyHbkpmGzEePxy2oXJ",
    "attributes": {
        "role": "DeFi Trading Expert",
        "universe": "To Da Moon",
        "personality": "Confident, analytical, and slightly eccentric",
        "expertise": "DeFi trading, market analysis, risk management",
        "special_abilities": [
            "Real-time market analysis",
            "Cross-chain arbitrage detection",
            "Risk-adjusted strategy optimization",
            "Natural language market commentary"
        ]
    }
}

def register_initial_ip():
    """Register the initial IP on Story Protocol"""
    try:
        # Generate random token ID
        token_id = secrets.randbits(256)
        
        # Prepare metadata
        ip_metadata = {
            "title": "Story Protocol Twitter Tracker",
            "description": "A project that tracks derivative works from a Twitter account",
            "mediaUrl": f"https://twitter.com/{os.getenv('TWITTER_USERNAME')}",
            "mediaType": "text/plain",
            "creators": [
                {
                    "name": "Story Protocol Twitter Tracker",
                    "address": account.address,
                    "description": "A bot that tracks derivative works on Twitter",
                    "contributionPercent": 100,
                    "socialMedia": [
                        {
                            "platform": "Twitter",
                            "url": f"https://twitter.com/{os.getenv('TWITTER_USERNAME')}"
                        }
                    ]
                }
            ]
        }
        
        # Convert metadata to hash
        ip_metadata_hash = Web3.keccak(text=json.dumps(ip_metadata))
        
        # Build transaction to register the IP
        tx = ip_asset_registry.functions.register(
            11155111,  # Sepolia chain ID
            account.address,  # Using our address as the NFT contract since we don't have a real NFT yet
            token_id  # Using our random token ID
        ).build_transaction({
            'from': account.address,
            'nonce': w3.eth.get_transaction_count(account.address),
            'gas': 500000,
            'maxFeePerGas': w3.eth.max_priority_fee + (2 * w3.eth.get_block('latest')['baseFeePerGas']),
            'maxPriorityFeePerGas': w3.eth.max_priority_fee,
        })

        # Sign and send transaction
        signed_tx = w3.eth.account.sign_transaction(tx, account.key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"Initial IP registration tx hash: {tx_hash.hex()}")

        # Wait for transaction receipt
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Initial IP registration receipt: {receipt}")

        # For now, we'll use a random address as the IP ID
        # In production, you would want to properly decode the event logs
        ip_id = account.address
        print(f"IP ID: {ip_id}")

        # Register license terms
        license_terms_tx = pil_template.functions.registerLicenseTerms((
            0,  # minting fee
            10 * 10**6,  # 10% commercial rev share
            Web3.to_checksum_address(ADDRESSES['ROYALTY_POLICY_LAP']),
            Web3.to_checksum_address(ADDRESSES['WIP'])
        )).build_transaction({
            'from': account.address,
            'nonce': w3.eth.get_transaction_count(account.address),
            'gas': 500000,
            'maxFeePerGas': w3.eth.max_priority_fee + (2 * w3.eth.get_block('latest')['baseFeePerGas']),
            'maxPriorityFeePerGas': w3.eth.max_priority_fee,
        })

        # Sign and send transaction
        signed_tx = w3.eth.account.sign_transaction(license_terms_tx, account.key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        license_terms_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        # For now, use a random number as license terms ID
        license_terms_id = secrets.randbits(256)
        print(f"License Terms ID: {license_terms_id}")

        # Attach license terms
        attach_tx = licensing_module.functions.attachLicenseTerms(
            ip_id,
            Web3.to_checksum_address(ADDRESSES['PIL_TEMPLATE']),
            license_terms_id
        ).build_transaction({
            'from': account.address,
            'nonce': w3.eth.get_transaction_count(account.address),
            'gas': 500000,
            'maxFeePerGas': w3.eth.max_priority_fee + (2 * w3.eth.get_block('latest')['baseFeePerGas']),
            'maxPriorityFeePerGas': w3.eth.max_priority_fee,
        })

        # Sign and send transaction
        signed_tx = w3.eth.account.sign_transaction(attach_tx, account.key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print("License terms attached successfully")

        return ip_id, license_terms_id

    except Exception as e:
        print(f"Error registering initial IP: {e}")
        raise

def monitor_twitter(ip_id, license_terms_id):
    """Monitor Twitter for relevant tweets and register derivatives"""
    try:
        # Initialize Twitter client
        client = tweepy.Client(
            consumer_key=os.getenv('TWITTER_API_KEY'),
            consumer_secret=os.getenv('TWITTER_API_SECRET'),
            access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
            access_token_secret=os.getenv('TWITTER_ACCESS_SECRET')
        )

        # Get user's tweets
        tweets = client.get_users_tweets(
            os.getenv('TWITTER_USERNAME'),
            exclude=['retweets', 'replies'],
            max_results=10
        )

        keywords = ['defi', 'trading', 'market', 'analysis', 'crypto']
        
        for tweet in tweets.data or []:
            if any(keyword in tweet.text.lower() for keyword in keywords):
                print(f"Found relevant tweet: {tweet.text}")
                # Register derivative work for this tweet
                register_derivative(ip_id, license_terms_id, tweet.text, tweet.id)

    except Exception as e:
        print(f"Error monitoring Twitter: {e}")

def register_derivative(parent_ip_id, license_terms_id, tweet_text, tweet_id):
    """Register a derivative work for a tweet"""
    try:
        # Implementation of derivative registration
        # This would follow a similar pattern to register_initial_ip
        # but use the appropriate derivative registration functions
        pass

    except Exception as e:
        print(f"Error registering derivative: {e}")

def main():
    try:
        # Register initial IP
        ip_id, license_terms_id = register_initial_ip()
        print(f"Successfully registered initial IP with ID: {ip_id}")
        print(f"License terms ID: {license_terms_id}")

        # Monitor Twitter immediately
        monitor_twitter(ip_id, license_terms_id)

        # Set up cron job for monitoring
        cron = CronTab(user=True)
        job = cron.new(command=f'python {os.path.abspath(__file__)} --monitor {ip_id} {license_terms_id}')
        job.minute.every(15)
        cron.write()

    except Exception as e:
        print(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()
