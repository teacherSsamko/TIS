<template>
  <v-container>
    <v-card
      class="mx-auto mb-4"
      color="#26c6da"
      dark
      max-width="90%"
      v-for="item in List"
      :key="item.no"
    >
      <v-card-title>
        <v-icon large left>mdi-hand-right</v-icon>

        <span class="title font-weight-light">{{item.category}}</span>
        <span class="title">{{item.title}}</span>
        <v-row align="center" justify="end">
          <span class="subheading mr-2">{{item.user}}</span>
        </v-row>
      </v-card-title>
      <v-card-text class="headline font-weight-bold">{{item.content}}</v-card-text>
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
    <v-row justify="end" width="100%" class="pr-12">
      <v-card width="80%">
        <v-card-title>JK</v-card-title>
        <v-card-text>What?</v-card-text>
      </v-card>
    </v-row>
  </v-container>
</template>

<script>
export default {
  props: {
    List: Array
  },
  data: function() {},
  computed: {}
};
</script>