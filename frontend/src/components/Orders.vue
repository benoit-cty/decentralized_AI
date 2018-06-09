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
               <Category :contracts="contracts" :value="value" @input="$emit('input', $event)" :category="n" />
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
    components: {
        Category
    }
}
</script>
