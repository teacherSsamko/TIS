<template>
  <v-container>
    <v-row>
      <v-select :items="categories" label="Outlined style" outlined></v-select>
    </v-row>
    <v-row>
      <v-text-field label="Title" outlined></v-text-field>
    </v-row>
    <v-row>
      <v-textarea outlined label="Content"></v-textarea>
    </v-row>
    <v-row>
      <v-btn>write</v-btn>
      <v-btn @click="cancelWrite">cancel</v-btn>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    categories: ["HELP", "IDEA"]
  }),
  methods: {
    cancelWrite: function() {
      this.$emit("cancelWrite");
    }
  }
};
</script>