// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract DerivativeWorks is ERC721, Ownable {
    uint256 private _tokenIds;
    uint256 private _licenseIds;

    enum LicenseType { NonCommercial, Commercial }
    enum Status { Pending, Approved, Rejected }

    struct License {
        address holder;
        uint256 originalTokenId;
        LicenseType licenseType;
        uint256 issuedAt;
        bool isValid;
    }

    struct DerivativeWork {
        string title;
        address creator;
        uint256 createdAt;
        string imageUrl;
        string description;
        LicenseType licenseType;
        Status status;
        string ipfsMetadata;
        address originalIPOwner;
        uint256 originalTokenId;
        uint256 licenseId;
    }

    // IP token contract
    IERC20 public ipToken;

    // License fee in IP tokens
    uint256 public licenseFee;
    
    // Original IP owner's address
    address public originalIPOwner;
    
    // Original token ID
    uint256 public originalTokenId;

    // Mapping from license ID to License
    mapping(uint256 => License) public licenses;
    
    // Mapping from token ID to DerivativeWork
    mapping(uint256 => DerivativeWork) public derivatives;
    
    // Mapping from holder to their licenses
    mapping(address => uint256[]) public holderLicenses;
    
    // Mapping from license to its derivatives
    mapping(uint256 => uint256[]) public licenseDerivatives;

    event LicenseMinted(
        uint256 indexed licenseId,
        address indexed holder,
        LicenseType licenseType
    );

    event DerivativeWorkCreated(
        uint256 indexed tokenId,
        string title,
        address indexed creator,
        LicenseType licenseType,
        Status status,
        uint256 indexed licenseId
    );

    event DerivativeWorkStatusUpdated(
        uint256 indexed tokenId,
        Status status
    );

    event LicenseFeeUpdated(
        uint256 oldFee,
        uint256 newFee
    );

    constructor(
        address initialOwner,
        uint256 _originalTokenId,
        uint256 _licenseFee,
        address _ipTokenAddress
    ) ERC721("DerivativeWorks", "DRW") Ownable(initialOwner) {
        originalIPOwner = initialOwner;
        originalTokenId = _originalTokenId;
        licenseFee = _licenseFee;
        ipToken = IERC20(_ipTokenAddress);
    }

    function setLicenseFee(uint256 _newFee) external onlyOwner {
        uint256 oldFee = licenseFee;
        licenseFee = _newFee;
        emit LicenseFeeUpdated(oldFee, _newFee);
    }

    function mintLicense(LicenseType licenseType) public returns (uint256) {
        // Transfer IP tokens from msg.sender to originalIPOwner
        require(ipToken.transferFrom(msg.sender, originalIPOwner, licenseFee), "IP token transfer failed");
        
        unchecked {
            _licenseIds++;
        }
        uint256 newLicenseId = _licenseIds;

        License memory newLicense = License({
            holder: msg.sender,
            originalTokenId: originalTokenId,
            licenseType: licenseType,
            issuedAt: block.timestamp,
            isValid: true
        });

        licenses[newLicenseId] = newLicense;
        holderLicenses[msg.sender].push(newLicenseId);

        emit LicenseMinted(newLicenseId, msg.sender, licenseType);
        return newLicenseId;
    }

    function createDerivativeWork(
        string memory title,
        string memory imageUrl,
        string memory description,
        string memory ipfsMetadata,
        uint256 licenseId
    ) public returns (uint256) {
        License memory license = licenses[licenseId];
        require(license.holder == msg.sender, "Must own the license");
        require(license.isValid, "License is not valid");

        unchecked {
            _tokenIds++;
        }
        uint256 newTokenId = _tokenIds;

        DerivativeWork memory newWork = DerivativeWork({
            title: title,
            creator: msg.sender,
            createdAt: block.timestamp,
            imageUrl: imageUrl,
            description: description,
            licenseType: license.licenseType,
            status: Status.Pending,
            ipfsMetadata: ipfsMetadata,
            originalIPOwner: originalIPOwner,
            originalTokenId: originalTokenId,
            licenseId: licenseId
        });

        derivatives[newTokenId] = newWork;
        licenseDerivatives[licenseId].push(newTokenId);
        _safeMint(msg.sender, newTokenId);

        emit DerivativeWorkCreated(
            newTokenId,
            title,
            msg.sender,
            license.licenseType,
            Status.Pending,
            licenseId
        );

        return newTokenId;
    }

    function updateDerivativeStatus(uint256 tokenId, Status newStatus) public {
        DerivativeWork storage work = derivatives[tokenId];
        require(
            msg.sender == originalIPOwner || msg.sender == owner(),
            "Only original IP owner or contract owner can update status"
        );
        require(
            work.status == Status.Pending,
            "Can only update pending derivatives"
        );

        work.status = newStatus;
        emit DerivativeWorkStatusUpdated(tokenId, newStatus);
    }

    function getDerivativeWork(uint256 tokenId) public view returns (
        string memory title,
        address creator,
        uint256 createdAt,
        string memory imageUrl,
        string memory description,
        LicenseType licenseType,
        Status status,
        string memory ipfsMetadata,
        address workOriginalIPOwner,
        uint256 workOriginalTokenId,
        uint256 licenseId
    ) {
        DerivativeWork memory work = derivatives[tokenId];
        return (
            work.title,
            work.creator,
            work.createdAt,
            work.imageUrl,
            work.description,
            work.licenseType,
            work.status,
            work.ipfsMetadata,
            work.originalIPOwner,
            work.originalTokenId,
            work.licenseId
        );
    }

    function getLicense(uint256 licenseId) public view returns (
        address holder,
        uint256 originalTokenId,
        LicenseType licenseType,
        uint256 issuedAt,
        bool isValid
    ) {
        License memory license = licenses[licenseId];
        return (
            license.holder,
            license.originalTokenId,
            license.licenseType,
            license.issuedAt,
            license.isValid
        );
    }

    function getHolderLicenses(address holder) public view returns (uint256[] memory) {
        return holderLicenses[holder];
    }

    function getLicenseDerivatives(uint256 licenseId) public view returns (uint256[] memory) {
        return licenseDerivatives[licenseId];
    }

    function getDerivativeCount() public view returns (uint256) {
        return _tokenIds;
    }

    function getLicenseCount() public view returns (uint256) {
        return _licenseIds;
    }

    receive() external payable {}
}
