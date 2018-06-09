import Vue from 'vue'
import App from './App.vue'
import Vuetify from 'vuetify'
import EthJs from 'ethjs'
import createIExecContracts from 'iexec-contracts-js-client'
import createIEXECClient from 'iexec-server-js-client'
import { chains, DEFAULT_CHAIN } from './chains'
import AsyncComputed from 'vue-async-computed'
import IpfsApi from 'ipfs-api'
import VueResource from 'vue-resource'

import 'vuetify/dist/vuetify.css'

Vue.use(Vuetify)
Vue.use(AsyncComputed)
Vue.use(VueResource);

const sleep = ms => new Promise(r => setTimeout(r, ms));
const debug = console.log;

const iexec = createIEXECClient({ server: 'https://testxw.iex.ec:443' });

const ipfs = IpfsApi('nrxubuntu.eastus2.cloudapp.azure.com', '7001')
// const ipfs = IpfsApi('localhost', '5001')
// const ipfs = IpfsApi({ host: 'ipfs.infura.io', port: 5001, protocol: 'https' })

let Global = new Vue({
  data: {
    $ipfs: ipfs,
    $iexec: iexec,
    $ethjs: null,
    $account: null,
    $chainId: DEFAULT_CHAIN
  },
});

Vue.mixin({
  computed: {
    $ipfs: {
      get: () => Global.$data.$ipfs
    },
    $iexec: {
      get: () => Global.$data.$iexec
    },
    $account: {
      get: () => { return Global.$data.$account },
      set: (account) => { Global.$data.$account = account }
    },
    $chainId: {
      get: () => { return Global.$data.$chainId },
      set: (chainId) => { Global.$data.$chainId = chainId }
    },
    $ethjs: {
      get: () => { return Global.$data.$ethjs },
      set: (ethjs) => { Global.$data.$ethjs = ethjs }
    },
  },
})

const setAccount = (account) => Global.$data.$account = account
const setChainID = (chainId) => Global.$data.$chainId = chainId

new Vue({
  el: '#app',
  watch: {
    $account(account) {
      // this.$iexec.auth(web3.currentProvider, account).then(({ jwtoken, cookie }) => {
      //   console.log(jwtoken); // this is given by auth.iex.ec server
      //   console.log(cookie); // this is given by iExec server
      // });
    }
  },
  async mounted () {
    this.$ipfs.swarm.peers((err, res) => {
      if (err) {
        console.error("IPFS ERROR :" + err)
      } else {
        console.log("IPFS - connected.")
      }
    })

    this.$ipfs.id((err, res) => {
      if (err) throw err
        debug('IPFS id :', res.id)
        debug('IPFS agentVersion :', res.agentVersion)
        debug('IPFS protocolVersion :', res.protocolVersion)
    })

    if (typeof window.web3 !== 'undefined') {
      this.$ethjs = new EthJs(window.web3.currentProvider);
      debug('ethjs', this.$ethjs);
      this.$ethjs
        .protocolVersion()
        .then(result => debug('ethjs.protocolVersion', result))
        .catch(debug);
      this.$ethjs
        .net_version()
        .then(result => debug('ethjs.net_version', result))
        .catch(debug);
      this.$ethjs
        .web3_clientVersion()
        .then(result => debug('ethjs.web3_clientVersion', result))
        .catch(debug);
      this.$ethjs
        .accounts()
        .then(accounts => {
          debug('ethjs.accounts', accounts);
        })
        .catch(debug);

      let currChainID = await this.$ethjs.net_version();
      debug('currChainID', currChainID);
      if (currChainID && currChainID !== DEFAULT_CHAIN) setChainID(currChainID);
      const checkChainID = async () => {
        const newChainID = await this.$ethjs.net_version();
        if (newChainID !== currChainID) {
          setChainID(newChainID);
          currChainID = newChainID;
        }
        await sleep(200);
        checkChainID();
      };
      checkChainID();

      let [currAccount] = await this.$ethjs.accounts();
      debug('currAccount', currAccount);
      if (currAccount) setAccount(currAccount);
      const checkAccount = async () => {
        const [newAccount] = await this.$ethjs.accounts();
        if (newAccount !== currAccount) {
          debug('Metamask change account', newAccount);
          setAccount(newAccount);
          currAccount = newAccount;
        }
        await sleep(200);
        checkAccount();
      };
      checkAccount();
    } else {
      debug('No web3, need to install metamask');
    }
  },
  render: h => h(App)
})
