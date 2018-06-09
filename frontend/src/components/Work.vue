<template>
    <v-list-tile
        ripple
        @click="onClick">
        <v-list-tile-action>
            <v-icon :color="colorStatus">{{ iconStatus }}</v-icon>
        </v-list-tile-action>
        <v-list-tile-content>
            <v-list-tile-title>
            {{ work.woid }}
            </v-list-tile-title>
            <v-list-tile-sub-title>
                {{ work.uri }}
            </v-list-tile-sub-title>
        </v-list-tile-content>
    </v-list-tile>
</template>

<script>
import { chainsMap } from '../chains'
export default {
    props: {
        work: {
            type: Object,
            required: true
        }
    },
    computed: {
        iconStatus () {
            switch (this.work.status) {
                case "1":
                    return 'sync'
                case "4":   
                    return 'check_circle'
            }
        },
        colorStatus () {
            switch (this.work.status) {
                case "1":
                    return 'orange'
                case "4":   
                    return 'green'
            }
        },
    },
    mounted () {
        console.log(this.work)
    },
    methods: {
        onClick () {
            if (this.work.uri) {
                const download = this.$iexec.createDownloadURI(this.work.uri)
                console.log(download)
                window.open(download)
            } else {
                window.open(`https://explorer.iex.ec/${chainsMap[this.$chainId]}/work/${this.work.transactionHash}`)
            }
        }
    }
}
</script>
