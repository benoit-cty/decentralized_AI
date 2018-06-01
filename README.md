# decentralized_AI

This is a first try at building a Decentralized AI.

## Building the Docker Image

```
docker build docker_keras_cpu/ -t trancept/keras_mnist:v0
docker run -v /tmp:/iexec trancept/keras_mnist:v0
docker push trancept/keras_mnist:v0
```

=> It will train an AI to do OCR on the well known MNIST dataset.
Dockerfile is based on work from https://github.com/gw0/docker-keras , thanks to him.

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

Deploy your app after code change :
```
iexec app deploy
```

### Execute Dapp

You have to initiate an order to buy computing ressource, then find one avaliable, then buy it !

```
iexec order init --buy
# Show available computing ressource
iexec orderbook show --category 5
# Check a ressource
iexec order show 170
# Buy the ressource
iexec order fill 170
# Check the status
iexec work show 0x7ec5f9af4f5b4e137b6e6fc311c8a21df3276e7e
# Download the result
iexec work show 0x7ec5f9af4f5b4e137b6e6fc311c8a21df3276e7e --download
```




