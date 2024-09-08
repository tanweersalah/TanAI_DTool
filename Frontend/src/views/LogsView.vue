<template>
  <div>
    <h3>Select a log to get help</h3>

    <q-toolbar
      class="bg-teal outlined text-white shadow-2 rounded-borders toolbar"
    >
      <q-btn to="/" stretch flat label="Home" />

      <q-space />

      <q-btn stretch flat icon="sync" @click="getlogs" />
      <q-btn stretch flat icon="sort" @click="sortLogs" />

      <q-separator dark vertical />

      <q-select
        class="log_count"
        dark
        filled
        v-model="logs_count"
        :options="count_options"
        label="Logs Count"
      />

      <q-separator dark vertical />

      <q-toggle v-model="error_only" color="red" label="Error Only" />
    </q-toolbar>

    <div :class="['log-grid', { 'two-column': isTwoColumn }]">
      <q-scroll-area class="log-area">
        <q-list dark bordered separator style="max-width: 90vw">
          <q-item
            clickable
            @click="openChat(log, index)"
            v-ripple
            v-for="(log, index) in logs.logs"
            :key="index"
            :class="{ selectedLog: index == selectedIndex }"
          >
            <q-item-section side top>
              <q-item-label caption>{{
                formatRelativeTime(log.timestamp)
              }}</q-item-label>
            </q-item-section>
            <q-item-section style="word-break: break-all">{{
              log.message
            }}</q-item-section>
          </q-item>
          <q-inner-loading
            dark
            :showing="loadvisible"
            label="Please wait..."
            label-class="text-teal"
            label-style="font-size: 1.1em"
          /> </q-list
      ></q-scroll-area>

      <div v-if="isTwoColumn">
        <q-btn label="Close Chat" @click="toggleLayout" />
        <q-scroll-area class="llm-area" style="height: 80vh">
          <div v-if="!chatLog">
            <q-skeleton type="text" class="text-subtitle1" />
            <q-skeleton type="text" width="50%" class="text-subtitle1" />
            <q-skeleton type="text" class="text-caption" />
          </div>

          <div>
            <vue-markdown
              :source="chatLog['output']"
              v-if="chatLog"
              class="ai-chatbox"
            />
          </div>
        </q-scroll-area>
      </div>
    </div>
  </div>
</template>

<script>
import { inject } from "vue";
import { formatRelativeTime } from "../utils/utils";
import VueMarkdown from "vue-markdown-render";
export default {
  components: {
    VueMarkdown,
  },
  props: {
    id: {
      type: String,
      required: true,
    },
  },

  methods: {
    formattedText(text) {
      return text.replace(/\n/g, "<br>");
    },
    formatRelativeTime,
    toggleLayout() {
      this.isTwoColumn = !this.isTwoColumn;
      console.log(this.isTwoColumn);
      this.selectedIndex = null;
    },
    async openChat(log, index) {
      this.selectedIndex = index;
      this.isTwoColumn = true;
      this.chatLog = null;
      this.chatLog = await this.dtoolApi.callApi(log);
      this.selectedIndex = index;
    },
    async getlogs() {
      console.log("Refresh logs");
      this.logs = await this.docker.getContainerLogs(
        this.id,
        this.logs_count,
        this.error_only
      );
      this.isAscending = !this.isAscending;
      this.sortLogs();
    },

    sortLogs() {
      console.log(this.logs.logs);
      this.isAscending = !this.isAscending;
      this.logs.logs.sort((a, b) => {
        const timestampA = new Date(a.timestamp).getTime();
        const timestampB = new Date(b.timestamp).getTime();
        return this.isAscending
          ? timestampA - timestampB
          : timestampB - timestampA;
      });
    },
  },
  async beforeMount() {
    this.loadvisible = true;
    await this.getlogs();
    this.loadvisible = false;
  },
  watch: {
    error_only() {
      this.getlogs();
    },
    logs_count() {
      this.getlogs();
    },
  },
  data() {
    return {
      logs_count: 10,
      isAscending: true,
      count_options: [10, 30, 50, 100, 200],
      error_only: false,
      isTwoColumn: false,
      loadvisible: true,
      chatLog: null,
      selectedIndex: null,
      docker: inject("docker"),
      dtoolApi: inject("dtool-api"),
      logs: {
        container_id:
          "ced0643cd2d1065addf370fd27c0448b388ee34dfa61fc39c6190cdb391c49cf",
        logs: null,
        examplelogs: [
          {
            timestamp: "2024-09-03T07:23:29.409757315Z",
            message:
              '172.71.172.122 - - [03/Sep/2024:07:23:29 +0000] "GET /logs/ced0643cd2d1065addf370fd27c0448b388ee34dfa61fc39c6190cdb391c49cf?filter_errors=true&tail=5 HTTP/1.1" 200 1259 "https://logapi.tanflix.me/docs" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"',
          },
          {
            timestamp: "2024-09-03T07:23:32.328187277Z",
            message:
              '172.71.172.122 - - [03/Sep/2024:07:23:32 +0000] "GET /logs/ced0643cd2d1065addf370fd27c0448b388ee34dfa61fc39c6190cdb391c49cf?filter_errors=true&tail=5 HTTP/1.1" 200 1646 "https://logapi.tanflix.me/docs" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"',
          },
          {
            timestamp: "2024-09-03T07:23:41.758455104Z",
            message:
              '172.71.172.122 - - [03/Sep/2024:07:23:41 +0000] "GET /logs/ced0643cd2d1065addf370fd27c0448b388ee34dfa61fc39c6190cdb391c49cf?filter_errors=true&tail=5 HTTP/1.1" 200 2033 "https://logapi.tanflix.me/docs" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"',
          },
          {
            timestamp: "2024-09-03T07:23:48.778935018Z",
            message:
              '172.71.172.122 - - [03/Sep/2024:07:23:48 +0000] "GET /logs/ced0643cd2d1065addf370fd27c0448b388ee34dfa61fc39c6190cdb391c49cf?filter_errors=true&tail=5 HTTP/1.1" 200 2029 "https://logapi.tanflix.me/docs" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"',
          },
          {
            timestamp: "2024-09-03T07:23:56.670667499Z",
            message:
              '172.71.172.122 - - [03/Sep/2024:07:23:56 +0000] "GET /logs/ced0643cd2d1065addf370fd27c0448b388ee34dfa61fc39c6190cdb391c49cf?filter_errors=false&tail=5 HTTP/1.1" 200 2026 "https://logapi.tanflix.me/docs" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"',
          },
        ],
      },
    };
  },
};
</script>

<style scoped>
.toolbar {
  margin-top: 20px;

  height: 10px;
}

.log_count {
  width: 130px;
}
.log-area {
  height: 85vh;
  max-width: 100%;
  margin-top: 20px;
}

.selectedLog {
  background-color: rgba(0, 94, 255, 0.257);
}

.ai-chatbox {
  padding: 10px;
  max-width: 40vw;
  overflow-wrap: break-word;
}
.log-grid {
  display: flex;
  gap: 20px;
  transition: all 2s ease-in-out;
}

.log-grid > * {
  flex-basis: 100%;
  transition: flex-basis 1s ease-in-out, max-width 1s ease-in-out;
}

.log-grid.two-column > * {
  flex-basis: calc(50% - 10px);
  max-width: calc(50% - 10px);
}

.llm-area {
  padding: 10px;
  border: 1px solid white;
  border-radius: 8px;
  overflow: hidden;
}

/* Hide the second column when in single column mode */
.log-grid > *:nth-child(2) {
  width: 0px;
  max-width: 0;
  padding: 0;
  opacity: 0;
}

.log-grid.two-column > *:nth-child(2) {
  max-width: calc(50% - 10px);
  padding: 10px;
  opacity: 1;
}
</style>
