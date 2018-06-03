<template>
  <v-app>
    <v-toolbar fixed app>
      <v-toolbar-title>
        Welcome {{ $account }}
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-title>
        {{ currChain }}
      </v-toolbar-title>
    </v-toolbar>
    <v-content>
      <v-container fluid>
        <picture-input 
          ref="pictureInput"
          width="600" 
          height="600" 
          margin="16" 
          accept="image/jpeg,image/png" 
          size="10" 
          button-class="btn"
          :custom-strings="{
            upload: '<h1>IExec!</h1>',
            drag: 'Select an image'
          }"
          @change="onChange">
        </picture-input>
        <v-btn raised @click="iexec('175')">
          IExec !
        </v-btn>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
  import PictureInput from 'vue-picture-input'
  import createIExecContracts from 'iexec-contracts-js-client';
  import { chains, chainsMap } from './chains'

  export default {
    data () {
      return {
        image: null
      }
    },
    computed: {
      contracts () {
        if (this.$ethjs && this.$account && this.$chainId) {
          console.log(chains[this.$chainId].hub)
          return createIExecContracts({
            eth: this.$ethjs,
            chainID: this.$chainId,
            txOptions: {
              from: this.$account,
              gas: 5000000
            },
            hubAddress: chains[this.$chainId].hub,
          })
        }
      },
      currChain () {
        return chainsMap[this.$chainId];
      }
    },
    watch: {
      contracts (val) {
        console.log(val)
      }
    },
    methods: {
      onChange (image) {
        console.log('New picture selected!')
        if (image) {
          console.log('Picture loaded.')
          this.image = image
        } else {
          console.log('FileReader API not supported: use the <form>, Luke!')
        }
      },
      async iexec (orderID) {
        if (!this.contracts) return
        const marketplaceAddress = await this.contracts.fetchMarketplaceAddress();
        const orderRPC = await this.contracts
          .getMarketplaceContract({ at: marketplaceAddress })
          .getMarketOrder(orderID);

        const args = [
          orderID,
          orderRPC.workerpool,
          '0xec3CF9FF711268ef329658DD2D233483Bd0127e6', // dappAddress,
          '0x0000000000000000000000000000000000000000', // dataset
          '{"cmdline":"https://storage.canalblog.com/78/32/802934/60160490.jpg"}',
          '0x0000000000000000000000000000000000000000', // callback
          '0x0000000000000000000000000000000000000000', // beneficiary
        ]
        const transactionHash = this.contracts
          .getHubContract()
          .buyForWorkOrder(...args)
        console.log(transactionHash)
      }
    },
    components: {
      PictureInput
    }
  }
</script>
