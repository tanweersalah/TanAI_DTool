<template>
  <div>
    <h3>Containers</h3>
    <div class="docker-list">
      <div v-for="(item, index) in container_lists" :key="index">
        <DockerContainer :contianerDetails="item" />
      </div>
      <q-inner-loading
        dark
        :showing="loadvisible"
        label="Please wait..."
        label-class="text-teal"
        label-style="font-size: 1.1em"
      />
    </div>
  </div>
</template>

<style>
.docker-list {
  padding-top: 20px;
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}
</style>

<script>
import { inject } from "vue";
import DockerContainer from "../components/DockerContainer.vue";

export default {
  components: { DockerContainer },
  async beforeMount() {
    this.loadvisible = true;
    this.container_lists = await this.docker.getContainerList();
    this.loadvisible = false;
    console.log(this.container_lists);
  },
  methods: {},
  data() {
    return {
      loadvisible: true,
      docker: inject("docker"),
      container_lists: null,
    };
  },
};
</script>
