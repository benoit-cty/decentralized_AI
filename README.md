# decentralized_AI

This is a first try at building a "Decentralized AI". Well it is just a semantic segmentation task that run in a decentralized fashion : The task is done on a machine in the internet, like in a proprietary cloud, but on a decentralized cloud : you do not have to create an account with the computer owner. All is handle by iExec.

The semantic segmentation is done by the Mask_RCNN (https://github.com/matterport/Mask_RCNN) project trained on the COCO Dataset (http://cocodataset.org/).

My work was only to make a Docker image, based on the Modern Deep-learning container https://hub.docker.com/r/waleedka/modern-deep-learning/ from Waleed Abdulla, add Mask_RCNN in it.
Add a modified version of the demo and package it for iExec.

iExec is a whole ecosystem with a market-place for DApps, Oracle mechanism, Scheduler, workers,... Dedicated to off-chain computing in a fully decentralized way.
(https://cdn-images-1.medium.com/max/1200/1*iiERfyS1iqvVXNCXFrghfA.jpeg)

The V2 is just out (speaking from 1st of June 2018).

[iExec SDK](https://github.com/iExecBlockchainComputing/iexec-sdk) is a NodeJS application who allow to easily create and manage your application.

The result is that you can call it quite like an API to get your resulting image :



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
=> For ETH, on Kovan you have to go to ask for it on https://gitter.im/kovan-testnet
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


### How to execute Dapp

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
