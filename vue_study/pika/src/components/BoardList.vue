<template>
  <v-container>
    <v-card class="mx-auto mb-4" color="#26c6da" dark max-width="400">
      <v-card-title>
        <v-icon large left>mdi-hand-right</v-icon>

        <span class="title font-weight-light">HELP</span>
        <v-row align="center" justify="end">
          <span class="subheading mr-2">SSAMKO</span>
        </v-row>
      </v-card-title>
      <v-card-text class="headline font-weight-bold">I need help</v-card-text>
      <v-card-actions>
        <v-list-item class="grow">
          <v-list-item-content>
            <v-list-item-title>2020-07-06 18:09</v-list-item-title>
          </v-list-item-content>
          <v-row align="center" justify="end">
            <v-icon class="mr-1">mdi-heart</v-icon>
            <span class="subheading mr-2">16</span>
            <v-icon class="mr-1">mdi-eye</v-icon>
            <span class="subheading">345</span>
          </v-row>
        </v-list-item>
      </v-card-actions>
    </v-card>
    <v-card
      class="mx-auto mb-4"
      color="#26c6da"
      dark
      max-width="400"
      v-for="(item) in List"
      :key="item.no"
    >
      <v-card-title>
        <v-icon large left>mdi-hand-right</v-icon>

        <span class="title font-weight-light">{{item.category}}</span>
        <v-row align="center" justify="end">
          <span class="subheading mr-2">{{item.user}}</span>
        </v-row>
      </v-card-title>
      <v-card-text class="headline font-weight-bold">{{item.title}}</v-card-text>
      <v-card-actions>
        <v-list-item class="grow">
          <v-list-item-content>
            <v-list-item-title>{{item.reg_date}}</v-list-item-title>
          </v-list-item-content>
          <v-row align="center" justify="end">
            <v-icon class="mr-1">mdi-heart</v-icon>
            <span class="subheading mr-2">{{item.like}}</span>
            <v-icon class="mr-1">mdi-eye</v-icon>
            <span class="subheading">{{item.view}}</span>
          </v-row>
        </v-list-item>
      </v-card-actions>
    </v-card>
    <v-btn @click="writePageOn">write</v-btn>
  </v-container>
</template>

<script>
export default {
  name: "BoardList",
  props: {
    List: Array,
    listOn: Boolean,
    writeOn: Boolean
  },
  data: () => ({}),
  methods: {
    writePageOn: function() {
      this.$emit("writePageOn");
    }
  }
};
</script>