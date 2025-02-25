// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Script} from "forge-std/Script.sol";
import {DerivativeWorks} from "../src/DerivativeWorks.sol";

contract DeployDerivativeWorks is Script {
    function run() public returns (DerivativeWorks) {
        // Ava's address and token ID
        address originalIPOwner = 0x04fbd8a2e56dd85CFD5500A4A4DfA955B9f1dE6f;
        uint256 originalTokenId = 1;
        uint256 licenseFee = 0.01 ether; // 0.01 IP tokens

        // IP token address - this needs to be set to the actual IP token contract address
        address ipTokenAddress = address(0); // TODO: Replace with actual IP token address

        vm.startBroadcast();
        DerivativeWorks derivativeWorks = new DerivativeWorks(
            originalIPOwner,
            originalTokenId,
            licenseFee,
            ipTokenAddress
        );
        vm.stopBroadcast();
        
        return derivativeWorks;
    }
}
