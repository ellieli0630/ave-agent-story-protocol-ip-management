import { useState, useEffect } from 'react';
import { formatAddress, formatDate } from '../utils/format';
import '../styles/IPDetails.css';

const IPFS_GATEWAY = 'https://ipfs.io/ipfs/';
const AVA_CREATOR = "0xb8De82bFE670070559f3E587F7d4aDa2802bbf77";
const AVA_IPFS_HASH = "QmYqA9uqHhKgJ9LZqKgSyY5w5JZ8kbvNqHLEqkxZyZY5Zj"; // Replace with actual IPFS hash

function IPDetails() {
  const [ipDetails, setIpDetails] = useState({
    name: "Ava",
    description: "Ava is a digital native character who embodies the spirit of web3. Born in the metaverse, she's a curious and adventurous soul exploring the frontiers of digital innovation. With her signature blue hair and vibrant personality, Ava bridges the gap between traditional storytelling and blockchain technology.",
    avatar: "https://raw.githubusercontent.com/storyprotocol/my-story-pf/main/assets/ava.png",
    creator: AVA_CREATOR,
    createdAt: "2024-01-15T00:00:00Z",
    license: "CC BY 4.0",
    tags: ["character", "digital native", "web3", "metaverse"],
    socialLinks: {
      twitter: "https://x.com/ToDaMoon_Ava",
      website: "https://story-protocol.xyz"
    },
    traits: [
      { name: "Personality", value: "Adventurous, Curious, Tech-savvy" },
      { name: "Appearance", value: "Blue hair, Digital-inspired outfit" },
      { name: "Background", value: "Born in the metaverse" },
      { name: "Mission", value: "Exploring web3 storytelling" }
    ]
  });

  const [derivatives, setDerivatives] = useState([]);

  // Fetch IPFS metadata
  useEffect(() => {
    const fetchIpfsMetadata = async () => {
      try {
        const response = await fetch(`${IPFS_GATEWAY}${AVA_IPFS_HASH}`);
        const metadata = await response.json();
        setIpDetails(prevDetails => ({
          ...prevDetails,
          ...metadata
        }));
      } catch (error) {
        console.error('Failed to fetch IPFS metadata:', error);
      }
    };

    fetchIpfsMetadata();
  }, []);

  // Fetch derivatives from contract
  useEffect(() => {
    // Mock data - replace with actual contract call
    setDerivatives([
      {
        id: 1,
        title: "Ava in Cyberpunk City",
        creator: "0xabcd...1234",
        createdAt: new Date().toISOString(),
        imageUrl: "ipfs://Qm...",
        ipfsUrl: "https://ipfs.io/ipfs/Qm...",
        description: "Ava exploring a neon-lit cyberpunk cityscape"
      }
    ]);
  }, []);

  return (
    <div className="ip-details-container">
      <div className="original-ip">
        <div className="original-ip-header">
          <div className="avatar-container">
            <img src={ipDetails.avatar} alt="Ava" />
          </div>
          <div className="ip-info">
            <h1 className="ip-title">{ipDetails.name}</h1>
            <p className="ip-description">{ipDetails.description}</p>
          </div>
        </div>
        
        <div className="ip-metadata">
          <div className="metadata-item">
            <div className="metadata-label">Creator</div>
            <div className="metadata-value">{formatAddress(ipDetails.creator)}</div>
          </div>
          <div className="metadata-item">
            <div className="metadata-label">Created</div>
            <div className="metadata-value">{formatDate(ipDetails.createdAt)}</div>
          </div>
          <div className="metadata-item">
            <div className="metadata-label">License</div>
            <div className="metadata-value">{ipDetails.license}</div>
          </div>
          <div className="metadata-item">
            <div className="metadata-label">Tags</div>
            <div className="metadata-value">{ipDetails.tags.join(', ')}</div>
          </div>
          <div className="metadata-item">
            <div className="metadata-label">Social</div>
            <div className="metadata-value social-links">
              <a href={ipDetails.socialLinks.twitter} target="_blank" rel="noopener noreferrer" className="social-link">
                <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                  <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
                </svg>
                X (Twitter)
              </a>
              <a href={ipDetails.socialLinks.website} target="_blank" rel="noopener noreferrer" className="social-link">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="10"/>
                  <path d="M2 12h20"/>
                  <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
                </svg>
                Website
              </a>
            </div>
          </div>
        </div>

        <div className="character-traits">
          <h2 className="traits-title">Character Traits</h2>
          <div className="traits-grid">
            {ipDetails.traits.map((trait, index) => (
              <div key={index} className="trait-item">
                <div className="trait-label">{trait.name}</div>
                <div className="trait-value">{trait.value}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="derivatives-section">
        <h2 className="derivatives-title">Derivative Works</h2>
        <div className="derivatives-grid">
          {derivatives.map((derivative) => (
            <div key={derivative.id} className="derivative-card">
              <img 
                src={derivative.imageUrl?.replace('ipfs://', IPFS_GATEWAY)} 
                alt={derivative.title}
                className="derivative-image"
              />
              <div className="derivative-info">
                <h3 className="derivative-title">{derivative.title}</h3>
                <div className="derivative-metadata">
                  <div>
                    <span className="metadata-label">Creator:</span>
                    <span className="metadata-value">{formatAddress(derivative.creator)}</span>
                  </div>
                  <div>
                    <span className="metadata-label">Created:</span>
                    <span className="metadata-value">{formatDate(derivative.createdAt)}</span>
                  </div>
                  <div>
                    <span className="metadata-label">Description:</span>
                    <p className="metadata-value">{derivative.description}</p>
                  </div>
                  <a 
                    href={derivative.ipfsUrl} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="derivative-link"
                  >
                    View on IPFS
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                      <polyline points="15 3 21 3 21 9"></polyline>
                      <line x1="10" y1="14" x2="21" y2="3"></line>
                    </svg>
                  </a>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default IPDetails;
