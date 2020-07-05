<template>
  <v-container class>
    <v-row>
      <h2>
        <router-link :to="{name: 'Write'}">Forum</router-link>
      </h2>
    </v-row>

    <BoardList v-if="listOn" :List="boardList" @writePageOn="writePageOn" />
    <Write v-if="writeOn" @cancelWrite="listPageOn" />
    <Detail :List="boardList" />
    <v-btn @click="showWritePage">test</v-btn>
    <router-view></router-view>
  </v-container>
</template>

<script>
import BoardList from "@/components/BoardList.vue";
import Write from "@/components/WritePage.vue";
import ex_list from "../assets/ex_list.json";
import Detail from "@/components/Detail.vue";

export default {
  name: "Forum",
  components: {
    BoardList,
    Write,
    Detail
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
    },
    showWritePage() {
      this.$router.push({ name: "Write" });
    }
  }
};
</script>

<style scoped>
a {
  text-decoration: none;
  color: black;
}
</style>