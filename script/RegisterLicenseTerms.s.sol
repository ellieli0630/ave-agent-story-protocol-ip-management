// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {Script} from "forge-std/Script.sol";
import {IPILicenseTemplate} from "@storyprotocol/core/interfaces/modules/licensing/IPILicenseTemplate.sol";
import {PILTerms} from "@storyprotocol/core/interfaces/modules/licensing/IPILicenseTemplate.sol";

contract RegisterLicenseTerms is Script {
    // Ava's IP NFT contract address
    address constant AVA_IP = 0x6b0af5c02fefb2d4fc920776d0feecd00cad0d4a;
    
    // Story Protocol Contract Addresses
    IPILicenseTemplate constant PIL_TEMPLATE = IPILicenseTemplate(0x2E896b0b2Fdb7457499B56AAaA4AE55BCB4Cd316);
    address constant ROYALTY_POLICY_LAP = 0xBe54FB168b3c982b7AaE60dB6CF75Bd8447b390E;
    address constant MERC20 = 0xF2104833d386a2734a4eB3B8ad6FC6812F29E38E;

    function run() public {
        // Create CC BY-like PIL Terms
        PILTerms memory pilTerms = PILTerms({
            transferable: true,                // License can be transferred
            royaltyPolicy: ROYALTY_POLICY_LAP, // Use LAP policy
            defaultMintingFee: 0.01 ether,     // 0.01 IP tokens to mint
            expiration: 0,                     // No expiration
            commercialUse: true,               // Allow commercial use (CC BY)
            commercialAttribution: true,       // Require attribution (CC BY)
            commercializerChecker: address(0), // No additional checks
            commercializerCheckerData: "",     // No checker data
            commercialRevShare: 0,             // No revenue share
            commercialRevCeiling: 0,           // No revenue ceiling
            derivativesAllowed: true,          // Allow derivatives (CC BY)
            derivativesAttribution: true,      // Require attribution for derivatives (CC BY)
            derivativesApproval: false,        // No approval needed (CC BY)
            derivativesReciprocal: false,      // No reciprocal licensing (CC BY)
            derivativeRevCeiling: 0,           // No derivative revenue ceiling
            currency: MERC20,                  // Use MERC20 token
            uri: "ipfs://QmHash"               // Terms URI (to be replaced)
        });

        vm.startBroadcast();
        
        // Register the PIL Terms
        uint256 licenseTermsId = PIL_TEMPLATE.registerLicenseTerms(pilTerms);
        
        // Verify registration
        uint256 selectedLicenseTermsId = PIL_TEMPLATE.getLicenseTermsId(pilTerms);
        require(licenseTermsId == selectedLicenseTermsId, "License terms not registered correctly");

        vm.stopBroadcast();
    }
}
