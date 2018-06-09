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
      <v-spacer></v-spacer>
        <v-btn icon @click.stop="drawer = !drawer">
          <v-icon>menu</v-icon>
        </v-btn>
    </v-toolbar>
    <v-content>
      <v-container fluid>
        <v-layout>
          <v-flex xs4>
            <v-layout>
              <v-card width="100%">
                <img v-if="image_url" @click="inputFile" :src="image_url" width="100%">
                <img v-else src="https://cdn-images-1.medium.com/max/1600/0*I0nyARrHiSl-a3lZ." @click="inputFile" width="100%">
                <v-progress-linear indeterminate v-if="uploading"></v-progress-linear>
                <v-card-text>
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
                      <v-subheader>image url</v-subheader>
                    </v-flex>
                    <v-flex xs8>
                      <v-text-field
                        id="params"
                        name="input-1"
                        label="Enter the dApp input image url"
                        v-model="image_url"
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
                        label="dApp input parameters"
                        v-model="params"
                        disabled
                      ></v-text-field>
                    </v-flex>
                  </v-layout>
                </v-card-text>
              </v-card>
              <input
                v-show="false"
                ref="file-input"
                accept="image/*"
                type="file"
                @change="onChange">
            </v-layout>

            <v-layout>
              <v-btn :disabled="!image_url" block raised @click="iexec(orderId)">
                IExec !
              </v-btn>
            </v-layout>
          </v-flex>
          <v-flex xs8>
            <Orders :contracts="contracts" v-model="orderId"/>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
    <v-navigation-drawer
      temporary
      right
      v-model="drawer"
      fixed
      :width="600"
    >
      <Works />
     </v-navigation-drawer>
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
  import Orders from './components/Orders'
  import Works from './components/Works'
  import createIExecContracts from 'iexec-contracts-js-client';
  import { chains, chainsMap } from './chains'

  import buffer from 'buffer'
  
  const Extensions = require('iexec-poco-v2/utils/extensions.js');

  export default {
    data () {
      return {
        drawer: false,
        image_url: 'https://cdn-images-1.medium.com/max/1600/0*I0nyARrHiSl-a3lZ.',
        snackbar: false,
        uploading: false,
        message: "",
        orderId: null,
        dapp: '0xec3CF9FF711268ef329658DD2D233483Bd0127e6',
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
      },
      params () {
        return `{"cmdline":"${this.image_url}"}`
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
      }
    },
    methods: {
      notify (message) {
        this.message = message
        this.snackbar = true
      },
      onChange (e) {
        const f = e.target.files[0]
        if (f) {
          const reader = new FileReader();
          this.uploading = true
          reader.onloadend = () => {
            const buf = buffer.Buffer(reader.result)
            this.$ipfs.files.add(buf, (err, res) => {
                if (err) throw err
                const hash = res[0].hash
                console.log('hash', hash);
                this.uploading = false
                this.image_url = `https://ipfs.io/ipfs/${hash}`
                this.notify(`Image successfully uploaded to IPFS ${this.image_url}`)
                // this.$ipfs.cat(hash, (err, res) => {
                //   if (err) throw err
                //   this.image = [].reduce.call(res, (p,c) => p+String.fromCharCode(c),'')
                // })
            })
          }
          reader.readAsArrayBuffer(f);
        }
      },
      async iexec (orderId) {
        if (!this.contracts) return

        const marketplaceAddress = await this.contracts.fetchMarketplaceAddress();
        const orderRPC = await this.contracts
          .getMarketplaceContract({ at: marketplaceAddress })
          .getMarketOrder(orderId);

        if (!orderRPC) return

        const args = [
          orderId,
          orderRPC.workerpool,
          this.dapp, // dappAddress,
          '0x0000000000000000000000000000000000000000', // dataset
          this.params,
          '0x0000000000000000000000000000000000000000', // callback
          this.$account, // beneficiary
        ]
        const aIexecHubInstance = await this.contracts.getHubContract()
        const txMined = await aIexecHubInstance.buyForWorkOrder(...args, {
          from: this.$account
        })
        console.log(txMined)
        const receipt = await this.contracts.waitForReceipt(txMined)
        this.notify(`Fill order submitted. Waiting for transaction ${txMined} to be processed`)

        if (receipt.status === "0x0") {
          this.notify('Error processing the transaction')
        }
        const events = await Extensions.getEventsPromise(aIexecHubInstance.WorkOrderActivated({}),orderId,10000000);
        let woid = events[0].args.woid;
        console.log(woid)
        let aWorkOrderInstance = await this.contracts.getWorkOrderContract().at(woid);
        console.log(aWorkOrderInstance)
        let status = await aWorkOrderInstance.m_status.call();
        console.log(status)

        const completed = await Extensions.getEventsPromise(aIexecHubInstance.WorkOrderActivated({}),orderId,10000000);
        console.log(complete)
      },
      inputFile () {
        this.$refs['file-input'].click();
      },
    },
    components: {
       Orders, Works
    }
  }
</script>
