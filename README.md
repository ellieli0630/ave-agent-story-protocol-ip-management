# Story Protocol Tracker

A web application for tracking and registering derivative works for Ava's IP on Story Protocol.

## Features

- View Ava's original IP details
- Register new derivative works (fan art)
- Upload images to IPFS
- Connect with Story Protocol smart contracts
- Track derivative works and their creators

## Tech Stack

- Frontend: React + Vite
- Blockchain: Story Protocol (Chain ID: 1315)
- Wallet: RainbowKit
- Storage: IPFS (Pinata)
- Styling: Custom CSS

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/ellieli0630/story-protocol-tracker.git
cd story-protocol-tracker
```

2. Install dependencies:
```bash
cd frontend
npm install
```

3. Create a `.env` file in the root directory with your configuration:
```env
STORY_RPC_URL=your_rpc_url
PINATA_API_KEY=your_pinata_key
PINATA_SECRET_KEY=your_pinata_secret
```

4. Start the development server:
```bash
npm run dev
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── IPDetails.jsx    # Original IP and derivatives display
│   │   └── ...
│   ├── styles/
│   │   ├── IPDetails.css    # Component styles
│   │   └── ...
│   ├── utils/
│   │   └── format.js        # Utility functions
│   ├── App.jsx             # Main application component
│   └── config.js           # Configuration
└── package.json
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Story Protocol for the smart contract infrastructure
- RainbowKit for the wallet connection UI
- Pinata for IPFS hosting
