<template>
  <div>
    <h3>Containers</h3>
    <div class="docker-list">
      <div v-for="(item, index) in container_lists" :key="index">
        <DockerContainer :contianerDetails="item" />
      </div>
    </div>
  </div>
</template>

<style>
.docker-list {
  padding-top: 20px;
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
    this.container_lists = await this.docker.getContainerList();
    console.log(container_lists);
  },
  methods: {},
  data() {
    return {
      docker: inject("docker"),
      container_lists: [
        {
          name: "1",
          ports: "8080:80",
          status: "running",
          image: "nginx:latest",
        },
        {
          name: "2",
          ports: "3306:3306",
          status: "stopped",
          image: "mysql:5.7",
        },
        {
          name: "3",
          ports: "6379:6379",
          status: "running",
          image: "redis:alpine",
        },
      ],
    };
  },
};
</script>
