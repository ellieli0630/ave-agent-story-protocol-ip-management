// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Script.sol";
import "forge-std/console.sol";
import "../contracts/lib/protocol-core-v1/contracts/interfaces/modules/licensing/IPILicenseTemplate.sol";

interface IIPAssetRegistry {
    function ipId(uint256 chainId, address tokenContract, uint256 tokenId) external view returns (address);
}

interface ILicensingModule {
    function attachLicenseTerms(address ipId, address template, uint256 termsId) external;
    function getLicenseTermsIds(address ipId) external view returns (uint256[] memory);
}

interface IPILFlavors {
    function getOrCreateCCBYTerms(address template) external returns (uint256);
}

contract SetupAvaTermsScript is Script {
    address constant IP_ASSET_REGISTRY = 0x77319B4031e6eF1250907aa00018B8B1c67a244b;
    address constant LICENSING_MODULE = 0x04fbd8a2e56dd85CFD5500A4A4DfA955B9f1dE6f;
    address constant PIL_TEMPLATE = 0x2E896b0b2Fdb7457499B56AAaA4AE55BCB4Cd316;
    address constant AVA_CHARACTER = 0x6b0AF5c02Fefb2d4FC920776D0fEECd00CaD0d4A;
    address constant PIL_FLAVORS = 0xC2Cc3f8a57995C51976c0666d4Dbbf0f178E9E0E;
    address constant ZERO_ADDRESS = address(0);
    bytes constant EMPTY_BYTES = "";

    function run() external {
        uint256 deployerPrivateKey = vm.envUint("STORY_WALLET_PRIVATE_KEY");
        vm.startBroadcast(deployerPrivateKey);

        // Get Ava's IP ID
        IIPAssetRegistry registry = IIPAssetRegistry(IP_ASSET_REGISTRY);
        address avaIpId = registry.ipId(block.chainid, AVA_CHARACTER, 0);
        require(avaIpId != address(0), "IP not registered");
        console.log("Found Ava's IP ID:", avaIpId);

        // Check existing license terms
        ILicensingModule licensingModule = ILicensingModule(LICENSING_MODULE);
        uint256[] memory existingTerms = licensingModule.getLicenseTermsIds(avaIpId);
        
        if (existingTerms.length > 0) {
            console.log("IP already has license terms attached. Terms ID:", existingTerms[0]);
            
            // Get terms details
            try IPILicenseTemplate(PIL_TEMPLATE).getLicenseTerms(existingTerms[0]) returns (PILTerms memory registeredTerms) {
                console.log("Terms Details:");
                console.log("- Transferable:", registeredTerms.transferable);
                console.log("- Royalty Policy:", registeredTerms.royaltyPolicy);
                console.log("- Minting Fee:", registeredTerms.defaultMintingFee);
                console.log("- Commercial Use:", registeredTerms.commercialUse);
                console.log("- Commercial Attribution:", registeredTerms.commercialAttribution);
                console.log("- Derivatives Allowed:", registeredTerms.derivativesAllowed);
                console.log("- Derivatives Attribution:", registeredTerms.derivativesAttribution);
                console.log("- Derivatives Reciprocal:", registeredTerms.derivativesReciprocal);
                console.log("- License URI:", registeredTerms.uri);
            } catch {
                console.log("Could not fetch terms details");
            }
        } else {
            console.log("No license terms attached to IP yet");

            // Create new CC BY terms
            PILTerms memory terms = PILTerms({
                transferable: true,
                royaltyPolicy: ZERO_ADDRESS,
                defaultMintingFee: 0,
                expiration: 0,
                commercialUse: true,
                commercialAttribution: true,
                commercializerChecker: ZERO_ADDRESS,
                commercializerCheckerData: EMPTY_BYTES,
                commercialRevShare: 0,
                commercialRevCeiling: 0,
                derivativesAllowed: true,
                derivativesAttribution: true,
                derivativesApproval: false,
                derivativesReciprocal: true,
                derivativeRevCeiling: 0,
                currency: ZERO_ADDRESS,
                uri: "ipfs://QmccBPKZqhGwqZ7XgLCxGQAYzEJXaQHVGKqMxqYPW7siAo"
            });

            try IPILicenseTemplate(PIL_TEMPLATE).registerLicenseTerms(terms) returns (uint256 termsId) {
                console.log("Created new CC-BY terms with ID:", termsId);

                // Attach the terms to Ava's IP
                try licensingModule.attachLicenseTerms(avaIpId, PIL_TEMPLATE, termsId) {
                    console.log("Successfully attached license terms to Ava's IP");
                } catch {
                    console.log("Failed to attach license terms");
                }
            } catch {
                console.log("Failed to create license terms");
            }
        }

        vm.stopBroadcast();
    }
}
