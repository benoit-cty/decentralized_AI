# Synergy between OpenMined and iExec
## Decentralized AI Whitepaper for Siraj's Decentralized Apps

## Authors
Benoit C, Matthew McAteer, Alexandre Moreau, Jeddi Mees.

## Introduction

Artificial intelligence (AI) is an umbrella term for systems that can . In more recent years this has come to include the definitions of Machine Learning and by extension Deep Learning, techniques in computer science that allow programs to make inferences and predictions based on examples of input data. AI has been a boon to organizations with large silos of data at their disposal, but it has also raised some concerns. Some of these include but are not limited to user privacy, ownership of data, negative externalities of AI models optimizing for a narrowly-defined cost function, and latency and vulnerability of such centralized services. We propose a dual, general purpose paradigm for using decentralized artificial intelligence, that combines the best of two projects in the field: iExec and OpenMined.

![MASK_R-CNN](https://github.com/trancept/decentralized_AI/blob/master/img/20180604_143926.png)

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

![iexec_blueprint](https://github.com/trancept/decentralized_AI/blob/master/img/architecture_2.png)

## Technologies

Our project is build around iExec, the Inter-Planetary FileSystem (IPFS), and OpenMined.
IPFS is a distributed data storage system. Rather than having content addressed by servers like with HTTP, IPFS creates unique addresses for content itself that is copied redundantly over multiple nodes. It's functionality has already been demonstrated multiple times in the real world, and multiple projects exist to build on top of it (such as FileCoin developing ways to incentivize people to host these nodes, and thereby create a more stable network for people to keep their files on).

The iExec project goal is to allow off-chain computation in a decentralized fashion. People can share their spare computing capacity for a given machine learning task, and they can be rewarded with RLC tokens. In the future, the project aims to sell unique datasets on this network (NOTE: iExec just recently released its testnet last week, so it is more challenging to use it. For example there is only company worker to execute task so when they are stopped we have no way to work on our project).

If iExec offers the marketplace, incentivization, and computation management system for distributed AI, the OpenMined adds the computing paradigm for user and data anonymization. OpenMined combines machine learning with homomorphic encyption (encyrption that still allows for computations to be run on the encrypted data), and federated machine learning ()

Combined, the result is a fully distributed information storage, processing, and buying/selling system.

## MARKET OPPORTUNITY  

Decentralisation is essential if we wan't to get our privacy and liberty back.
OpenSource was a first step. Blockchain like Ethereum took it to the next level by allowing to incentive peoples.
But current blockchain, or best call it distributed ledger technology (DLT), coulnd't handle heavy computing task.
We are at the beginning of a new erae with project like [Open Mined](XXX) and iExec for example.
These project aim at computing challenging task. With a great addition to privacy for Open Mined.

Privacy is no more a cypherpunk concept, it is a mainstream subject with GDPR and Facebook numerous leaks.
More and more poeple saw their data as valuable assets and meaningful.

### The Blockchain market

The report "Blockchain Market by Provider, Application (Payments, Exchanges, Smart Contracts, Documentation, Digital Identity, Supply Chain Management, and GRC Management), Organization Size, Industry Vertical, and Region - Global Forecast to 2022", The blockchain market size is expected to grow from USD 411.5 Million in 2017 to USD 7,683.7 Million by 2022, at a Compound Annual Growth Rate (CAGR) of 79.6%. The key factors including reduced total cost of ownership, faster transactions, simplified business process with transparency and immutability, and rising cryptocurrencies market cap and ICO are expected to drive the overall growth of the market.
Blockchain is more challenging, most poeple sees it only like a crypto-currency and not like an other way to do computing while there’s a tons of other use cases: identity, notary, digital assets, smart contracts, digital voting, distributed storage, AI computing, etc.

### The dapps market
DAPPs means Decentralized Applications. That’s a new kind of applications. These types of applications are not owned by anyone, can’t be shut down, and cannot have downtime. A DAPP should meet these criteria: Open Source, Decentralized, Incentive (digital assets for feeling itself). There’s DAPPS built on top of the two biggest blockchain platforms Bitcoin and Ethereal. There’s also some DAPPs built on their own blockchain.
New DAPPs are built every day, as you can see on https://www.stateofthedapps.com, listing 1576 DAPPs on his explorer, or even on https://dappradar.com

Everything can be decentralized. We believe that in the future, all kind of applications will be decentralized, even the bigger ones.
One of the current issue is that dapps are not necessarily user friendly and it’s pretty hard to be mass market. Another issue, is scalability. Ethereum’s scalability issues were recently emphasized by the popular cat-collecting virtual game CryptoKitties (DAPP game). The viral game caused the network, that can only handle 10 transactions per second to become clogged, and transaction fees skyrocketed.

### The traditional cloud market

It's a huge market. Many company transfert their infrastructures to the cloud. XXX Market value ?

### The edge and fog computing market

A new approach began to emmerrge with "Fog Computing". XXX Explain ?

## TECHNOLOGY OVERVIEW
### Background

Computing on blockchain is really limited to few instructions. And it will probably remain like that.
But there is the need for heavy computation like AI, video encoding, 3D rendering to be done decentralized.
This is what we will demonstrate with our project.

### Our stack

We have two main part : the front, who is the user interface and the back, which do the computation.

![project_blueprint](https://github.com/trancept/decentralized_AI/blob/master/img/architecture_1.png)

### The Back-end

We build a Docker image with Keras, Tensorflow, Python 3 and matplotlib in headless mode to render the result to a file. We add the RCNN (regional convolutional neural network) weight file trained on [COCO dataset](http://cocodataset.org/). We made a Python script based on the demo Jupyter Notebook from Matterport for [Mask RCNN](https://github.com/matterport/Mask_RCNN). We add the Docker image to [DockerHub](https://hub.docker.com/). We made an iExec DApp (decentralized application) using the just released [iExec SDK V2](https://github.com/iExecBlockchainComputing/iexec-sdk). We deploy it to the [iExec marketplace](https://market.iex.ec/). So we now have a DApp ready to be called by any Ethereum smart contract. The contract call the DApp with the image URL to process. When the processing is finish a callback function is called so the contrat could continue his process. The computation of the image is done off-chain and act as an [Oracle](https://medium.com/bethereum/how-oracles-connect-smart-contracts-to-the-real-world-a56d3ed6a507).

### The Front-end

![front_screenshot](https://github.com/trancept/decentralized_AI/blob/master/img/front_preview.png)

We use NodeJS, Vue.JS, [Vuetify](https://vuetifyjs.com/en/), ETHjs, the [iExec front SDK](https://github.com/iExecBlockchainComputing/iexec-server-js-client), and IPFS-api. We use IPFS to allow user to upload an image to IPFS. But it is not mandatory, a user could also copy-paste an url from Internet. Then the user pays the processing in RLC currency and the Gas in ETH with Metamask.

### Note on Proof-of-contribution
Proof of Contibution (PoCo) is the way iExec ensure that a worker do not cheat when we pay him for a work. A worker must make a deposit and if they cheat, they loose the deposit. This is a core functionnality for iExec. It means that task for the distributed computation must be probabilistic to be able to check against cheating.

## THE MARKETPLACE FOR CLOUD RESOURCES

iExec offerx a cloud computing marketplace to allow cloud computing as a commodity. It means that one can easily by computing ressources. A computing ressource is called a "worker". Workers are grouped together in a "workerpool". This worker pool could be a former cloud provider who want to get money for his unsued computing power. Or individuals who want to get a little bit of money from their home computer. The iExec marketplace is the place where workers sell their power to buyers. Like an open marketplace or an exchange. It's a pay-per-task (ppt) system. A bit like cloud API provider. The DApp store is where you can find packaged application to run on iExec network. For  or project that's where we put our semantic segmentation DApp. The data marketplace is where you could sell or buy data (available in a future release).

## ROADMAP
### Overview

_Phase 1_: Creation of MVP (June, 2018)
_Phase 2_: Debugging on Testnets (Q2 2018 - Q4 2018)
_Phase 3_: Release and further real-world testing (starting Q4 2018 - Q1 2019)

### Financial Considerations & Budget

This project is currently without cost and has no assigned budget. Development is fueled by volunteers who contribute part-time, and the kind donors of computing power on the testnet. As such, we also do not plan to launch an ICO. Aside from the risks of an ICO (such as needing to spend disproportionate amounts of capital on marketing instead of engineering), we have enough faith in humanity for it to contribute towards helping us achieve our collective development goals.

(Note: We have imposed a very minor transaction fee on transactions made using our Dapp to finance teambuilding excursions once a week.)

## TEAM

We build a great team to be able to achieve our goal.

### Benoît Courty
![Benoît](../img/ben-rd168.png)

French technical project manager who works as a free-lancer in big company in energy, insurance , e-commerce and TV since 1999. He also co-founded an UAV start-up, Neo-Robotix, that unfortunately didn't find his market fit.

He's deeply looking at blockchain technology since one year, beginning with trading, then mining and now with development of smart contract and decentralized computing with project like iExec. As you can see in his GitHub :https://github.com/trancept/ He's looking for new opportunities in blockchain and machine learning.

### Matthew McAteer
![Matthew](../img/Mattew-rd168.png)

Matthew is a Developer at [Inkrypt](https://www.inkrypt.io/), a company working on using IPFS to create censorship-resistant journalism tools, and Data Scientist at HelloFriend, which works on consumer DApps for event organizing and social media. Matthew has also worked with Companies such as Google and Suspect Technologies, and is a Graduate of Brown University. 

### Alexandre Moreau
![Alexandre](../img/Alex-rd.png)

Alexandre graduated in 2016 as a Computer Science engineer specialized in Robotics from the Institut polytechnique de Bordeaux in France. He currently works as an Integration Engineer at Deepomatic, a start-up specialized in Deep-Learning and video recognition systems. Before that, he worked as a R&D Software Engineer at another startup specialized in 3D printing and completed three research internships in Bioinformatics, Computer Graphics and High Performance Computing.

### Jeddi Mees
![Jeddi](../img/Jeddi-rd168.png)

Growth hacker from the Growth Tribe Academy in Amsterdam and technical dev from LeWagon. He worked for EdTech and FoodTech industry as a growth marketer. Since 2016, he's helping startups and corporates to find new ways to grow.
He's passionate about blockchain technology and AI. He's looking for new opportunities into this space as a growth marketer/product marketer. User Acquisition, Conversion Optimization and Retention, that's his specialization https://www.linkedin.com/in/jeddi-mees-i-do-growth/

WARNING : *this a student project and has to be taken as his, without any warranty of any kind. Use at you own risk.* This is our final project for [TheSchool.AI](https://www.theschool.ai), a decentralized application course by Siraj Raval. This Whitepaper is inspired by the one from iExec and the OpenMined project. We talk a lot of iExec & OpenMined because it is the core technology we use for our project, but we have no link or affiliation of any kind with iExec.

## REFERENCES

Below is a list of the papers and projects that have inspired this work:

- [Vuetify](https://vuetifyjs.com/en/)
- [Mask RCNN](https://arxiv.org/abs/1703.06870)
- [iExec (whitepaper)](https://iex.ec/whitepaper/iExec-WPv3.0-English.pdf)
- [OpenMined (site)](https://www.openmined.org/)
