import "./assets/main.css";

import { createApp } from "vue";

import { Quasar } from "quasar";

// Import icon libraries
import "@quasar/extras/material-icons/material-icons.css";

// Import Quasar css
import "quasar/src/css/index.sass";

import DockerService from "./services/dockerService";
import DToolAPIService from "./services/dtoolAIApi";

import App from "./App.vue";
import router from "./router";

var dockerService = new DockerService();
var dtoolAPI = new DToolAPIService();

const app = createApp(App);

app.use(Quasar, {
  plugins: {}, // import Quasar plugins and add here
});
app.provide("docker", dockerService);
app.provide("dtool-api", dtoolAPI);
app.use(router);

app.mount("#app");
