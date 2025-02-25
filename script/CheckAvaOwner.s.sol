// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Script.sol";
import "forge-std/console.sol";

interface IIPAssetRegistry {
    function ipId(uint256 chainId, address tokenContract, uint256 tokenId) external view returns (address);
    function ownerOf(address ipId) external view returns (address);
}

contract CheckAvaOwnerScript is Script {
    address constant IP_ASSET_REGISTRY = 0x77319B4031e6eF1250907aa00018B8B1c67a244b;
    address constant AVA_CHARACTER = 0x6b0AF5c02Fefb2d4FC920776D0fEECd00CaD0d4A;

    function run() external view {
        // Get Ava's IP ID
        IIPAssetRegistry registry = IIPAssetRegistry(IP_ASSET_REGISTRY);
        address avaIpId = registry.ipId(block.chainid, AVA_CHARACTER, 0);
        require(avaIpId != address(0), "IP not registered");
        console.log("Found Ava's IP ID:", avaIpId);

        // Get IP owner
        address owner = registry.ownerOf(avaIpId);
        console.log("IP Owner:", owner);
    }
}
