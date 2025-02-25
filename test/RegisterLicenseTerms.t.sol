// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {Test} from "forge-std/Test.sol";
import {RegisterLicenseTerms} from "../script/RegisterLicenseTerms.s.sol";
import {IPILicenseTemplate} from "@storyprotocol/core/interfaces/modules/licensing/IPILicenseTemplate.sol";
import {PILTerms} from "@storyprotocol/core/interfaces/modules/licensing/IPILicenseTemplate.sol";

contract RegisterLicenseTermsTest is Test {
    RegisterLicenseTerms internal register;
    IPILicenseTemplate internal constant PIL_TEMPLATE = IPILicenseTemplate(0x2E896b0b2Fdb7457499B56AAaA4AE55BCB4Cd316);
    address internal constant ROYALTY_POLICY_LAP = 0xBe54FB168b3c982b7AaE60dB6CF75Bd8447b390E;
    address internal constant MERC20 = 0xF2104833d386a2734a4eB3B8ad6FC6812F29E38E;

    function setUp() public {
        register = new RegisterLicenseTerms();
    }

    function test_registerPILTerms() public {
        // Create the same PIL Terms as in the script
        PILTerms memory pilTerms = PILTerms({
            transferable: true,
            royaltyPolicy: ROYALTY_POLICY_LAP,
            defaultMintingFee: 0.01 ether,
            expiration: 0,
            commercialUse: true,
            commercialAttribution: true,
            commercializerChecker: address(0),
            commercializerCheckerData: "",
            commercialRevShare: 0,
            commercialRevCeiling: 0,
            derivativesAllowed: true,
            derivativesAttribution: true,
            derivativesApproval: false,
            derivativesReciprocal: false,
            derivativeRevCeiling: 0,
            currency: MERC20,
            uri: "ipfs://QmHash"
        });

        // Register the terms
        uint256 licenseTermsId = PIL_TEMPLATE.registerLicenseTerms(pilTerms);

        // Verify registration
        uint256 selectedLicenseTermsId = PIL_TEMPLATE.getLicenseTermsId(pilTerms);
        assertEq(licenseTermsId, selectedLicenseTermsId, "License terms not registered correctly");

        // Verify terms match what we expect
        PILTerms memory registeredTerms = PIL_TEMPLATE.getLicenseTerms(licenseTermsId);
        assertEq(registeredTerms.defaultMintingFee, 0.01 ether, "Wrong minting fee");
        assertEq(registeredTerms.commercialUse, true, "Should allow commercial use");
        assertEq(registeredTerms.commercialAttribution, true, "Should require attribution");
        assertEq(registeredTerms.derivativesAllowed, true, "Should allow derivatives");
        assertEq(registeredTerms.derivativesAttribution, true, "Should require attribution for derivatives");
    }
}
