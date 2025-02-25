// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Script.sol";
import "forge-std/console.sol";

interface IIPAssetRegistry {
    function ipId(uint256 chainId, address tokenContract, uint256 tokenId) external view returns (address);
}

interface ILicensingModule {
    function getLicenseTerms(address ipId, address template) external view returns (uint256);
}

interface IPILicenseTemplate {
    function licenseTerms(uint256 termsId) external view returns (
        bool transferable,
        address royaltyPolicy,
        uint256 mintingFee,
        bool attribution
    );
}

contract CheckAvaTermsScript is Script {
    // Story Protocol testnet addresses
    address constant IP_ASSET_REGISTRY = 0x77319B4031e6eF1250907aa00018B8B1c67a244b;
    address constant LICENSING_MODULE = 0x04fbd8a2e56dd85CFD5500A4A4DfA955B9f1dE6f;
    address constant PIL_TEMPLATE = 0x2E896b0b2Fdb7457499B56AAaA4AE55BCB4Cd316;
    address constant AVA_CHARACTER = 0x6b0AF5c02Fefb2d4FC920776D0fEECd00CaD0d4A;

    function run() external view {
        // Get Ava's IP ID
        IIPAssetRegistry registry = IIPAssetRegistry(IP_ASSET_REGISTRY);
        address avaIpId = registry.ipId(block.chainid, AVA_CHARACTER, 0);
        require(avaIpId != address(0), "IP not registered");
        console.log("Found Ava's IP ID:", avaIpId);

        // Get licensing info
        ILicensingModule licensingModule = ILicensingModule(LICENSING_MODULE);
        
        // Check if terms are attached
        try licensingModule.getLicenseTerms(avaIpId, PIL_TEMPLATE) returns (uint256 termsId) {
            console.log("Current license terms ID:", termsId);
            
            // Get terms details
            IPILicenseTemplate pilTemplate = IPILicenseTemplate(PIL_TEMPLATE);
            try pilTemplate.licenseTerms(termsId) returns (
                bool transferable,
                address royaltyPolicy,
                uint256 mintingFee,
                bool attribution
            ) {
                console.log("Terms Details:");
                console.log("- Transferable:", transferable);
                console.log("- Royalty Policy:", royaltyPolicy);
                console.log("- Minting Fee:", mintingFee);
                console.log("- Attribution Required:", attribution);
            } catch {
                console.log("Could not fetch terms details");
            }
        } catch {
            console.log("No license terms attached to Ava's IP");
        }
    }
}
