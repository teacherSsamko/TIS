<template>
  <v-container class>
    <v-row>Forum</v-row>

    <BoardList :List="boardList" />
    <button class="btn btn-primary">write</button>
    <Write />
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
    boardList: ex_list.board
  })
};
</script>