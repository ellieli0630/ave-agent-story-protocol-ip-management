require('dotenv').config();
const { StoryClient } = require('@story-protocol/core-sdk');
const { http } = require('viem');
const { privateKeyToAccount } = require('viem/accounts');

async function main() {
    const RPC_URL = 'https://aeneid.storyrpc.io/';

    // Get private key from env
    const privateKey = process.env.STORY_WALLET_PRIVATE_KEY;
    if (!privateKey) {
        throw new Error('STORY_WALLET_PRIVATE_KEY not found in environment variables');
    }

    // Create viem account and wallet client
    const account = privateKeyToAccount(privateKey);
    console.log('Using wallet address:', account.address);

    const client = await StoryClient.newClient({
        transport: http(RPC_URL),
        account: account,
    });

    // Log available client properties
    console.log('Client properties:', Object.keys(client));
    
    // Log all methods on the client
    console.log('Client methods:', Object.getOwnPropertyNames(Object.getPrototypeOf(client)));

    // Use the known values
    const ipId = '0xb8De82bFE670070559f3E587F7d4aDa2802bbf77';
    const LICENSE_TERMS_ID = 571n;

    try {
        console.log('Attempting to attach license terms...');
        const response = await client.license.attachLicenseTerms({
            licenseTermsId: LICENSE_TERMS_ID,
            ipId: ipId,
            txOptions: { waitForTransaction: true }
        });

        if (response.success) {
            console.log(`Attached License Terms to IPA at transaction hash ${response.txHash}.`);
        } else {
            console.log(`License Terms already attached to this IPA.`);
        }
    } catch (error) {
        console.error('Error:', error);
        if (error.cause) {
            console.error('Error cause:', error.cause);
        }
    }
}

main().catch(console.error);
