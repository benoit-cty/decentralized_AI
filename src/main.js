import Vue from 'vue'
import App from './App.vue'
import Vuetify from 'vuetify'
import EthJs from 'ethjs'
import createIExecContracts from 'iexec-contracts-js-client'
import { chains, DEFAULT_CHAIN } from './chains'

import 'vuetify/dist/vuetify.css'

Vue.use(Vuetify)

const sleep = ms => new Promise(r => setTimeout(r, ms));
const debug = console.log;

let Global = new Vue({
  data: {
    $ethjs: null,
    $account: null,
    $chainId: DEFAULT_CHAIN
  }
});

Vue.mixin({
  computed: {
    $account: {
      get: function () { return Global.$data.$account },
      set: function (account) { Global.$data.$account = account }
    },
    $chainId: {
      get: function () { return Global.$data.$chainId },
      set: function (chainId) { Global.$data.$chainId = chainId }
    },
    $ethjs: {
      get: function () { return Global.$data.$ethjs },
      set: function (ethjs) { Global.$data.$ethjs = ethjs }
    },
  }
})

const setAccount = (account) => Global.$data.$account = account
const setChainID = (chainId) => Global.$data.$chainId = chainId

new Vue({
  el: '#app',
  async mounted () {
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
  // mounted () {
  //   this.$iexec.auth(web3.currentProvider, web3.eth.accounts[0]).then(({ jwtoken, cookie }) => {
  //     console.log(jwtoken); // this is given by auth.iex.ec server
  //     console.log(cookie); // this is given by iExec server
  //     // hit iExec server API
      
  //     this.$iexec.getAppByName("0xec3cf9ff711268ef329658dd2d233483bd0127e6").then(console.log); // print app description from deploy txHash
  //     this.$iexec.getWorkByExternalID("0x84b4a80628352c78ca71eeedd4e8cbf5fc07103036d39bb6f1b9956ba30ca0b3").then(console.log); // print work description from submit txHash
  //   });
  // },
  render: h => h(App)
})
