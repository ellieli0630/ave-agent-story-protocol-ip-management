// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {Script} from "forge-std/Script.sol";
import {Vm} from "forge-std/Vm.sol";
import {console2} from "forge-std/console2.sol";
import {IPILicenseTemplate} from "protocol-core-v1/interfaces/modules/licensing/IPILicenseTemplate.sol";
import {PILTerms} from "protocol-core-v1/interfaces/modules/licensing/IPILicenseTemplate.sol";

contract RegisterLicenseTerms is Script {
    // Ava's IP NFT contract address (checksummed)
    address constant AVA_IP = 0x6b0AF5c02Fefb2d4FC920776D0fEECd00CaD0d4A;
    
    // Story Protocol Contract Addresses
    IPILicenseTemplate constant PIL_TEMPLATE = IPILicenseTemplate(0x2E896b0b2Fdb7457499B56AAaA4AE55BCB4Cd316);
    address constant ROYALTY_POLICY_LAP = 0xBe54FB168b3c982b7AaE60dB6CF75Bd8447b390E;
    address constant MERC20 = 0xF2104833d386a2734a4eB3B8ad6FC6812F29E38E;

    function setUp() public {
        // Verify contract addresses exist
        require(address(PIL_TEMPLATE).code.length > 0, "PIL_TEMPLATE not deployed");
        require(ROYALTY_POLICY_LAP.code.length > 0, "ROYALTY_POLICY_LAP not deployed");
        require(MERC20.code.length > 0, "MERC20 not deployed");
    }

    function run() public {
        // Log start of execution
        console2.log("Starting license terms registration...");
        
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
            uri: "ipfs://QmXZQpPxDC3DnzGhVr6yNs8qhzA8mZXJAZCQWAd4i7LJQt"  // Actual IPFS hash
        });

        console2.log("PIL Terms struct created");
        
        vm.startBroadcast();
        
        // Register the PIL Terms with error logging
        console2.log("Attempting to register license terms...");
        uint256 licenseId = PIL_TEMPLATE.registerLicenseTerms(pilTerms);
        console2.log("License terms registered with ID:", licenseId);
        require(licenseId > 0, "License terms not registered correctly");

        vm.stopBroadcast();
    }
}
