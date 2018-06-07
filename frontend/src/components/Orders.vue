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
                <v-card>
                    <v-card-title>
                    Category {{ n }} Work Orders
                    <v-spacer></v-spacer>
                    <v-text-field
                        v-model="search"
                        append-icon="search"
                        label="Search"
                        single-line
                        hide-details
                    ></v-text-field>
                    </v-card-title>
                    <v-data-table
                        :headers="headers"
                        :items="ordersByCategory(n)"
                        :loading="loading"
                        :search="search"
                        class="elevation-1"
                        :rows-per-page-items='[10, 25, 100,{"text":"All","value":-1}]'
                    >
                        <v-progress-linear slot="progress" color="blue" indeterminate></v-progress-linear>
                        <template slot="items" slot-scope="props" @click.stop="$emit('input', props.item.id.toString())">
                            <tr @click="$emit('input', props.item.id.toString())" v-bind:style="[props.item.remaining > 0 ? { 'background-color': 'mediumseagreen' } : { 'background-color': 'silver' }]">
                                <td>{{ props.item.id }}</td>
                                <td class="text-xs-right">{{ props.item.value }}</td>
                                <td class="text-xs-right">{{ props.item.remaining }}</td>
                                <td class="text-xs-right">{{ props.item.volume }}</td>
                                <td class="text-xs-right">{{ props.item.workerpool }}</td>
                                <td class="text-xs-right">{{ props.item.trust }}</td>
                            </tr>
                        </template>
                        <v-alert slot="no-results" :value="true" color="error" icon="warning">
                            Your search for "{{ search }}" found no results.
                        </v-alert>
                        <template slot="no-data">
                            <v-alert :value="true" color="error" icon="warning">
                                Sorry, no work order to display here :(
                            </v-alert>
                        </template>
                    </v-data-table>
                </v-card>
            </v-tab-item>
        </v-tabs>
    </v-container>
</template>

<script>
export default {
    data () {
        return {
            loading: true,
            selected: [],
            search: '',
            orders: [],
            headers: [
            { text: 'ID', value: 'id' },
            { text: 'Price (RLC)', value: 'value' },
            { text: 'Remaining', value: 'remaining' },
            { text: 'Volume', value: 'volume' },
            { text: 'Workerpool', value: 'workerpool' },
            { text: 'Trust', value: 'trust' }
            ],
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
        },
        ordersByCategory () {
            return (n) => this.orders.filter((order) => order.category === n)
        }
    },
    methods: {
        async updateOrders () {
            if (!this.contracts) return
            this.loading = true
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
                        value: order.value.toNumber(),
                        volume: order.volume.toNumber(),
                        workerpool: order.workerpool,
                        trust: order.trust.toString(),
                        direction: order.direction.toString(),
                        id: i
                    })
                }
            }
            this.loading = false
        }
    }
}
</script>
