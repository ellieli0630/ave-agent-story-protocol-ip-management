// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {Script} from "forge-std/Script.sol";
import {console2} from "forge-std/console2.sol";
import {ILicensingModule} from "@storyprotocol/core/interfaces/modules/licensing/ILicensingModule.sol";
import {IPILicenseTemplate} from "@storyprotocol/core/interfaces/modules/licensing/IPILicenseTemplate.sol";
import {IIPAssetRegistry} from "@storyprotocol/core/interfaces/registries/IIPAssetRegistry.sol";
import {ILicenseRegistry} from "@storyprotocol/core/interfaces/registries/ILicenseRegistry.sol";
import {IIPAccount} from "@storyprotocol/core/interfaces/IIPAccount.sol";
import {IERC721} from "@openzeppelin/contracts/token/ERC721/IERC721.sol";

contract AttachLicense is Script {
    // Contract addresses
    address constant AVA_NFT = 0x6b0AF5c02Fefb2d4FC920776D0fEECd00CaD0d4A;
    uint256 constant TOKEN_ID = 0; // Changed from 1 to 0
    uint256 constant CHAIN_ID = 1315; // Story Protocol testnet chain ID
    uint256 constant LICENSE_ID = 571; // License ID from the registration event
    
    // Proxy addresses for all contracts
    IPILicenseTemplate constant PIL_TEMPLATE = IPILicenseTemplate(0x2E896b0b2Fdb7457499B56AAaA4AE55BCB4Cd316); // License proxy
    ILicensingModule constant LICENSING_MODULE = ILicensingModule(0x04fbd8a2e56dd85CFD5500A4A4DfA955B9f1dE6f); // Licensing module proxy
    IIPAssetRegistry constant IP_ASSET_REGISTRY = IIPAssetRegistry(0x77319B4031e6eF1250907aa00018B8B1c67a244b); // IP Asset Registry proxy
    ILicenseRegistry constant LICENSE_REGISTRY = ILicenseRegistry(0x529a750E02d8E2f15649c13D69a465286a780e24); // License Registry proxy
    
    function setUp() public view {
        require(address(PIL_TEMPLATE).code.length > 0, "PIL_TEMPLATE not deployed");
        require(address(LICENSING_MODULE).code.length > 0, "LICENSING_MODULE not deployed");
        require(address(IP_ASSET_REGISTRY).code.length > 0, "IP_ASSET_REGISTRY not deployed");
        require(address(LICENSE_REGISTRY).code.length > 0, "LICENSE_REGISTRY not deployed");
    }
    
    function run() public {
        uint256 privateKey = vm.envUint("PRIVATE_KEY");
        address owner = vm.addr(privateKey);
        vm.startBroadcast(privateKey);

        // Get the IP ID for the NFT
        address ipId = IP_ASSET_REGISTRY.ipId(CHAIN_ID, AVA_NFT, TOKEN_ID);
        require(ipId != address(0), "IP ID not found");
        console2.log("IP ID:", ipId);

        // Check if license terms are already attached
        bool isAttached = LICENSE_REGISTRY.hasIpAttachedLicenseTerms(ipId, address(PIL_TEMPLATE), LICENSE_ID);
        require(!isAttached, "License terms already attached");

        // Get the IP Account instance
        IIPAccount ipAccount = IIPAccount(ipId);
        
        // Approve the licensing module if not already approved
        if (!ipAccount.isModuleApproved(address(LICENSING_MODULE))) {
            ipAccount.setApprovalForModule(address(LICENSING_MODULE), true);
            console2.log("Approved licensing module");
        }

        // Attach the license terms
        LICENSING_MODULE.attachLicenseTerms(ipId, address(PIL_TEMPLATE), LICENSE_ID);
        console2.log("Successfully attached license terms");

        vm.stopBroadcast();
    }
}
