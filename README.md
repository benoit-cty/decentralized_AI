# decentralized_ai

> A Vue.js project

## Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build
```

For detailed explanation on how things work, consult the [docs for vue-loader](http://vuejs.github.io/vue-loader).


## IPFS

First install [IPFS](https://ipfs.io/docs/install/)

``` 
    ipfs config Addresses.Gateway /ip4/0.0.0.0/tcp/9001
    ipfs config Addresses.API /ip4/0.0.0.0/tcp/5001
    ipfs config --json API.HTTPHeaders.Access-Control-Allow-Methods '["PUT", "GET", "POST", "OPTIONS"]'
    ipfs config --json API.HTTPHeaders.Access-Control-Allow-Origin '["*"]'
    ipfs daemon
```