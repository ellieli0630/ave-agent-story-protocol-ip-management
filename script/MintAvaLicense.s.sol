// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Script.sol";
import "../contracts/interfaces/IIPAssetRegistry.sol";
import "../contracts/interfaces/ILicenseRegistry.sol";
import "../contracts/interfaces/ILicensingModule.sol";
import "../contracts/interfaces/IPILicenseTemplate.sol";
import "../contracts/interfaces/ILicenseToken.sol";
import "../contracts/lib/PILFlavors.sol";
import "../contracts/lib/PILTypes.sol";
import "../contracts/src/AvaCharacter.sol";
import "../contracts/mocks/MockIPGraph.sol";

contract MintAvaLicenseScript is Script {
    // Story Protocol testnet addresses
    address constant IP_ASSET_REGISTRY = 0x77319B4031e6eF1250907aa00018B8B1c67a244b;
    address constant LICENSING_MODULE = 0x04fbd8a2e56dd85CFD5500A4A4DfA955B9f1dE6f;
    address constant PIL_TEMPLATE = 0x2E896b0b2Fdb7457499B56AAaA4AE55BCB4Cd316;
    address constant LICENSE_TOKEN = 0xFe3838BFb30B34170F00030B52eA4893d8aAC6bC;
    address constant ROYALTY_POLICY_LAP = 0xBe54FB168b3c982b7AaE60dB6CF75Bd8447b390E;
    address constant MERC20 = 0xF2104833d386a2734a4eB3B8ad6FC6812F29E38E;
    
    // Ava's NFT contract from previous deployment
    address constant AVA_CHARACTER = 0x6b0AF5c02Fefb2d4FC920776D0fEECd00CaD0d4A;
    
    // IPFS metadata hash for fan art
    string constant FANART_METADATA = "ipfs://QmY4ZpyCxnBBssyqHKKwwJ1uam5pbMBKZgfjtVXSDY5qpY";

    address constant zeroAddress = address(0);
    bytes constant EMPTY_BYTES = "";

    function run() external {
        uint256 deployerPrivateKey = vm.envUint("STORY_WALLET_PRIVATE_KEY");
        address deployer = vm.addr(deployerPrivateKey);

        // Mock IPGraph precompile
        vm.etch(address(0x0101), address(new MockIPGraph()).code);

        vm.startBroadcast(deployerPrivateKey);

        // Step 1: Get Ava's IP ID
        IIPAssetRegistry registry = IIPAssetRegistry(IP_ASSET_REGISTRY);
        address avaIpId = registry.ipId(block.chainid, AVA_CHARACTER, 0);
        require(avaIpId != address(0), "IP not registered");
        console.log("Found Ava's IP ID:", avaIpId);

        // Step 2: Set Approvals
        AvaCharacter avaCharacter = AvaCharacter(AVA_CHARACTER);
        avaCharacter.setApprovalForAll(LICENSING_MODULE, true);
        avaCharacter.setApprovalForAll(LICENSE_TOKEN, true);
        console.log("Set approvals for licensing");

        // Step 3: Create CC BY license terms
        PILTypes.PILTerms memory terms = PILTypes.PILTerms({
            transferable: true,
            royaltyPolicy: zeroAddress,
            mintingFee: 0,
            attribution: true
        });

        // Step 4: Register the license terms
        IPILicenseTemplate pilTemplate = IPILicenseTemplate(PIL_TEMPLATE);
        uint256 termsId;
        try pilTemplate.registerLicenseTerms(terms) returns (uint256 newTermsId) {
            termsId = newTermsId;
            console.log("Successfully registered new license terms with ID:", termsId);
        } catch Error(string memory reason) {
            console.log("Failed to register license terms:", reason);
            revert("Failed to register license terms");
        }

        // Step 5: Attach the license terms to the IP
        ILicensingModule licensingModule = ILicensingModule(LICENSING_MODULE);
        try licensingModule.attachLicenseTerms(avaIpId, PIL_TEMPLATE, termsId) {
            console.log("Successfully attached license terms with ID:", termsId);
        } catch Error(string memory reason) {
            console.log("Failed to attach terms:", reason);
            // Continue anyway as terms might already be attached
        }

        // Step 6: Mint License Token with zero fees
        try licensingModule.mintLicenseTokens({
            licensorIpId: avaIpId,
            licenseTemplate: PIL_TEMPLATE,
            licenseTermsId: termsId,
            amount: 1,
            receiver: deployer,
            royaltyContext: "",
            maxMintingFee: 0,
            maxRevenueShare: 0
        }) returns (uint256 licenseTokenId) {
            console.log("Successfully minted license token with ID:", licenseTokenId);

            // Step 7: Register Fan Art as Derivative Work
            try registry.register(
                block.chainid,
                LICENSE_TOKEN,
                licenseTokenId
            ) returns (address fanArtIpId) {
                console.log("Successfully registered fan art IP with ID:", fanArtIpId);
            } catch Error(string memory reason) {
                console.log("Failed to register fan art:", reason);
            } catch {
                console.log("Failed to register fan art with unknown error");
            }
        } catch Error(string memory reason) {
            console.log("Failed to mint license token:", reason);
        } catch {
            console.log("Failed to mint license token with unknown error");
        }

        vm.stopBroadcast();
    }
}
