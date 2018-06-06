<template>
    <v-container fluid>
        <v-tabs
            color="cyan"
            dark
            slider-color="yellow"
        >
            <v-tab
                v-for="n in 5"
                :key="n"
                ripple
            >
                Category {{ n }}
            </v-tab>
            <v-tab-item
                v-for="n in 5"
                :key="n"
            >
                <v-card style="max-height: 750px" class="scroll-y">
                <v-card-text>
                    <v-list two-line subheader>
                        <v-subheader inset>Order Book</v-subheader>
                        <v-list-tile 
                            v-for="item in orders" 
                            v-if="item.category === n" 
                            :key="item.id" 
                            avatar 
                            @click="$emit('input', item.id.toString())">
                            <v-list-tile-avatar>
                            <span>{{ item.id }}</span>
                            </v-list-tile-avatar>
                            <v-list-tile-content>
                            <v-list-tile-title>remaining : {{ item.remaining }} / {{ item.volume }}</v-list-tile-title>
                            <v-list-tile-sub-title>{{ item.workerpool }}</v-list-tile-sub-title>
                            </v-list-tile-content>
                            <v-list-tile-action>
                            <v-btn v-if="value === item.id.toString()" icon ripple>
                                <v-icon color="green lighten-1">check</v-icon>
                            </v-btn>
                            </v-list-tile-action>
                        </v-list-tile>
                    </v-list>
                </v-card-text>
                </v-card>
            </v-tab-item>
        </v-tabs>
    </v-container>
</template>

<script>
export default {
    data () {
        return {
            orders: []
        }
    },
    mounted () {
        this.updateOrders()
    },
    watch: {
        contracts (contracts) {
            this.updateOrders();
        }
    },
    props: {
        contracts: {
            type: Object
        },
        value: {
            type: String
        }
    },
    computed: {
        sortedOrders () {
            return this.orders.sort((a, b) => a.remaining > b.remaining)
        }
    },
    methods: {
        async updateOrders () {
            if (!this.contracts) return
            this.orders = []
            const marketplaceAddress = await this.contracts.fetchMarketplaceAddress();
            for (let i = 100; i < 200; i++) {
                const order = await this.contracts
                    .getMarketplaceContract({ at: marketplaceAddress })
                    .getMarketOrder(i.toString())
                if (order) {
                    this.orders.push({
                        category: order.category.toNumber(),
                        remaining: order.remaining.toNumber(),
                        volume: order.volume.toNumber(),
                        workerpool: order.workerpool,
                        trust: order.trust.toString(),
                        direction: order.direction.toString(),
                        id: i
                    })
                }
            }
        }
    }
}
</script>
