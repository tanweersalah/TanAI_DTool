<template>
  <q-card class="my-card bg-secondary text-white">
    <q-card-section>
      <div class="text-h6">{{ contianerDetails.image }}</div>
      <!-- <div class="text-subtitle2">{{ contianerDetails.ports }}</div> -->
    </q-card-section>

    <q-card-section>
      {{ contianerDetails.status }}
    </q-card-section>

    <q-card-section>
      Ports : {{ getPorts(contianerDetails.ports) }}
    </q-card-section>

    <q-separator dark />

    <q-card-actions>
      <q-btn flat @click="openLogs(contianerDetails.id)">Check Logs</q-btn>
    </q-card-actions>
  </q-card>
</template>

<script>
export default {
  props: ["contianerDetails"],
  methods: {
    openLogs(id) {
      this.$router.push("/logs/" + id);
    },
    getPorts(ports) {
      const firstKey = Object.keys(ports)[0];
      console.log(ports[firstKey][0]["HostPort"]);
      return `${firstKey} -> ${ports[firstKey][0]["HostPort"]}`;
    },
  },
};
</script>
