<template>
  <v-container class>
    <v-row>Forum</v-row>

    <BoardList v-if="listOn" :List="boardList" @writePageOn="writePageOn" />
    <Write v-if="writeOn" @cancelWrite="listPageOn" />
  </v-container>
</template>

<script>
import BoardList from "@/components/BoardList.vue";
import Write from "@/components/WritePage.vue";
import ex_list from "../assets/ex_list.json";

export default {
  name: "Forum",
  components: {
    BoardList,
    Write
  },
  data: () => ({
    boardList: ex_list.board,
    listOn: true,
    writeOn: false
  }),
  methods: {
    writePageOn: function() {
      (this.listOn = false), (this.writeOn = true);
    },
    listPageOn: function() {
      (this.listOn = true), (this.writeOn = false);
    }
  }
};
</script>