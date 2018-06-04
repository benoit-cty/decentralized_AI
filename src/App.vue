<template>
  <v-app>
    <v-toolbar fixed app>
      <v-toolbar-title>
        Welcome {{ $account }}
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-title>
        RLC : {{ rlc }}
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-title>
        {{ currChain }}
      </v-toolbar-title>
    </v-toolbar>
    <v-content>
      <v-container fluid>
        <v-layout>
          <v-flex xs6>
            <v-layout>
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
            </v-layout>
            <v-layout row>
              <v-flex xs4>
                <v-subheader>Order ID</v-subheader>
              </v-flex>
              <v-flex xs8>
                <v-text-field
                  id="orderId"
                  name="input-1"
                  label="Enter the order id"
                  v-model="orderId"
                ></v-text-field>
              </v-flex>
            </v-layout>
            <v-layout>
              <v-flex xs4>
                <v-subheader>dApp</v-subheader>
              </v-flex>
              <v-flex xs8>
                <v-text-field
                  id="dapp"
                  name="input-1"
                  label="Enter the dApp address"
                  v-model="dapp"
                ></v-text-field>
              </v-flex>
            </v-layout>
            <v-layout>
              <v-flex xs4>
                <v-subheader>params</v-subheader>
              </v-flex>
              <v-flex xs8>
                <v-text-field
                  id="params"
                  name="input-1"
                  label="Enter the dApp input parameters"
                  v-model="params"
                ></v-text-field>
              </v-flex>
            </v-layout>
            <v-layout>
              <v-btn block raised @click="iexec">
                IExec !
              </v-btn>
            </v-layout>
          </v-flex>
          <v-flex xs6>
            <Orders :contracts="contracts"/>
          </v-flex>
        </v-layout>   
      </v-container>
    </v-content>
     <v-snackbar
      top
      multi-line
      v-model="snackbar"
    >
      {{ message }}
      <v-btn flat color="pink" @click.native="snackbar = false">Close</v-btn>
    </v-snackbar>
  </v-app>
</template>

<script>
  import PictureInput from 'vue-picture-input'
  import Orders from './components/Orders'

  import createIExecContracts from 'iexec-contracts-js-client';
  import { chains, chainsMap } from './chains'
  
  import buffer from 'buffer'

  export default {
    data () {
      return {
        image: null,
        image_url: null,
        snackbar: false,
        message: "",
        orderId: '152',
        dapp: '0xec3CF9FF711268ef329658DD2D233483Bd0127e6',
        params: '{"cmdline":""}'
      }
    },
    computed: {
      contracts () {
        if (this.$ethjs && this.$account && this.$chainId) {
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
    asyncComputed: {
      async rlc () {
        if (!this.contracts) return 0
        const rlcAddress = await this.contracts.fetchRLCAddress();
        const { balance } = await this.contracts
          .getRLCContract({at: rlcAddress})
          .balanceOf(this.$account);
        return balance.toString()
      }
    },
    watch: {
      async contracts (val) {
        console.log(val)
      },
      image_url (url) {
        this.params = `'{"cmdline":"${this.image_url}"}'`
      }
    },
    methods: {
      notify (message) {
        this.message = message
        this.snackbar = true
      },
      onChange (image) {
        console.log('New picture selected!')
        if (image) {
          console.log('Picture loaded.')
          this.image = image
          this.image_url = null
          this.$ipfs.add([buffer.Buffer(image)], (err, res) => {
              if (err) throw err
              const hash = res[0].hash
              console.log('hash', hash);
              this.image_url = `/ipfs/${hash}`
              this.notify(`Image successfully uploaded to IPFS [${this.image_url}]`)
              this.$ipfs.cat(hash, (err, res) => {
                if (err) throw err
                this.image = [].reduce.call(res, (p,c) => p+String.fromCharCode(c),'')
              })
          })
        } else {
          console.log('FileReader API not supported: use the <form>, Luke!')
        }
      },
      async iexec () {
        if (!this.contracts) return
        
        const marketplaceAddress = await this.contracts.fetchMarketplaceAddress();
        const orderRPC = await this.contracts
          .getMarketplaceContract({ at: marketplaceAddress })
          .getMarketOrder(this.orderId);

        console.log(orderRPC)
        
        if (!orderRPC) return
        
        const args = [
          this.orderId,
          orderRPC.workerpool,
          this.dapp, // dappAddress,
          '0x0000000000000000000000000000000000000000', // dataset
          this.params,
          marketplaceAddress, // callback
          '0x0000000000000000000000000000000000000000', // beneficiary
        ]
        const transactionHash = await this.contracts
          .getHubContract()
          .buyForWorkOrder(...args)

        const event = await this.contracts.getHubContract().Deposit((error, result) => {
          console.log('event')
          console.error(error)
          console.log(result)
        });

        this.notify(`Fill order submitted. Waiting for transaction ${transactionHash} to be processed`)
        
        console.log(transactionHash)

        const receipt = await this.contracts.waitForReceipt(transactionHash)
        console.log(receipt)
      }
    },
    components: {
      PictureInput, Orders
    }
  }
</script>
