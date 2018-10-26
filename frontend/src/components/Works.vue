<template>
    <v-app>
        <v-toolbar fixed app>
            <v-toolbar-title>
            Works
            </v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn :disabled="loading" @click="getWorks($chainId)">
                {{ loading ? "Loading..." : "Refresh" }}
            </v-btn>
        </v-toolbar>
        <v-content>
            <v-container fluid>
                <v-layout>
                    <v-list two-line>
                        <Work v-for="work in works" v-if="$account && (work.requester.toLowerCase() === $account.toLowerCase())" :key="work._id" :work="work" />
                    </v-list>
                </v-layout>
            </v-container>
        </v-content>
    </v-app>
</template>

<script>
import Work from './Work'

export default {
    data () {
        return {
            works: [],
            loading: false
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
            this.loading = true
            this.works = []
            console.log(chain)
            const result = await this.$http.post('https://gateway.iex.ec/works', {"chainID":chain})
            this.works = result.body.works
            this.loading = false
            //console.log(this.works)
            //console.log(result)
        }
    },
    components: {
        Work
    }
}
</script>
