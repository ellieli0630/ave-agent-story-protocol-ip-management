import dotenv from 'dotenv';
import { ethers } from 'ethers';
import cron from 'node-cron';
import { TwitterApi } from 'twitter-api-v2';
import { 
  IP_ASSET_REGISTRY_ABI, 
  LICENSING_MODULE_ABI, 
  PIL_TEMPLATE_ABI,
  ADDRESSES 
} from './contracts/abis.js';

dotenv.config();

// Initialize provider and wallet
const provider = new ethers.JsonRpcProvider(process.env.STORY_RPC_URL);
const wallet = new ethers.Wallet(process.env.STORY_WALLET_PRIVATE_KEY, provider);

// Initialize contracts
const ipAssetRegistry = new ethers.Contract(
  ADDRESSES.IP_ASSET_REGISTRY,
  IP_ASSET_REGISTRY_ABI,
  wallet
);

const licensingModule = new ethers.Contract(
  ADDRESSES.LICENSING_MODULE,
  LICENSING_MODULE_ABI,
  wallet
);

const pilTemplate = new ethers.Contract(
  ADDRESSES.PIL_TEMPLATE,
  PIL_TEMPLATE_ABI,
  wallet
);

// Initial IP metadata
const initialIP = {
  name: "Devin - The DeFi Trading AI",
  description: "Devin is a sophisticated AI agent in the 'To Da Moon' simulation ecosystem, where AI agents interact and audiences predict storyline developments. As a DeFi trading expert, Devin operates both within and outside the simulation, analyzing market trends, identifying trading opportunities, and sharing insights with his growing community of followers.",
  image: "ipfs://Qmc5m94Gu7z62RC8waSKkZUrCCBJPyHbkpmGzEePxy2oXJ",
  attributes: {
    role: "DeFi Trading Expert",
    universe: "To Da Moon",
    personality: "Confident, analytical, and slightly eccentric",
    expertise: "DeFi trading, market analysis, risk management",
    special_abilities: [
      "Real-time market analysis",
      "Cross-chain arbitrage detection",
      "Risk-adjusted strategy optimization",
      "Natural language market commentary"
    ]
  }
};

// Function to register initial IP
async function registerInitialIP() {
  try {
    // Register IP using the IP Asset Registry contract
    const tx = await ipAssetRegistry.register(
      11155111, // chainId (11155111 for Sepolia testnet)
      wallet.address, // token contract address (using wallet address as placeholder)
      ethers.hexlify(ethers.randomBytes(32)) // random tokenId
    );

    console.log('Initial IP registration transaction:', tx);
    const receipt = await tx.wait();
    console.log('Initial IP registered:', receipt);

    // For now, let's use a temporary IP ID since we can't get it from the receipt
    // In production, you would want to properly decode the event logs
    const ipId = "0x" + receipt.hash.slice(2, 42);
    console.log('IP ID:', ipId);

    // Register license terms
    const licenseTermsTx = await pilTemplate.registerLicenseTerms({
      mintingFee: 0,
      commercialRevShare: ethers.parseUnits("10", 6), // 10%
      royaltyPolicy: ADDRESSES.ROYALTY_POLICY_LAP,
      currencyToken: ADDRESSES.WIP
    });

    const licenseTermsReceipt = await licenseTermsTx.wait();
    // For now, use a temporary license terms ID
    const licenseTermsId = ethers.hexlify(ethers.randomBytes(32));
    console.log('License Terms ID:', licenseTermsId);

    // Attach license terms to the IP
    const attachTx = await licensingModule.attachLicenseTerms(ipId, ADDRESSES.PIL_TEMPLATE, licenseTermsId);
    await attachTx.wait();
    console.log('License terms attached successfully');

    return { ipId, licenseTermsId };
  } catch (error) {
    console.error('Error registering initial IP:', error);
    throw error;
  }
}

// Function to register derivative work
async function registerDerivativeWork(parentIpId, tweetContent, licenseTermsId) {
  try {
    // First mint a license token
    const mintTx = await licensingModule.mintLicenseTokens({
      licensorIpId: parentIpId,
      licenseTemplate: ADDRESSES.PIL_TEMPLATE,
      licenseTermsId: licenseTermsId,
      amount: 1,
      receiver: wallet.address,
      royaltyContext: "",
      maxMintingFee: 0,
      maxRevenueShare: 0
    });

    const mintReceipt = await mintTx.wait();
    const licenseTokenId = mintReceipt.events[0].args.tokenId;

    // Register new IP for the derivative
    const registerTx = await ipAssetRegistry.register(
      11155111, // chainId
      wallet.address, // token contract
      ethers.hexlify(ethers.randomBytes(32)) // random tokenId
    );

    const registerReceipt = await registerTx.wait();
    const childIpId = registerReceipt.events.find(e => e.event === "IPRegistered").args.ipId;

    // Register as derivative
    const derivativeTx = await licensingModule.registerDerivativeWithLicenseTokens({
      childIpId: childIpId,
      licenseTokenIds: [licenseTokenId],
      royaltyContext: "",
      maxRts: 0
    });

    const derivativeReceipt = await derivativeTx.wait();
    console.log('Derivative work registered:', derivativeReceipt);

    return childIpId;
  } catch (error) {
    console.error('Error registering derivative work:', error);
    throw error;
  }
}

// Keywords to track
const KEYWORDS = ['defi', 'trading', 'market', 'analysis', 'crypto'];

// Function to check if tweet contains relevant keywords
function containsRelevantKeywords(tweetText) {
  return KEYWORDS.some(keyword => tweetText.toLowerCase().includes(keyword));
}

// Function to monitor Twitter and register derivative works
async function monitorTwitterAndRegisterDerivatives(parentIpId, licenseTermsId) {
  try {
    const twitterClient = new TwitterApi({
      appKey: process.env.TWITTER_API_KEY,
      appSecret: process.env.TWITTER_API_SECRET,
      accessToken: process.env.TWITTER_ACCESS_TOKEN,
      accessSecret: process.env.TWITTER_ACCESS_SECRET,
    });

    const tweets = await twitterClient.v2.userByUsername(process.env.TWITTER_USERNAME);
    const userId = tweets.data.id;
    
    const timeline = await twitterClient.v2.userTimeline(userId, {
      exclude: ['retweets', 'replies'],
      max_results: 10
    });

    for (const tweet of timeline.data.data) {
      if (containsRelevantKeywords(tweet.text)) {
        console.log('Found relevant tweet:', tweet.text);
        await registerDerivativeWork(parentIpId, tweet.text, licenseTermsId);
      }
    }
  } catch (error) {
    console.error('Error monitoring Twitter:', error);
  }
}

// Main execution
async function main() {
  try {
    // First register the initial IP and get the IP ID and license terms ID
    const { ipId, licenseTermsId } = await registerInitialIP();
    console.log('Successfully registered initial IP with ID:', ipId);
    console.log('License terms ID:', licenseTermsId);

    // Then start monitoring Twitter every 15 minutes
    cron.schedule('*/15 * * * *', async () => {
      console.log('Running scheduled Twitter check...');
      await monitorTwitterAndRegisterDerivatives(ipId, licenseTermsId);
    });

    // Also run the first check immediately
    await monitorTwitterAndRegisterDerivatives(ipId, licenseTermsId);
  } catch (error) {
    console.error('Error in main execution:', error);
  }
}

main().catch(console.error);
