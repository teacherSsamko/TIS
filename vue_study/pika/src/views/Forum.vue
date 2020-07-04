<template>
    <v-container class="">
        <v-row>
            Forum
        </v-row>
        <v-card 
        color="#26c6da"
        dark
        max-width="400">
        <v-card-title>
            <v-icon
                large
                left
            >
                mdi-hand-right
            </v-icon>
            <v-col cols=6>i need help </v-col>
            <v-col cols=4>ssamko</v-col>
        </v-card-title>
        <v-card-subtitle>
            <v-col cols=7>2020-07-06 18:09</v-col>
            <v-col cols=2>likes 19</v-col>
            <v-col cols=2>views 10</v-col>
        </v-card-subtitle>
        </v-card>
        <v-card
            class="mx-auto"
            color="#26c6da"
            dark
            max-width="400"
        >
            <v-card-title>
            <v-icon
                large
                left
            >
                mdi-hand-right
            </v-icon>
            
            <span class="title font-weight-light">HELP</span>
            </v-card-title>

            <v-card-text class="headline font-weight-bold">
            I need help
            </v-card-text>

            <v-card-actions>
            <v-list-item class="grow">
                

                <v-list-item-content>
                <v-list-item-title>SSAMKO</v-list-item-title>
                </v-list-item-content>

                <v-row
                align="center"
                justify="end"
                >
                <v-icon class="mr-1">mdi-heart</v-icon>
                <span class="subheading mr-2">16</span>

                <v-icon class="mr-1">mdi-eye</v-icon>
                <span class="subheading">345</span>
                </v-row>
            </v-list-item>
            </v-card-actions>
        </v-card>
        <v-card
            class="mx-auto"
            color="#26c6da"
            dark
            max-width="400"
        >
            <v-card-title>
            <v-icon
                large
                left
            >
                mdi-alert-circle-outline
            </v-icon>
            
            <span class="title font-weight-light">IDEA</span>
            </v-card-title>

            <v-card-text class="headline font-weight-bold">
            I have an idea
            </v-card-text>

            <v-card-actions>
            <v-list-item class="grow">
                

                <v-list-item-content>
                <v-list-item-title>Jamie</v-list-item-title>
                </v-list-item-content>

                <v-row
                align="center"
                justify="end"
                >
                <v-icon class="mr-1">mdi-heart</v-icon>
                <span class="subheading mr-2">256</span>

                <v-icon class="mr-1">mdi-eye</v-icon>
                <span class="subheading">45</span>
                </v-row>
            </v-list-item>
            </v-card-actions>
        </v-card>
    </v-container>
</template>

<script>
export default {
    name: 'Forum',
}
</script>