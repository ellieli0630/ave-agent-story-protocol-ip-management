// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Script.sol";
import "../contracts/interfaces/IIPAssetRegistry.sol";
import "../contracts/src/AvaCharacter.sol";

contract DeployAvaIPScript is Script {
    // Story Protocol testnet addresses
    address constant IP_ASSET_REGISTRY = 0x77319B4031e6eF1250907aa00018B8B1c67a244b;

    // IPFS metadata hash
    string constant AVA_METADATA = "ipfs://QmUBYxVcVbXmqUDC38UMMaoWMXSKLgWdgo2qQYLCEk4Xyg";

    function run() external {
        uint256 deployerPrivateKey = vm.envUint("STORY_WALLET_PRIVATE_KEY");
        address deployer = vm.addr(deployerPrivateKey);
        vm.startBroadcast(deployerPrivateKey);

        // 1. Deploy Ava's NFT contract
        console.log("Deploying Ava's NFT contract...");
        AvaCharacter avaCharacter = new AvaCharacter();
        console.log("Ava's NFT contract deployed at:", address(avaCharacter));

        // 2. Mint Ava's NFT
        console.log("\nMinting Ava's NFT...");
        avaCharacter.mint(deployer, AVA_METADATA);
        console.log("Minted Ava's NFT to:", deployer);

        // 3. Register Ava's IP
        console.log("\nRegistering Ava's IP...");
        IIPAssetRegistry registry = IIPAssetRegistry(IP_ASSET_REGISTRY);
        address avaIpId = registry.register(block.chainid, address(avaCharacter), 0);
        console.log("Registered Ava's IP with ID:", avaIpId);

        vm.stopBroadcast();
    }
}
