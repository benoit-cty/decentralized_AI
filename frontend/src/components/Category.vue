<template>
     <v-card>
        <v-card-title>
        All Category Work Orders
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
            :items="orders"
            :loading="loading"
            :search="search"
            class="elevation-1"
            :rows-per-page-items='[10, 25, 100,{"text":"All","value":-1}]'
        >
            <v-progress-linear slot="progress" color="blue" indeterminate></v-progress-linear>
            <template slot="items" slot-scope="props" @click.stop="$emit('input', props.item.id.toString())">
                <tr @click="$emit('input', props.item.id.toString())" v-bind:style="[props.item.remaining > 0 ? { 'background-color': 'mediumseagreen' } : { 'background-color': 'silver' }]">
<td>{{ props.item.value }}</td>
                    <td class="text-xs-right">{{ props.item.category }}</td>
                    <td class="text-xs-right">{{ props.item.id }}</td>

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
</template>

<script>
export default {
    data () {
        return {
            selected: [],
            search: '',
            headers: [
{ text: 'Price (RLC)', value: 'value' },
            { text: 'Category', value: 'id' },
            { text: 'Order ID', value: 'id' },

            { text: 'Remaining', value: 'remaining' },
            { text: 'Volume', value: 'volume' },
            { text: 'Workerpool', value: 'workerpool' },
            { text: 'Trust', value: 'trust' }
            ],
        }
    },
    props: {
        value: {
            type: String
        },
        /*category: {
            type: Number
        },*/
        orders: {
            type: Array
        },
        loading: {
            type: Boolean
        }
    }
}
</script>
