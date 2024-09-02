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
}
