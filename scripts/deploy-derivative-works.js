const hre = require("hardhat");

async function main() {
  const DerivativeWorks = await hre.ethers.getContractFactory("DerivativeWorks");
  const derivativeWorks = await DerivativeWorks.deploy();
  await derivativeWorks.deployed();

  console.log("DerivativeWorks deployed to:", derivativeWorks.address);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
