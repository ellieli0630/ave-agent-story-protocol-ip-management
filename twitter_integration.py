import os
import tweepy
from dotenv import load_dotenv
from web3 import Web3
import json
import requests
from pathlib import Path
import sys
import base64
import hmac
import hashlib
import time
from urllib.parse import quote, urlencode
from datetime import datetime

# Add contracts directory to Python path
sys.path.append(str(Path(__file__).parent))

# Import ABIs
from contracts.abis import (
    IP_ASSET_REGISTRY_ABI,
    LICENSING_MODULE_ABI,
    ADDRESSES
)

load_dotenv()

# Web3 setup
w3 = Web3(Web3.HTTPProvider(os.getenv('STORY_RPC_URL')))
account = w3.eth.account.from_key(os.getenv('STORY_WALLET_PRIVATE_KEY'))

def download_media_from_tweet(tweet):
    """Download media (image or video) from a tweet"""
    try:
        if hasattr(tweet, 'attachments') and tweet.attachments:
            media_keys = tweet.attachments.get('media_keys', [])
            if media_keys:
                # Get media object
                media = tweet.includes['media'][0]
                
                # Handle different media types
                if media.type == 'photo':
                    image_url = media.url
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        return response.content, 'image'
                elif media.type == 'video':
                    # For videos, we'll use the preview image
                    if hasattr(media, 'preview_image_url'):
                        response = requests.get(media.preview_image_url)
                        if response.status_code == 200:
                            return response.content, 'video'
                    # If no preview image, try to get the thumbnail
                    elif hasattr(media, 'thumbnail_url'):
                        response = requests.get(media.thumbnail_url)
                        if response.status_code == 200:
                            return response.content, 'video'
        return None, None
    except Exception as e:
        print(f"Error downloading media: {str(e)}")
        return None, None

def post_tweet(tweet_text):
    """Post a tweet using Twitter API v2"""
    try:
        # Initialize client with OAuth 2.0
        client = tweepy.Client(
            bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
            consumer_key=os.getenv('TWITTER_API_KEY'),
            consumer_secret=os.getenv('TWITTER_API_SECRET'),
            access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
            access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
            wait_on_rate_limit=True
        )
        
        # Post tweet
        response = client.create_tweet(text=tweet_text)
        return response.data['id']

    except Exception as e:
        print(f"Error posting tweet: {str(e)}")
        raise

def process_derivative_registration(tweet):
    """Process a tweet for derivative work registration"""
    try:
        # Check if tweet contains the trigger phrase
        if "registering this as derivative work" in tweet.text.lower():
            print(f"Found derivative work registration request in tweet {tweet.id}")
            
            # Download media from tweet
            media_data, media_type = download_media_from_tweet(tweet)
            if not media_data:
                print("No media found in tweet")
                return
            
            # Get metadata from tweet
            metadata = {
                "name": f"Derivative Work by @{tweet.author.username}",
                "description": tweet.text,
                "tweet_url": f"https://twitter.com/user/status/{tweet.id}",
                "author": tweet.author.username,
                "creation_date": tweet.created_at.isoformat(),
                "media_type": media_type
            }
            
            # Register derivative work using our existing function
            from register_fan_art import register_derivative_work, setup_license_terms, mint_license_token
            
            # Setup license and get token
            parent_ip_id = "0x0AedD694851871614012d67195a6DeE1930682cf"  # Ava's character IP ID
            license_terms_id = setup_license_terms(parent_ip_id)
            license_token_id = mint_license_token(parent_ip_id, license_terms_id)
            
            # Register the derivative work
            derivative_ip_id = register_derivative_work(
                media_data,
                metadata["name"],
                metadata["description"],
                parent_ip_id,
                license_token_id
            )
            
            # Post confirmation tweet
            media_type_emoji = "🎥" if media_type == "video" else "🎨"
            confirmation_tweet = f"""{media_type_emoji} Registered derivative work from @{tweet.author.username}!

View on Story Protocol: https://aeneid.storyscan.xyz/ip/{derivative_ip_id}
Original tweet: https://twitter.com/user/status/{tweet.id}"""
            
            post_tweet(confirmation_tweet)
            
    except Exception as e:
        print(f"Error processing derivative registration: {str(e)}")
        raise

def process_specific_tweet(tweet_id):
    """Process a specific tweet by ID"""
    try:
        # Initialize client with OAuth 2.0
        client = tweepy.Client(
            bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
            consumer_key=os.getenv('TWITTER_API_KEY'),
            consumer_secret=os.getenv('TWITTER_API_SECRET'),
            access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
            access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
            wait_on_rate_limit=True
        )
        
        # Get tweet with expansions
        tweet = client.get_tweet(
            tweet_id,
            expansions=['author_id', 'attachments.media_keys'],
            media_fields=['url', 'type', 'preview_image_url', 'variants']
        )
        
        if tweet and tweet.data:
            print(f"Found tweet: {tweet.data.text}")
            
            # Create a tweet-like object that matches our processing function's expectations
            tweet_data = {
                'text': tweet.data.text,
                'id': tweet.data.id,
                'author': {'username': tweet.includes['users'][0].username},
                'created_at': tweet.data.created_at,
                'attachments': {'media_keys': []},
                'includes': {'media': []}
            }
            
            # Add media information
            if hasattr(tweet, 'includes') and 'media' in tweet.includes:
                tweet_data['includes']['media'] = tweet.includes['media']
            
            # Process the tweet
            process_derivative_registration(tweet_data)
        else:
            print(f"Could not find tweet with ID: {tweet_id}")
            
    except Exception as e:
        print(f"Error processing specific tweet: {str(e)}")
        raise

def start_derivative_listener():
    """Start listening for derivative work registration tweets in real-time"""
    try:
        # Initialize client with OAuth 2.0
        client = tweepy.Client(
            bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
            consumer_key=os.getenv('TWITTER_API_KEY'),
            consumer_secret=os.getenv('TWITTER_API_SECRET'),
            access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
            access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
            wait_on_rate_limit=True
        )
        
        # Create stream
        stream = tweepy.StreamingClient(
            os.getenv('TWITTER_BEARER_TOKEN'),
            wait_on_rate_limit=True
        )
        
        # Add rules
        rule = tweepy.StreamRule(
            'registering this as derivative work from:ToDaMoon_Ava'
        )
        
        # Delete existing rules
        existing_rules = stream.get_rules()
        if existing_rules.data:
            stream.delete_rules([rule.id for rule in existing_rules.data])
            
        # Add our rule
        stream.add_rules(rule)
        
        # Start streaming
        print("Starting real-time stream for derivative work registration...")
        stream.filter(
            expansions=['author_id', 'attachments.media_keys'],
            media_fields=['url', 'type', 'preview_image_url', 'variants']
        )
        
    except Exception as e:
        print(f"Error starting listener: {str(e)}")
        raise

def main():
    """Main function to either start listener or process specific tweet"""
    if len(sys.argv) > 1:
        # If tweet ID is provided, process that specific tweet
        tweet_id = sys.argv[1]
        print(f"Processing specific tweet: {tweet_id}")
        process_specific_tweet(tweet_id)
    else:
        # Otherwise start the real-time listener
        start_derivative_listener()

if __name__ == "__main__":
    main()
