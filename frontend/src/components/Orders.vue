<template>
    <v-container fluid>

               <Category :value="value" @input="$emit('input', $event)" :orders="orders" :loading="loading"/>

    </v-container>
</template>

<script>
import Category from './Category'

export default {
    props: {
        contracts: {
            type: Object
        },
        value: {
            type: String
        }
    },
    data () {
        return {
            orders: [],
            loading: false
        }
    },
    async mounted () {
        this.getOrders(this.$chainId)
    },
    watch: {
        $chainId (chain) {
            this.getOrders(chain)
        }
    },
    methods: {

        async getOrders(chain) { //async
            this.loading = true
            this.orders = []
            console.log(chain)
            /* curl 'https://gateway.iex.ec/orders' -H 'origin: https://market.iex.ec' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: en-US,en;q=0.9,fr;q=0.8' -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/70.0.3538.67 Chrome/70.0.3538.67 Safari/537.36' -H 'content-type: application/json' -H 'accept: application/json' -H 'referer: https://market.iex.ec/' -H 'authority: gateway.iex.ec' --data-binary            '{"chainID":"42","find":{"category":"3","status":"open"},"sort":{"value":1,"blockTimestamp":-1},"limit":20}' --compressed */
            /*
            {"ok":true,"orders":[{"_id":"5bcf5930a22aad053a250b9f","transactionHash":"0x9be003ba7a03ca959755e199070993c784fbaf5d989e0c8ac564f438ecbc2208","direction":"2","category":"3","trust":"10","value":"154","volume":1,"remaining":1,"workerpool":"0x4899295937f3F7eEe4be1D2AD658788c6c9272B6","workerpoolOwner":"0xB40c7659A6a359279A560676F4Cd9e07C4C13b08","marketorderIdx":"1175","status":"open","chainID":42,"blockNumber":9164003,"blockTimestamp":"2018-10-23T17:24:00.000Z"},{"_id":"5bcf6188a22aad053a251478","transactionHash":"0x8000416108f6b986f43ea2fda50ffab8bd81b9f14b304eb8236cc34c735adb34","direction":"2","category":"3","trust":"10","value":"166","volume":1,"remaining":1,"workerpool":"0x4899295937f3F7eEe4be1D2AD658788c6c9272B6","workerpoolOwner":"0xB40c7659A6a359279A560676F4Cd9e07C4C13b08","marketorderIdx":"1176","status":"open","chainID":42,"blockNumber":9164240,"blockTimestamp":"2018-10-23T17:59:36.000Z"},{"_id":"5bc8aa78a22aad053a1e4cc8","transactionHash":"0x2d4e913ae49cd73a1fa1990a147ea6e61a7159fed6300b430d380b909ef50dd4","direction":"2","category":"3","trust":"10","value":"173","volume":1,"remaining":1,"workerpool":"0x4899295937f3F7eEe4be1D2AD658788c6c9272B6","workerpoolOwner":"0xB40c7659A6a359279A560676F4Cd9e07C4C13b08","marketorderIdx":"1119","status":"open","chainID":42,"blockNumber":9115487,"blockTimestamp":"2018-10-18T15:44:56.000Z"},{"_id":"5bc8aad0a22aad053a1e4d24","transactionHash":"0x2f34c9e87ada5758c1220647e4a7d653cc60563b6d9de883617249dee1d87a55","direction":"2","category":"3","trust":"10","value":"198","volume":1,"remaining":1,"workerpool":"0x4899295937f3F7eEe4be1D2AD658788c6c9272B6","workerpoolOwner":"0xB40c7659A6a359279A560676F4Cd9e07C4C13b08","marketorderIdx":"1120","status":"open","chainID":42,"blockNumber":9115497,"blockTimestamp":"2018-10-18T15:46:24.000Z"}]}
            */
            const result = await this.$http.post('https://gateway.iex.ec/orders',
             {"chainID":chain,"find":{"status":"open"},
             "sort":{"value":1,"blockTimestamp":-1},"limit":20});
            //const result = await this.$http.post('https://gateway.iex.ec/orders', {"chainID":chain,"find":{"category":"5","status":"filled"},"sort":{"blockTimestamp":-1}})
            console.log(result)
            console.log(result.body)

            // loop through each sensoer object, ignore top level key value

            this.orders = result.body.orders.map( (order) => ({
                          category: order.category,
                          remaining: order.remaining,
                          value: order.value,
                          volume: order.volume,
                          workerpool: order.workerpool,
                          trust: order.trust,
                          direction: order.direction,
                          id: order.marketorderIdx
                      })
                  )




            /*
            result.body.orders.forEach( (order) => {
                console.log(order.marketorderIdx);
                item.id = order.marketorderIdx;
                item.value = order.value.toNumber();
                */
                /*
                {
                  "_id": "5bcf5930a22aad053a250b9f",
                  "transactionHash": "0x9be003ba7a03ca959755e199070993c784fbaf5d989e0c8ac564f438ecbc2208",
                  "direction": "2",
                  "category": "3",
                  "trust": "10",
                  "value": "154",
                  "volume": 1,
                  "remaining": 1,
                  "workerpool": "0x4899295937f3F7eEe4be1D2AD658788c6c9272B6",
                  "workerpoolOwner": "0xB40c7659A6a359279A560676F4Cd9e07C4C13b08",
                  "marketorderIdx": "1175",
                  "status": "open",
                  "chainID": 42,
                  "blockNumber": 9164003,
                  "blockTimestamp": "2018-10-23T17:24:00.000Z"
                },
                */
                /*
                category: order.category.toNumber(),
                remaining: order.remaining.toNumber(),
                value: order.value.toNumber(),
                volume: order.volume.toNumber(),
                workerpool: order.workerpool,
                trust: order.trust.toString(),
                direction: order.direction.toString(),
                id: i
                */
      /*          this.orders.push(item)
            });
*/
            //this.orders = result.body.orders
            this.loading = false
            console.log(this.orders)
            return this.orders
        },
        async getSyncOrders(chain){
          const orders =  getOrders(chain);
          const response = await orders
          return response
        }
    },
    components: {
        Category
    }
}
</script>
