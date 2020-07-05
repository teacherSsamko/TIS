<template>
  <v-app>
    <v-content v-if="isHome">
      <HelloWorld />
      <About />
    </v-content>
    <v-main v-if="isForum">
      <Forum />
    </v-main>
  </v-app>
</template>

<script>
import HelloWorld from "./components/HelloWorld";
import About from "./views/About";
import Forum from "./views/Forum";

export default {
  name: "App",

  components: {
    HelloWorld,
    About,
    Forum
  },

  data: () => ({
    isHome: false,
    isForum: true
  })
};
</script>
