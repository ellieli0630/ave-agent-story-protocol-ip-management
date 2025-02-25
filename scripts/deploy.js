const hre = require("hardhat");

async function main() {
  console.log("Deploying AvaCharacter contract...");

  const AvaCharacter = await hre.ethers.getContractFactory("AvaCharacter");
  const avaCharacter = await AvaCharacter.deploy();

  await avaCharacter.waitForDeployment();

  console.log(`AvaCharacter deployed to ${await avaCharacter.getAddress()}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
