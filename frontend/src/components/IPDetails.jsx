import { useState, useEffect } from 'react';
import { useContractRead, useAccount, useContractReads } from 'wagmi';
import { ethers } from 'ethers';
import { formatAddress, formatDate } from '../utils/format';
import '../styles/IPDetails.css';

const IPFS_GATEWAY = 'https://ipfs.io/ipfs/';
const AVA_CONTRACT = "0x04fbd8a2e56dd85CFD5500A4A4DfA955B9f1dE6f";
const IP_REGISTRY = "0x77319B4031e6eF1250907aa00018B8B1c67a244b";
const LICENSING_FRAMEWORK = "0x04fbd8a2e56dd85CFD5500A4A4DfA955B9f1dE6f";
const STORY_PROTOCOL_EXPLORER = "https://testnet.storyprotocol.xyz";

// Import ABIs
import AvaCharacterABI from '../../../abis/AvaCharacter.json';
import IPAssetRegistryABI from '../../../abis/IPAssetRegistry.json';

function IPDetails() {
  const { address } = useAccount();
  const [ipDetails, setIpDetails] = useState({
    name: "Ava",
    description: "Loading...",
    avatar: "https://raw.githubusercontent.com/storyprotocol/my-story-pf/main/assets/ava.png",
    creator: null,
    createdAt: null,
    license: "CC BY 4.0",
    tags: [],
    socialLinks: {
      twitter: "https://x.com/ToDaMoon_Ava",
      website: "https://story-protocol.xyz"
    }
  });

  const [derivatives, setDerivatives] = useState([]);
  const [isLoadingDerivatives, setIsLoadingDerivatives] = useState(true);

  // Read Ava's metadata from the contract
  const { data: avaMetadata } = useContractRead({
    address: AVA_CONTRACT,
    abi: AvaCharacterABI.abi,
    functionName: 'tokenURI',
    args: [1], // Assuming Ava is token ID 1
  });

  // Read IP registration details
  const { data: ipRegistration } = useContractRead({
    address: IP_REGISTRY,
    abi: IPAssetRegistryABI.abi,
    functionName: 'getIPAccount',
    args: [AVA_CONTRACT],
  });

  // Get the IP ID for Ava
  const { data: avaIpId } = useContractRead({
    address: IP_REGISTRY,
    abi: IPAssetRegistryABI.abi,
    functionName: 'ipId',
    args: [1, AVA_CONTRACT, 1], // chainId, tokenContract, tokenId
  });

  // Fetch IPFS metadata when available
  useEffect(() => {
    if (avaMetadata) {
      const fetchMetadata = async () => {
        try {
          const ipfsHash = avaMetadata.replace('ipfs://', '');
          const response = await fetch(`${IPFS_GATEWAY}${ipfsHash}`);
          const metadata = await response.json();
          
          setIpDetails(prevDetails => ({
            ...prevDetails,
            ...metadata,
            creator: ipRegistration?.owner || prevDetails.creator,
            createdAt: ipRegistration?.createdAt ? new Date(ipRegistration.createdAt * 1000).toISOString() : prevDetails.createdAt
          }));
        } catch (error) {
          console.error('Failed to fetch IPFS metadata:', error);
        }
      };

      fetchMetadata();
    }
  }, [avaMetadata, ipRegistration]);

  // Fetch derivative works
  useEffect(() => {
    const fetchDerivatives = async () => {
      if (!avaIpId) return;

      try {
        setIsLoadingDerivatives(true);
        
        // In a real implementation, we would query the Story Protocol contracts
        // to get the list of derivative works. For now, we'll use a placeholder
        // that demonstrates the UI structure.
        const mockDerivatives = [
          {
            id: 1,
            title: "Ava's Digital Adventure",
            creator: "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
            createdAt: "2025-02-20T00:00:00Z",
            imageUrl: `${IPFS_GATEWAY}QmYqA9uqHhKgJ9LZqKgSyY5w5JZ8kbvNqHLEqkxZyZY5Zj`,
            description: "A digital comic series featuring Ava exploring the metaverse",
            licenseType: "Commercial",
            status: "Approved"
          },
          {
            id: 2,
            title: "Ava in Web3 Wonderland",
            creator: "0x123d35Cc6634C0532925a3b844Bc454e4438f456",
            createdAt: "2025-02-22T00:00:00Z",
            imageUrl: `${IPFS_GATEWAY}QmYqA9uqHhKgJ9LZqKgSyY5w5JZ8kbvNqHLEqkxZyZY5Zk`,
            description: "An interactive story where Ava guides users through Web3 concepts",
            licenseType: "Non-Commercial",
            status: "Pending"
          }
        ];

        setDerivatives(mockDerivatives);
      } catch (error) {
        console.error('Failed to fetch derivatives:', error);
      } finally {
        setIsLoadingDerivatives(false);
      }
    };

    fetchDerivatives();
  }, [avaIpId]);

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
            <div className="metadata-value">{ipDetails.creator ? formatAddress(ipDetails.creator) : 'Loading...'}</div>
          </div>
          <div className="metadata-item">
            <div className="metadata-label">Created</div>
            <div className="metadata-value">{ipDetails.createdAt ? formatDate(ipDetails.createdAt) : 'Loading...'}</div>
          </div>
          <div className="metadata-item">
            <div className="metadata-label">Contract</div>
            <div className="metadata-value">
              <a 
                href={`https://testnet.storyprotocol.xyz/address/${AVA_CONTRACT}`} 
                target="_blank" 
                rel="noopener noreferrer" 
                className="metadata-link"
              >
                {formatAddress(AVA_CONTRACT)}
              </a>
            </div>
          </div>
          <div className="metadata-item">
            <div className="metadata-label">License</div>
            <div className="metadata-value">{ipDetails.license}</div>
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

        {ipDetails.attributes && (
          <div className="character-traits">
            <h2 className="traits-title">Character Traits</h2>
            <div className="traits-grid">
              {ipDetails.attributes.map((trait, index) => (
                <div key={index} className="trait-item">
                  <div className="trait-label">{trait.trait_type}</div>
                  <div className="trait-value">{trait.value}</div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className="derivatives-section">
        <h2 className="derivatives-title">Derivative Works</h2>
        {isLoadingDerivatives ? (
          <div className="loading-message">Loading derivative works...</div>
        ) : derivatives.length === 0 ? (
          <div className="no-derivatives-message">No derivative works found</div>
        ) : (
          <div className="derivatives-grid">
            {derivatives.map((derivative) => (
              <div key={derivative.id} className="derivative-card">
                <div className="derivative-image-container">
                  <img 
                    src={derivative.imageUrl} 
                    alt={derivative.title}
                    className="derivative-image"
                  />
                  <div className={`status-badge ${derivative.status.toLowerCase()}`}>
                    {derivative.status}
                  </div>
                </div>
                <div className="derivative-info">
                  <h3 className="derivative-title">{derivative.title}</h3>
                  <div className="derivative-metadata">
                    <div className="metadata-row">
                      <span className="metadata-label">Creator:</span>
                      <a 
                        href={`${STORY_PROTOCOL_EXPLORER}/address/${derivative.creator}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="metadata-value address-link"
                      >
                        {formatAddress(derivative.creator)}
                      </a>
                    </div>
                    <div className="metadata-row">
                      <span className="metadata-label">Created:</span>
                      <span className="metadata-value">{formatDate(derivative.createdAt)}</span>
                    </div>
                    <div className="metadata-row">
                      <span className="metadata-label">License:</span>
                      <span className="metadata-value">{derivative.licenseType}</span>
                    </div>
                    <div className="metadata-row description">
                      <p className="metadata-value">{derivative.description}</p>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default IPDetails;
