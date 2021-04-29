import axios from "axios";

let BASE_URL = "https://fb8e6e92877c.ngrok.io";
if (process.env.NODE_ENV === "development") {
  BASE_URL = "http://localhost:8000";
}

export default axios.create({
  baseURL: `${BASE_URL}/api/v1`,
  headers: {
    "Content-Type": "application/json",
  },
});
