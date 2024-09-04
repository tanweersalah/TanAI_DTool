// movieService.js

import axios from "axios";

export default class DToolAPIService {
  constructor() {
    this.baseUrl = "http://localhost:8080/chain/invoke";
  }

  async callApi(input) {
    const requestBody = {
      input: {
        input: JSON.stringify(input),
      },
      config: {},
      kwargs: {},
    };

    try {
      console.log("Start:", input);
      const response = await axios.post(this.baseUrl, requestBody);
      console.log("Response:", response.data);
      return response.data;
    } catch (error) {
      console.error("Error:", error);
    }
  }
}
