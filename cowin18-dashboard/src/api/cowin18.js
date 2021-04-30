import axios from "axios";

let BASE_URL = "https://rsb0w6kv1i.execute-api.us-east-1.amazonaws.com/dev";
if (process.env.NODE_ENV === "development") {
  BASE_URL = "http://localhost:8000";
}

export default axios.create({
  baseURL: `${BASE_URL}/api/v2`,
  headers: {
    "Content-Type": "application/json",
  },
});
