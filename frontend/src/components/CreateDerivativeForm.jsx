import { useState } from 'react';
import { useContractWrite, usePrepareContractWrite, useContractRead } from 'wagmi';
import { parseEther } from 'ethers';
import DerivativeWorksABI from '../../../abis/DerivativeWorks.json';
import '../styles/CreateDerivativeForm.css';

const DERIVATIVE_CONTRACT = "YOUR_DEPLOYED_CONTRACT_ADDRESS"; // We'll update this after deployment

export default function CreateDerivativeForm({ onSuccess }) {
  const [step, setStep] = useState('license'); // 'license' or 'derivative'
  const [licenseId, setLicenseId] = useState(null);
  const [formData, setFormData] = useState({
    title: '',
    imageUrl: '',
    description: '',
    licenseType: 0, // 0 for NonCommercial, 1 for Commercial
    ipfsMetadata: ''
  });

  // Get license fee
  const { data: licenseFee } = useContractRead({
    address: DERIVATIVE_CONTRACT,
    abi: DerivativeWorksABI.abi,
    functionName: 'licenseFee'
  });

  // Get user's existing licenses
  const { data: userLicenses } = useContractRead({
    address: DERIVATIVE_CONTRACT,
    abi: DerivativeWorksABI.abi,
    functionName: 'getHolderLicenses',
    args: [address]
  });

  // Prepare mint license transaction
  const { config: mintConfig } = usePrepareContractWrite({
    address: DERIVATIVE_CONTRACT,
    abi: DerivativeWorksABI.abi,
    functionName: 'mintLicense',
    args: [formData.licenseType],
    value: licenseFee
  });

  // Prepare create derivative transaction
  const { config: createConfig } = usePrepareContractWrite({
    address: DERIVATIVE_CONTRACT,
    abi: DerivativeWorksABI.abi,
    functionName: 'createDerivativeWork',
    args: [
      formData.title,
      formData.imageUrl,
      formData.description,
      formData.ipfsMetadata,
      licenseId
    ]
  });

  const { write: mintLicense, isLoading: isMinting } = useContractWrite({
    ...mintConfig,
    onSuccess: (data) => {
      setLicenseId(data.events[0].args.licenseId);
      setStep('derivative');
    }
  });

  const { write: createDerivative, isLoading: isCreating } = useContractWrite({
    ...createConfig,
    onSuccess: () => {
      if (onSuccess) onSuccess();
    }
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (step === 'license' && mintLicense) {
      mintLicense();
    } else if (step === 'derivative' && createDerivative) {
      createDerivative();
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleExistingLicense = (selectedLicenseId) => {
    setLicenseId(selectedLicenseId);
    setStep('derivative');
  };

  return (
    <form onSubmit={handleSubmit} className="create-derivative-form">
      <h2>{step === 'license' ? 'Get a License' : 'Create Derivative Work'}</h2>
      
      {step === 'license' && (
        <>
          {userLicenses?.length > 0 && (
            <div className="existing-licenses">
              <h3>Your Existing Licenses</h3>
              <div className="licenses-grid">
                {userLicenses.map((license) => (
                  <button
                    key={license}
                    type="button"
                    onClick={() => handleExistingLicense(license)}
                    className="license-button"
                  >
                    License #{license.toString()}
                  </button>
                ))}
              </div>
              <div className="or-divider">OR</div>
            </div>
          )}

          <div className="form-group">
            <label htmlFor="licenseType">License Type</label>
            <select
              id="licenseType"
              name="licenseType"
              value={formData.licenseType}
              onChange={handleInputChange}
            >
              <option value={0}>Non-Commercial</option>
              <option value={1}>Commercial</option>
            </select>
          </div>

          <div className="fee-info">
            License Fee: {licenseFee ? parseEther(licenseFee.toString()) : '0'} ETH
          </div>

          <button 
            type="submit" 
            disabled={!mintLicense || isMinting}
            className={isMinting ? 'loading' : ''}
          >
            {isMinting ? 'Minting License...' : 'Mint License'}
          </button>
        </>
      )}

      {step === 'derivative' && (
        <>
          <div className="license-info">
            Using License #{licenseId?.toString()}
          </div>

          <div className="form-group">
            <label htmlFor="title">Title</label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleInputChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="imageUrl">Image URL (IPFS)</label>
            <input
              type="text"
              id="imageUrl"
              name="imageUrl"
              value={formData.imageUrl}
              onChange={handleInputChange}
              placeholder="ipfs://..."
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="description">Description</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="ipfsMetadata">IPFS Metadata URI (Optional)</label>
            <input
              type="text"
              id="ipfsMetadata"
              name="ipfsMetadata"
              value={formData.ipfsMetadata}
              onChange={handleInputChange}
              placeholder="ipfs://..."
            />
          </div>

          <button 
            type="submit" 
            disabled={!createDerivative || isCreating}
            className={isCreating ? 'loading' : ''}
          >
            {isCreating ? 'Creating...' : 'Create Derivative Work'}
          </button>
        </>
      )}
    </form>
  );
}
