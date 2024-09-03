// movieService.js

import axios from "axios";

export default class DockerService {
  constructor() {
    this.baseUrl = "https://logapi.tanflix.me/";
  }

  async getContainerList() {
    try {
      const response = await axios.get(this.baseUrl + "containers");
      return response.data;
    } catch (error) {
      throw new Error(`Error fetching container list: ${error.message}`);
    }
  }
  async getContainerLogs(container_id, total_logs, filter_error) {
    try {
      const response = await axios.get(
        this.baseUrl + "logs" + "/" + container_id,
        {
          params: {
            filter_errors: filter_error,
            tail: total_logs,
          },
        }
      );
      return response.data;
    } catch (error) {
      throw new Error(`Error fetching container logs: ${error.message}`);
    }
  }
}
