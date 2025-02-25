// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {Test} from "forge-std/Test.sol";
import {RegisterLicenseTerms} from "../script/RegisterLicenseTerms.s.sol";
import {IPILicenseTemplate} from "protocol-core-v1/interfaces/modules/licensing/IPILicenseTemplate.sol";
import {PILTerms} from "protocol-core-v1/interfaces/modules/licensing/IPILicenseTemplate.sol";

contract RegisterLicenseTermsTest is Test {
    RegisterLicenseTerms internal register;
    IPILicenseTemplate internal constant PIL_TEMPLATE = IPILicenseTemplate(0x2E896b0b2Fdb7457499B56AAaA4AE55BCB4Cd316);
    address internal constant ROYALTY_POLICY_LAP = 0xBe54FB168b3c982b7AaE60dB6CF75Bd8447b390E;
    address internal constant MERC20 = 0xF2104833d386a2734a4eB3B8ad6FC6812F29E38E;

    function setUp() public {
        register = new RegisterLicenseTerms();
    }

    function test_registerPILTerms() public {
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

        // Register the terms
        uint256 licenseId = PIL_TEMPLATE.registerLicenseTerms(pilTerms);

        // Verify registration
        assertTrue(licenseId > 0, "License terms not registered correctly");

        // Get the terms and verify
        PILTerms memory registeredTerms = PIL_TEMPLATE.getLicenseTerms(licenseId);
        assertEq(registeredTerms.defaultMintingFee, 0.01 ether, "Wrong minting fee");
        assertEq(registeredTerms.currency, MERC20, "Wrong currency");
        assertEq(registeredTerms.commercialAttribution, true, "Should require attribution");
        assertEq(registeredTerms.commercialUse, true, "Should allow commercial use");
        assertEq(registeredTerms.derivativesAllowed, true, "Should allow derivatives");
    }
}
