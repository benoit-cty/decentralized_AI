# Decentralized AI (final project for Siraj's School of AI)

## Authors
Benoit C, Matthew McAteer, Alexandre Moreau and Jeddi Mees

This is a first try at building a "Decentralized AI". Well it is just a semantic segmentation task that run in a decentralized fashion : The task is done on a machine in the internet, like in a proprietary cloud, but on a decentralized cloud : you do not have to create an account with the computer owner. All is handle by iExec.

The semantic segmentation is done by the [Mask RCNN](https://github.com/matterport/Mask_RCNN) project trained on the [COCO Dataset](http://cocodataset.org/).

Submit an image :
![FrontUI](https://raw.githubusercontent.com/trancept/decentralized_AI/master/img/front_ai2.jpg)

Get the result in the work tab :
![FrontUIWork](https://raw.githubusercontent.com/trancept/decentralized_AI/master/img/front-work.jpg)

And you are done :
![SampleResult](https://raw.githubusercontent.com/trancept/decentralized_AI/master/img/iexec-team-MRCNN.png)


Other sample :
![MASK_R-CNN](https://github.com/trancept/decentralized_AI/blob/master/img/20180604_143926.png)

The Docker image was based on the Modern Deep-learning container from [Waleed Abdulla](https://hub.docker.com/r/waleedka/modern-deep-learning/), with the Mask RCNN added into it along with a modified version of the demo packaged for iExec.

[iExec is a whole ecosystem with a market-place for DApps, Oracle mechanism, scheduler, workers](https://cdn-images-1.medium.com/max/1200/1*iiERfyS1iqvVXNCXFrghfA.jpeg),... Dedicated to off-chain computing in a fully decentralized way.

The V2 is just out (speaking from 1st of June 2018).

[iExec SDK](https://github.com/iExecBlockchainComputing/iexec-sdk) is a NodeJS application who allow to easily create and manage your application.

The result is that you can call it quite like an API to get your resulting image :

For more background info read our [Whitepaper](https://github.com/trancept/decentralized_AI/blob/master/whitepaper/whitepaper.md).

# How to Run 
## iExec Front Side

You could use it on the browser : http://nrxubuntu.eastus2.cloudapp.azure.com/

Get ETH and RLC for Kovan :
. Connect to Metamask and switch to Kovan Ethereum test network. Ask for free ETH on [Kovan faucet](https://gitter.im/kovan-testnet) and for free RLC on [iExec marketplace](https://market.iex.ec/), then transfert RLC from your wallet to your "account" (on top left of [iExec marketplace](https://market.iex.ec/))

Build it from source :
```
cd frontend
npm install
npm run dev
```
Your browser will automatically go to localhost:8081 so you can access the frontend.
. Choose an image from your harddisk or copy-past an url.
. Choose a worker in the list on the right.
. Click on "iExec" button.

## OpenMined Side

In [openmined](https://github.com/trancept/decentralized_AI/tree/master/openmined) folder you will find a demo of how to use Open Mined to train a model using decentralized grid computing capabilities.

# How we make it

## Building the Docker Image

```
docker build docker_keras_cpu/ -t trancept/keras_mrcnn:v0
docker run -v $(pwd):/iexec trancept/keras_mrcnn:v0  http://fr.ubergizmo.com/wp-content/uploads/2017/11/nouvel-algorithme-correction-panoramas-google-street-view.jpg
docker push trancept/keras_mrcnn:v0
```


## iExec project

```
# Init project

# Get money
iexec wallet getRLC
=> For ETH, on Kovan you have to go to ask for it on [Kovan faucet](https://gitter.im/kovan-testnet)
# Check your wallet
iexec wallet show
=> You need to have ETH and RLC
# Send money to the iExec account/Marketplace to use it
iexec account deposit 100
# Check money
iexec account show
```

### Deploy

Adding docker image to iExec :
- Edit iexec.js
- Run :
```
iexec app deploy
iexec app show
```
Prepare order

```
iexec order init --buy
```
*Important* : You have to edit iexec.json at these step to edit the "params" string to match the parameters you want to send to the job.


### How to execute iExec Dapp

#### Easiest way

The easiest way is to go to https://market.iex.ec/ and place a Buy order with :
- An available sell order ID
- Dapp Address: 0xc790D024Ec41a7649E7a0590e4AE05891fA61ef8
- Work Params: {"cmdline":"https://storage.canalblog.com/78/32/802934/60160490.jpg"}
 
#### Command line way

. Clone the repository
. Change the image url in iexec.json
. run

You have to initiate an order to buy computing ressource, then find one available, then buy it !

```
# Show available computing ressource
iexec orderbook show --category 3
# Check a ressource
iexec order show 170
# Buy the ressource
iexec order fill 170
# Check the status
iexec work show 0xfda65e0d09bf434ea1e52f4ec044a07d6e7d592d --watch --download
```
