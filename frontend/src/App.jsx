import { useState } from 'react'
import { WagmiConfig, createConfig, useAccount, useContractWrite } from 'wagmi'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import {
  RainbowKitProvider,
  ConnectButton,
  getDefaultWallets,
  darkTheme,
} from '@rainbow-me/rainbowkit'
import { createPublicClient, http } from 'viem'
import '@rainbow-me/rainbowkit/styles.css'
import './App.css'
import IPDetails from './components/IPDetails'
import envConfig from './config'

// Contract ABIs and addresses
const IPFS_GATEWAY = 'https://ipfs.io/ipfs/'
const AVA_IP_ID = "0xb8De82bFE670070559f3E587F7d4aDa2802bbf77"

const queryClient = new QueryClient()

// Story Protocol Testnet Chain Configuration
const storyChain = {
  id: 1315,
  name: 'Story Protocol Testnet',
  network: 'story-testnet',
  nativeCurrency: {
    decimals: 18,
    name: 'IP',
    symbol: 'IP',
  },
  rpcUrls: {
    public: { http: [envConfig.STORY_RPC_URL] },
    default: { http: [envConfig.STORY_RPC_URL] },
  },
  blockExplorers: {
    default: { name: 'Explorer', url: 'https://testnet.storyprotocol.xyz' },
  },
  testnet: true,
}

const { wallets } = getDefaultWallets({
  appName: 'Ava Fan Art Registration',
  projectId: 'YOUR_PROJECT_ID', // Get this from WalletConnect Cloud
  chains: [storyChain]
})

const config = createConfig({
  chains: [storyChain],
  transports: {
    [storyChain.id]: http()
  }
})

async function uploadToIPFS(file) {
  try {
    const formData = new FormData()
    formData.append('file', file)

    const response = await fetch('https://api.pinata.cloud/pinning/pinFileToIPFS', {
      method: 'POST',
      headers: {
        'pinata_api_key': envConfig.PINATA_API_KEY,
        'pinata_secret_api_key': envConfig.PINATA_SECRET_KEY
      },
      body: formData
    })

    const data = await response.json()
    if (!data.IpfsHash) {
      throw new Error('Failed to get IPFS hash from Pinata')
    }
    return `ipfs://${data.IpfsHash}`
  } catch (error) {
    console.error('IPFS upload error:', error)
    throw new Error('Failed to upload to IPFS: ' + error.message)
  }
}

function FanArtForm() {
  const [imagePreview, setImagePreview] = useState(null)
  const [status, setStatus] = useState({ message: '', type: '' })
  const { address } = useAccount()

  // Contract write hook for registering derivative work
  const { write: registerDerivative } = useContractWrite({
    address: '0x04fbd8a2e56dd85CFD5500A4A4DfA955B9f1dE6f', // Story Protocol Registry
    abi: [
      {
        name: 'registerDerivative',
        type: 'function',
        stateMutability: 'nonpayable',
        inputs: [
          { name: 'parentIpId', type: 'address' },
          { name: 'metadata', type: 'string' }
        ],
        outputs: [{ name: 'ipId', type: 'address' }]
      }
    ],
    functionName: 'registerDerivative'
  })

  const handleImageChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = (e) => setImagePreview(e.target.result)
      reader.readAsDataURL(file)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!address) {
      setStatus({ message: 'Please connect your wallet first', type: 'error' })
      return
    }

    setStatus({ message: 'Processing submission...', type: 'info' })
    
    try {
      const file = e.target.files[0]
      const title = e.target.title.value
      const description = e.target.description.value

      // 1. Upload image to IPFS
      setStatus({ message: 'Uploading image to IPFS...', type: 'info' })
      const imageUrl = await uploadToIPFS(file)

      // 2. Create and upload metadata
      const metadata = {
        name: title,
        description: description,
        image: imageUrl,
        properties: {
          type: 'fan-art',
          parentIpId: AVA_IP_ID
        }
      }

      setStatus({ message: 'Uploading metadata to IPFS...', type: 'info' })
      const metadataUrl = await uploadToIPFS(
        new Blob([JSON.stringify(metadata)], { type: 'application/json' })
      )

      // 3. Register derivative work
      setStatus({ message: 'Registering derivative work...', type: 'info' })
      await registerDerivative({
        args: [AVA_IP_ID, metadataUrl],
      })

      setStatus({ message: 'Successfully registered your fan art!', type: 'success' })
      e.target.reset()
      setImagePreview(null)
    } catch (error) {
      setStatus({ message: `Error: ${error.message}`, type: 'error' })
    }
  }

  return (
    <div className="registration-section">
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="imageFile">Upload Your Fan Art:</label>
          <input
            type="file"
            id="imageFile"
            accept="image/*"
            onChange={handleImageChange}
            required
          />
          {imagePreview && (
            <div className="image-preview">
              <img src={imagePreview} alt="Preview" />
            </div>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="title">Title:</label>
          <input
            type="text"
            id="title"
            name="title"
            required
            placeholder="Give your fan art a title"
          />
        </div>

        <div className="form-group">
          <label htmlFor="description">Description:</label>
          <textarea
            id="description"
            name="description"
            required
            placeholder="Tell us about your fan art"
          />
        </div>

        <div className="form-group">
          <label>
            <input type="checkbox" id="termsAccept" required />
            I accept the CC BY license terms
          </label>
        </div>

        <button type="submit">Register Fan Art</button>
      </form>

      {status.message && (
        <div className={`status-message ${status.type}`}>
          {status.message}
        </div>
      )}
    </div>
  )
}

function App() {
  return (
    <WagmiConfig config={config}>
      <QueryClientProvider client={queryClient}>
        <RainbowKitProvider chains={[storyChain]} theme={darkTheme()}>
          <div className="container">
            <header>
              <h1>Register Your Ava Fan Art</h1>
              <p>Share your creative work with the Ava community!</p>
              <div className="wallet-section">
                <ConnectButton />
              </div>
            </header>

            <main>
              <IPDetails />
              <FanArtForm />
            </main>
          </div>
        </RainbowKitProvider>
      </QueryClientProvider>
    </WagmiConfig>
  )
}

export default App
