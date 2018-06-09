<template>
    <v-list-tile
        ripple
        @click="toggle(index)">
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
                    return 'error'
                case "4":   
                    return 'check_circle'
            }
        },
        colorStatus () {
            switch (this.work.status) {
                case "1":
                    return 'red'
                case "4":   
                    return 'green'
            }
        }
    }
}
</script>
