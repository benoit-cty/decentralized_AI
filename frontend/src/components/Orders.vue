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
               <Category :value="value" @input="$emit('input', $event)" :orders="categoryOrdersWithRemaining(n)"  :category="n" :loading="loading"/>
            </v-tab-item>
        </v-tabs>
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
            loading: false,
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
    computed: {
        categoryOrdersWithRemaining () {
            return (category) => this.orders.filter((order) => (order.category === category && order.remaining > 0))
        }
    },
    methods: {
        async updateOrders () {
            if (!this.contracts) return
            this.loading = true
            let promises = []
            const batch_size = 20
            this.orders = []
            const marketplaceAddress = await this.contracts.fetchMarketplaceAddress();
            for (let i = 100; i < 1000; i++) {
                promises.push(this.contracts
                                .getMarketplaceContract({ at: marketplaceAddress })
                                .getMarketOrder(i.toString()))
                if (promises.length === batch_size) {
                    this.orders = this.orders.concat((await Promise.all(promises))
                        .filter((order => order))
                        .map((order) => ({
                                    category: order.category.toNumber(),
                                    remaining: order.remaining.toNumber(),
                                    value: order.value.toNumber(),
                                    volume: order.volume.toNumber(),
                                    workerpool: order.workerpool,
                                    trust: order.trust.toString(),
                                    direction: order.direction.toString(),
                                    id: i
                                })
                        )
                    )
                    promises = []
                }
            }
            if (promises.length === batch_size) {
                this.orders = (await Promise.all(promises))
                    .filter((order => order))
                    .map((order) => ({
                                category: order.category.toNumber(),
                                remaining: order.remaining.toNumber(),
                                value: order.value.toNumber(),
                                volume: order.volume.toNumber(),
                                workerpool: order.workerpool,
                                trust: order.trust.toString(),
                                direction: order.direction.toString(),
                                id: i
                            })
                    )
                promises = []
            }
            this.loading = false
        }
    },
    components: {
        Category
    }
}
</script>
