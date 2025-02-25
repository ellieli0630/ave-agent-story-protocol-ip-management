const hre = require("hardhat");
const { create } = require('ipfs-http-client');
const pinataSDK = require('@pinata/sdk');
require('dotenv').config();

async function uploadToIPFS(metadata) {
  const pinata = new pinataSDK({ pinataJWTKey: process.env.PINATA_JWT });
  const result = await pinata.pinJSONToIPFS(metadata);
  return `ipfs://${result.IpfsHash}`;
}

async function main() {
  // Get the deployed contract address from command line arguments
  const contractAddress = process.argv[2];
  if (!contractAddress) {
    throw new Error("Please provide the deployed contract address");
  }

  // Connect to the deployed contract
  const AvaCharacter = await hre.ethers.getContractFactory("AvaCharacter");
  const avaCharacter = AvaCharacter.attach(contractAddress);

  // Prepare NFT metadata
  const nftMetadata = {
    name: "Ava Asher - The NFT Artist",
    description: "Ava is a crypto-native digital artist who lives for the fusion of AI and Web3.",
    external_url: "https://twitter.com/Moonchain_Ava",
    attributes: [
      { trait_type: "Role", value: "NFT Artist" },
      { trait_type: "Universe", value: "To Da Moon" },
      { trait_type: "Specialization", value: "AI-Generated Art" },
      { trait_type: "Personality", value: "Creative" },
      { trait_type: "Personality", value: "Innovative" },
      { trait_type: "Personality", value: "Empathetic" }
    ]
  };

  // Upload NFT metadata to IPFS
  console.log("Uploading NFT metadata to IPFS...");
  const nftMetadataUrl = await uploadToIPFS(nftMetadata);
  console.log(`NFT Metadata uploaded to: ${nftMetadataUrl}`);

  // Mint NFT
  console.log("Minting NFT...");
  const mintTx = await avaCharacter.mint(await avaCharacter.signer.getAddress(), nftMetadataUrl);
  const mintReceipt = await mintTx.wait();
  
  // Get token ID from mint event
  const transferEvent = mintReceipt.logs.find(
    log => log.topics[0] === hre.ethers.id("Transfer(address,address,uint256)")
  );
  const tokenId = hre.ethers.getBigInt(transferEvent.topics[3]);
  console.log(`NFT minted with token ID: ${tokenId}`);

  // Prepare IP metadata
  const ipMetadata = {
    title: "Ava Asher - The NFT Artist@To Da Moon",
    description: "Ava is a crypto-native digital artist who lives for the fusion of AI and Web3. She believes that blockchain is a canvas, and NFTs are more than just collectibles - they're a movement.",
    createdAt: "",
    creators: [],
    bio: [
      "Ava is a crypto-native digital artist who lives for the fusion of AI and Web3. She believes that blockchain is a canvas, and NFTs are more than just collectibles - they're a movement.",
      "AI artist in Web3 | NFTs = digital soul | Exploring generative art, surreal dreamscapes & memetic culture",
      "Ava is a character in the To Da Moon simulation where 6 AI agents interact with each other in a simulation shaping the next digital renaissance."
    ],
    lore: [
      "Generates daily AI art and generate creative and artistic images",
      "Uses emojis and AI generated video by Luma API to express herself",
      "Creates pixel art style videos for her tweets to give them a retro-crypto aesthetic",
      "Loves debating 'Is AI art real art?'",
      "Critique art from @zora",
      "Relies on an AI generator to augment her NFT designs",
      "Post on thoughts about daily simulation results from TO Da Moon Simulation on Gitbook"
    ],
    knowledge: [
      "AI-generated art (DALL-E, Stable Diffusion, ComfyUI)",
      "Generate AI videos using Luma API with pixel art style",
      "Follow @Zora and @opensea to critique on the latest NFT launches",
      "AI-assisted animation/video (HeyGen, RunwayML)",
      "NFT minting processes (ERC-721, ERC-1155) and metadata standards",
      "Smart contract best practices for digital art provenance and royalty splits"
    ]
  };

  // Upload IP metadata to IPFS
  console.log("Uploading IP metadata to IPFS...");
  const ipMetadataUrl = await uploadToIPFS(ipMetadata);
  console.log(`IP Metadata uploaded to: ${ipMetadataUrl}`);

  // Connect to IP Asset Registry
  const ipAssetRegistry = await hre.ethers.getContractAt(
    "IIPAssetRegistry",
    "0x77319B4031e6eF1250907aa00018B8B1c67a244b"
  );

  // Register IP
  console.log("Registering IP...");
  const registerTx = await ipAssetRegistry.register(
    11155111, // Sepolia chain ID
    contractAddress,
    tokenId
  );
  await registerTx.wait();

  // Get IP ID
  const ipId = await ipAssetRegistry.ipId(11155111, contractAddress, tokenId);
  console.log(`Successfully registered IP with ID: ${ipId}`);

  // Save registration info
  const fs = require('fs');
  const registrationInfo = {
    contract_address: contractAddress,
    token_id: tokenId.toString(),
    ip_id: ipId,
    ip_metadata_url: ipMetadataUrl,
    nft_metadata_url: nftMetadataUrl
  };
  fs.writeFileSync('ava_registration.json', JSON.stringify(registrationInfo, null, 2));
  console.log("Registration info saved to ava_registration.json");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
