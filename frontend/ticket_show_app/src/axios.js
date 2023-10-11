import axios from "axios";
import router from "./router";
import store from "./store";

const instance = axios.create({
  baseURL: "http://127.0.0.1:8080/",
});

instance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

instance.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (
      error.response &&
      error.response.data &&
      error.response.data.msg === "Token has expired"
    ) {
      alert("Token has expired. Please log in again.");

      store.dispatch("logoutUser");
      router.push({ name: "adminlogin" });
    }
    return Promise.reject(error);
  }
);

export default instance;
