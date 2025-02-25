// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Test} from "forge-std/Test.sol";
import {DerivativeWorks} from "../src/DerivativeWorks.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

// Mock IP Token for testing
contract MockIPToken is ERC20 {
    constructor() ERC20("IP Token", "IP") {
        _mint(msg.sender, 1000 ether);
    }
}

contract DerivativeWorksTest is Test {
    DerivativeWorks public derivativeWorks;
    MockIPToken public ipToken;
    address public originalIPOwner;
    address public creator;
    uint256 public constant LICENSE_FEE = 0.01 ether;
    uint256 public constant ORIGINAL_TOKEN_ID = 1;

    function setUp() public {
        originalIPOwner = makeAddr("originalIPOwner");
        creator = makeAddr("creator");
        
        // Deploy mock IP token
        ipToken = new MockIPToken();
        
        // Transfer some IP tokens to creator
        ipToken.transfer(creator, 1 ether);
        
        // Deploy derivative works contract
        derivativeWorks = new DerivativeWorks(
            originalIPOwner,
            ORIGINAL_TOKEN_ID,
            LICENSE_FEE,
            address(ipToken)
        );
    }

    function test_LicenseMinting() public {
        vm.startPrank(creator);
        
        // Approve contract to spend IP tokens
        ipToken.approve(address(derivativeWorks), LICENSE_FEE);
        
        // Mint a non-commercial license
        uint256 licenseId = derivativeWorks.mintLicense(
            DerivativeWorks.LicenseType.NonCommercial
        );

        assertEq(licenseId, 1);
        
        // Check license details
        (
            address holder,
            uint256 originalTokenId,
            DerivativeWorks.LicenseType licenseType,
            uint256 issuedAt,
            bool isValid
        ) = derivativeWorks.getLicense(licenseId);

        assertEq(holder, creator);
        assertEq(originalTokenId, ORIGINAL_TOKEN_ID);
        assertEq(uint256(licenseType), uint256(DerivativeWorks.LicenseType.NonCommercial));
        assertGt(issuedAt, 0);
        assertTrue(isValid);
        
        // Check IP token transfer
        assertEq(ipToken.balanceOf(originalIPOwner), LICENSE_FEE);
        assertEq(ipToken.balanceOf(creator), 1 ether - LICENSE_FEE);

        vm.stopPrank();
    }

    function test_CreateDerivativeWithLicense() public {
        vm.startPrank(creator);
        
        // Approve and mint license
        ipToken.approve(address(derivativeWorks), LICENSE_FEE);
        uint256 licenseId = derivativeWorks.mintLicense(
            DerivativeWorks.LicenseType.NonCommercial
        );

        // Create derivative work using that license
        uint256 tokenId = derivativeWorks.createDerivativeWork(
            "Test Work",
            "ipfs://test",
            "Test Description",
            "ipfs://metadata",
            licenseId
        );

        assertEq(tokenId, 1);
        assertEq(derivativeWorks.ownerOf(tokenId), creator);

        (
            string memory title,
            address workCreator,
            uint256 createdAt,
            string memory imageUrl,
            string memory description,
            DerivativeWorks.LicenseType licenseType,
            DerivativeWorks.Status status,
            string memory ipfsMetadata,
            address workOriginalIPOwner,
            uint256 workOriginalTokenId,
            uint256 workLicenseId
        ) = derivativeWorks.getDerivativeWork(tokenId);

        assertEq(title, "Test Work");
        assertEq(workCreator, creator);
        assertGt(createdAt, 0);
        assertEq(imageUrl, "ipfs://test");
        assertEq(description, "Test Description");
        assertEq(uint256(licenseType), uint256(DerivativeWorks.LicenseType.NonCommercial));
        assertEq(uint256(status), uint256(DerivativeWorks.Status.Pending));
        assertEq(ipfsMetadata, "ipfs://metadata");
        assertEq(workOriginalIPOwner, originalIPOwner);
        assertEq(workOriginalTokenId, ORIGINAL_TOKEN_ID);
        assertEq(workLicenseId, licenseId);

        vm.stopPrank();
    }

    function test_RevertWhen_CreateDerivativeWithoutLicense() public {
        vm.startPrank(creator);
        
        vm.expectRevert(); // Expect the transaction to revert
        derivativeWorks.createDerivativeWork(
            "Test Work",
            "ipfs://test",
            "Test Description",
            "ipfs://metadata",
            1 // Non-existent license ID
        );

        vm.stopPrank();
    }

    function test_RevertWhen_CreateDerivativeWithInvalidLicense() public {
        address otherUser = makeAddr("otherUser");
        ipToken.transfer(otherUser, 1 ether);
        
        // First user mints a license
        vm.startPrank(otherUser);
        ipToken.approve(address(derivativeWorks), LICENSE_FEE);
        uint256 licenseId = derivativeWorks.mintLicense(
            DerivativeWorks.LicenseType.NonCommercial
        );
        vm.stopPrank();

        // Different user tries to use that license
        vm.startPrank(creator);
        vm.expectRevert(); // Expect the transaction to revert
        derivativeWorks.createDerivativeWork(
            "Test Work",
            "ipfs://test",
            "Test Description",
            "ipfs://metadata",
            licenseId
        );
        vm.stopPrank();
    }

    function test_UpdateDerivativeStatus() public {
        vm.startPrank(creator);
        
        // Approve and mint license
        ipToken.approve(address(derivativeWorks), LICENSE_FEE);
        uint256 licenseId = derivativeWorks.mintLicense(
            DerivativeWorks.LicenseType.NonCommercial
        );
        
        uint256 tokenId = derivativeWorks.createDerivativeWork(
            "Test Work",
            "ipfs://test",
            "Test Description",
            "ipfs://metadata",
            licenseId
        );
        vm.stopPrank();

        // Original IP owner approves the derivative
        vm.prank(originalIPOwner);
        derivativeWorks.updateDerivativeStatus(tokenId, DerivativeWorks.Status.Approved);
        
        (,,,,,, DerivativeWorks.Status status,,,,) = derivativeWorks.getDerivativeWork(tokenId);
        assertEq(uint256(status), uint256(DerivativeWorks.Status.Approved));
    }

    function test_RevertWhen_UpdateStatusByNonOwner() public {
        vm.startPrank(creator);
        
        // Approve and mint license
        ipToken.approve(address(derivativeWorks), LICENSE_FEE);
        uint256 licenseId = derivativeWorks.mintLicense(
            DerivativeWorks.LicenseType.NonCommercial
        );
        
        uint256 tokenId = derivativeWorks.createDerivativeWork(
            "Test Work",
            "ipfs://test",
            "Test Description",
            "ipfs://metadata",
            licenseId
        );
        
        // Try to approve own derivative
        vm.expectRevert(); // Expect the transaction to revert
        derivativeWorks.updateDerivativeStatus(tokenId, DerivativeWorks.Status.Approved);
        vm.stopPrank();
    }

    receive() external payable {}
}
