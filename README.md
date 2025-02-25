# Ava IP on Story Protocol

This repository demonstrates how to register and license an IP (Ava Asher - The NFT Artist) from To Da Moon where 6 AI agents interact with each other in a simulation (Demo here https://crypto-city-client.web.app/) on Story Protocol using their SDK and smart contracts.

## Overview

This project showcases:
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
