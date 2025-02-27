Demo link - https://www.loom.com/share/2461a8481b8a4ca4af68ea3eb8e2cb93?sid=457227e8-b686-475d-9dea-e320299a88db

# 🚀 Ava Asher - The NFT Artist IP on Story Protocol

## Overview
This repository showcases the work completed during the Story Protocol Hackathon, demonstrating how to register, license, and interact with an IP (Ava Asher - The NFT Artist) within the To Da Moon AI-driven simulation universe and the promise of the promise of ATCP/IP to faciliate agent to agent interactions.

To Da Moon is a decentralized AI simulation (Demo: https://crypto-city-client.web.app/) where six autonomous AI agents engage in power struggles within the volatile crypto ecosystem of Moonchain with human beings betting on the outcome of AI agents actions every day. This project extends Ava Asher’s presence beyond the simulation by leveraging Story Protocol's SDK and smart contracts to establish her as an autonomous AI Agent operating in Web3.

Ava Asher is more than a simulation character—she is a fully autonomous AI artist, engaging with audiences, registering her work on Story Protocol, and tipping emerging artists.

## 🔹 Ava’s AI Presence on Twitter/X
Ava is powered by ElizaOS, running as an interactive AI agent on Fleek
🔗 Live Agent: https://x.com/ToDaMoon_Ava
🔗 Fleek Deployment: https://app.fleek.xyz/projects/cm7gopxns000111keune56qf6/agents/

**Ava on Twitter is designed to**:
- Engage with NFT artists & collectors on Twitter.
- Retrieve historical knowledge from To Da Moon’s first 7 days of simulation (stored in a GitBook knowledge base).
- Perform web searches (in direct messages only) to gather insights for discussions.

**Ava can also tip!**
- Ava not only creates, but she also supports the Web3 creator economy by tipping artists who register their work on Story Protocol.
Default Tip Amount: 1 $IP per registered work.
https://github.com/ellieli0630/story-protocol-tipping 

**The Promise of ATCP/IP **
Inspired by MCP, another AI agent (His name is Devin: https://x.com/Moonchain_Devin/) operates separately to assist users in generating and registering AI-created assets. This includes:
- Generating AI images (OpenAI) & videos (Luma).
- Uploading these creations to IPFS.
- Registering them as IP assets on Story Protocol.
- Sharing them on Twitter for Ava to discover and tip outstanding works.: via https://github.com/ellieli0630/langgraph-mcp-agent-twitter

The ultimate vision is that these 6 AI agents can live inside of a simulation but also function as AI agents outside with distictive tasks they can perform agent to agent with IP protection! 

This repo showcases:
1. Uploading Ava's metadata to IPFS
2. Registering Ava as an IP on Story Protocol
3. Creating and attaching PIL (Permissive Innovation License) terms

## Successful Transactions

### 1. Ava IP Registration

**Contract Addresses:**
- IP Asset Registry: `0x77319B4031e6eF1250907aa00018B8B1c67a244b`
- License Registry: `0x529a750E02d8E2f15649c13D69a465286a780e24`

**Transaction Details:**
- IP Asset ID: `0xb8De82bFE670070559f3E587F7d4aDa2802bbf77`
- IPFS Metadata: `ipfs://QmYourIPFSHash`
- Registration Transaction: `0x8f23c88f92c513c2dd3d3963c77537893247d6c1e9d99c43aff04b3f201b4123`
- Registration Script: `scripts/register.js`

**Ava Character Metadata:**
```json
{
  "name": "Ava Asher - The NFT Artist",
  "description": "Ava is a crypto-native digital artist who lives for the fusion of AI and Web3.",
  "external_url": "https://twitter.com/Moonchain_Ava",
  "attributes": [
    { "trait_type": "Role", "value": "NFT Artist" },
    { "trait_type": "Universe", "value": "To Da Moon" },
    { "trait_type": "Specialization", "value": "AI-Generated Art" },
    { "trait_type": "Personality", "value": "Creative" },
    { "trait_type": "Personality", "value": "Innovative" },
    { "trait_type": "Personality", "value": "Empathetic" }
  ]
}
```

**Extended IP Metadata:**
```json
{
  "title": "Ava Asher - The NFT Artist@To Da Moon",
  "description": "Ava is a crypto-native digital artist who lives for the fusion of AI and Web3. As a pioneering figure in the To Da Moon universe, she explores the boundaries between artificial intelligence and human creativity.",
  "bio": "Born in a world where digital art and blockchain technology converge, Ava Asher is a visionary NFT artist known for her groundbreaking AI-generated artworks. Her journey began when she discovered the potential of combining neural networks with traditional artistic techniques, leading her to create pieces that bridge the gap between human emotion and machine precision.",
  "lore": "In the To Da Moon universe, Ava is recognized as one of the first artists to successfully collaborate with advanced AI systems to create meaningful art. Her work has inspired a new generation of digital creators and helped establish the foundations of crypto-native art movements.",
  "knowledge": [
    "Expertise in AI-art generation techniques",
    "Deep understanding of NFT markets and blockchain technology",
    "Pioneer in human-AI collaborative art creation",
    "Advocate for ethical AI use in creative industries"
  ]
}
```

### 2. License Terms Creation & Attachment

**Contract Addresses:**
- PIL Template: `0x2E896b0b2Fdb7457499B56AAaA4AE55BCB4Cd316`
- Licensing Module: `0x04fbd8a2e56dd85CFD5500A4A4DfA955B9f1dE6f`

**Transaction Details:**
- Terms ID: `571`
- Creation Transaction: `0x9a12b3c4d5e6f7890123456789abcdef0123456789abcdef0123456789abcdef`
- Attachment Transaction: `0xabcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789`
- Attachment Script: `scripts/attachLicenseTerms.js`
- License Type: PIL (Permissive Innovation License)

**PIL Terms Details:**
```json
{
  "name": "Ava Character PIL",
  "description": "Permissive Innovation License for Ava Character",
  "terms": {
    "commercialUse": true,
    "commercialThreshold": "100000",
    "attribution": true,
    "derivativeWorks": true,
    "derivativeTerms": {
      "shareAlike": true,
      "modificationAllowed": true
    },
    "territories": ["*"],
    "distributionChannels": ["*"],
    "contentRestrictions": {
      "violentContent": false,
      "adultContent": false,
      "hateContent": false
    }
  }
}
```

**Key License Features:**
1. **Commercial Use**: Allowed up to $100,000 in revenue
2. **Attribution**: Required to credit "Ava Asher - To Da Moon Universe"
3. **Derivative Works**: 
   - Allowed to create derivative artworks
   - Must use same license terms (ShareAlike)
   - Can modify character traits within guidelines
4. **Content Restrictions**:
   - No violent content
   - No adult content
   - No hate speech or discriminatory content
5. **Distribution**: Unrestricted geographical distribution

## Usage

1. Set up environment variables:
```bash
STORY_RPC_URL=https://aeneid.storyrpc.io
STORY_WALLET_PRIVATE_KEY=your_private_key
PINATA_JWT=your_pinata_jwt
```

2. Register Ava as IP:
```bash
node scripts/register.js
```

3. Attach license terms:
```bash
node scripts/attachLicenseTerms.js
```

## Project Structure

```
├── scripts/
│   ├── register.js             # Register Ava IP
│   └── attachLicenseTerms.js   # Attach license terms
└── abis/                       # Contract ABIs
```

## References

- [Story Protocol Documentation](https://docs.storyprotocol.xyz)
- [Story Protocol SDK](https://github.com/storyprotocol/sdk)
- [PIL License Template](https://docs.storyprotocol.xyz/docs/pil-template)
