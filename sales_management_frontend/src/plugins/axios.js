import axios from "axios";

const axiosInstance = axios.create({
  baseURL: "http://localhost:8000/api/v1/", // connecting to my django server
});

export default axiosInstance;
