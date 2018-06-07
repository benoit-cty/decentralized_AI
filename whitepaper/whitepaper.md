# Decentralized AI Whitepaper

## Intro

WARNING : this a student project and has to be taken as his, without any warranty of any kind. Use at you own risk.

This is our final project for [TheSchool.AI](https://www.theschool.ai), a decentralized application course by Siraj Raval.
This Whitepaper is ispired by the one from iExec
We talk a lot of iExec because it is the core technology we use for our project.
But we have no link or affiliation of any kind with iExec.

## BLUEPRINT FOR DECENTRALIZED ARTIFICIAL INTELLIGENCE

Big tech companies are leading AI these days. They use AI in more and more functionality in every application. For example Photoshop now use deep learning to separate subject from background.
Things like that is really difficult for open source software because even with engineer willing to add such functionality they don't have the Data. Data is the currency of this century. And we give them for free to these company to allow them to sell us product in return !
That is a non-sense. We all deserve to keep our data safe and be able to monetize or give them to who we want.
The leading technology for AI is Deep Learning, the concept is simple : just send millions of data with associated label (example : a picture of a cat with label "cat") to a computer program that will learn by itself to identify a cat when he saw one.
So there is three challenges :
- Having millions of data with label
- Having the computing power to train these algorithms
- Democratize the use of AI

Our contribution with this project is to address these points, beginning by the last.
Allowing anyone to compute Deep Learning algorithms with less knowledge as possible.

## BACKGROUND

Our project is build around iExec and IPFS.
IPFS means Iner-Planetary FileSystem. It's a way to share files in a peer-to-peer way.
It work perfectly well but lack of a way to incentives poeple to keep files online. FileCoin aim at doing this soon.
iExec goal is to allow off-chain computation in a decentralized way. Anybody could share his computer power and get RLC token in return. In the future, datasets could also be sold on the network.
iExec just release is testnet last week so it is more challenging to use it. For example there is only company worker to execute task so when they are stopped we have no way to work on our project.

## CURRENT LIMITATIONS

Wanting a decentralized

### Blockchain computing challenges
### traditional computing infrastructure challenges
## OUR SOLUTION
### technical overview
### core value proposition
### key technological advancements
## MARKET OPPORTUNITY  
### the perfect timing for go-to-market

Privacy is no more a cypherpunk concept, it is a mainstream subject with GDPR and Facebook numerous leaks.
More and more poeple saw there data as valuable and meaningful.

### the Blockchain market

The report "Blockchain Market by Provider, Application (Payments, Exchanges, Smart Contracts, Documentation, Digital Identity, Supply Chain Management, and GRC Management), Organization Size, Industry Vertical, and Region - Global Forecast to 2022", The blockchain market size is expected to grow from USD 411.5 Million in 2017 to USD 7,683.7 Million by 2022, at a Compound Annual Growth Rate (CAGR) of 79.6%. The key factors including reduced total cost of ownership, faster transactions, simplified business process with transparency and immutability, and rising cryptocurrencies market cap and ICO are expected to drive the overall growth of the market.
Blockchain is more challenging, most poeple sees it only like a crypto-currency and not like an other way to do computing while there’s a tons of other use cases: identity, notary, digital assets, smart contracts, digital voting, distributed storage, AI computing, etc.

### the dapps market
DAPPs means Decentralized Applications. That’s a new kind of applications. These types of applications are not owned by anyone, can’t be shut down, and cannot have downtime. A DAPP should meet these criteria: Open Source, Decentralized, Incentive (digital assets for feeling itself). There’s DAPPS built on top of the two biggest blockchain platforms Bitcoin and Ethereal. There’s also some DAPPs built on their own blockchain.
New DAPPs are built every day, as you can see on https://www.stateofthedapps.com, listing 1576 DAPPs on his explorer, or even on https://dappradar.com

Everything can be decentralized. We believe that in the future, all kind of applications will be decentralized, even the bigger ones.
One of the current issue is that dapps are not necessarily user friendly and it’s pretty hard to be mass market. Another issue, is scalability. Ethereum’s scalability issues were recently emphasized by the popular cat-collecting virtual game CryptoKitties (DAPP game). The viral game caused the network, that can only handle 10 transactions per second to become clogged, and transaction fees skyrocketed.

### the traditional cloud market
### the edge and fog computing market
### competitive landscape
## BUSINESS USE CASE
## TECHNOLOGY OVERVIEW
### Background
Computing on blockchain is really limited to few instructions. And it will probably remain like that.
But there is the need for heavy computation like AI, video encoding, 3D rendering to be done decentralized.
This is what we will demonstrate with our project.

### Our stack

We have two main part : the front, who is the user interface and the back, which do the computation.

XXX Insert schema here XXX

#### The Back
We build a Docker image with Keras, Tensorflow, Python 3 and matplotlib in headless mode to render the result to a file.
We add the RCNN (regional convolutional neural network) weight file trained on [COCO dataset](http://cocodataset.org/).
We made a Python script based on the demo Jupyter Notebook from Matterport for [Mask RCNN](https://github.com/matterport/Mask_RCNN).
We add the Docker image to [DockerHub](https://hub.docker.com/).
We made an iExec DApp (decentralized application) using the just released [iExec SDK V2](https://github.com/iExecBlockchainComputing/iexec-sdk).
We deploy it to the [iExec marketplace](https://market.iex.ec/).
So we now have a DApp ready to be called by any Ethereum smart contract.
The contract call the DApp with the image URL to process. When the processing is finish a callback function is called so the contrat could continue his process.
The computation of the image is done off-chain and act as an [Oracle](https://medium.com/bethereum/how-oracles-connect-smart-contracts-to-the-real-world-a56d3ed6a507).


### The front

XXX Insert screen capture XXX

We use NodeJS, Vue.JS, [Vuetify](https://vuetifyjs.com/en/), ETHjs, the [iExec front SDK](https://github.com/iExecBlockchainComputing/iexec-server-js-client), and IPFS-api.
We use IPFS to allow user to upload an image to IPFS. But it is not mandatory, a user could also copy-paste an url from Internet.
Then the user pays the processing in RLC currency and the Gas in ETH with Metamask.


### proof-of-contribution
Proof of Contibution (PoCo) is the way iExec ensure that a worker do not cheat when we pay him for a work.
Worker make a deposit and if they cheat, they loose it.
It's a core functionnality for iExec.
It means that task must be probabilistic to be able to check agains cheat.


### iExec smart contracts: multi-criteria scheduling
## THE MARKETPLACE FOR CLOUD RESOURCES
### the cloud computing marketplace
### cloud computing as a commodity
### workers pools
### the iexec marketplace
### pay-per-task (ppt)
### the dapp store
### the data marketplace
## ROADMAP
Our goal will be achieve when global warming was ended.
## FINANCIALS
### costs
We have no cost, we do it on our part time and kind peoples give us computing power on testnet.
### token sale
We do not plan to made an ICO because we believe in Humanity to contribute to help us in our goal.
We took a small fee on every transaction made using our Dapp to allow the team to go to Las Vegas and get drunk once a week.
## MEET THE TEAM
Name and pictures of team members with little bio.
## REFERENCES
Link to project we use
