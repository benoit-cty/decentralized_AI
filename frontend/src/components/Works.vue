<template>
    <v-container fluid>
        <v-layout>
            <v-list two-line>
                <Work v-for="work in works" v-if="work.requester.toLowerCase() === $account.toLowerCase()" :key="work._id" :work="work" />
            </v-list>
        </v-layout>
    </v-container>
</template>

<script>
import Work from './Work'

export default {
    data () {
        return {
            works: []
        }
    },
    async mounted () {
        this.getWorks(this.$chainId)
    },
    watch: {
        $chainId (chain) {
            this.getWorks(chain)
        }
    },
    methods: {
        async getWorks (chain) {
            console.log(chain)
            const result = await this.$http.post('https://gateway.iex.ec/works', {"chainID":chain})
            this.works = result.body.works
            console.log(this.works)
            console.log(result)
        }
    },
    components: {
        Work
    }
}
</script>
