import { createStore } from "vuex";
import axios from "../axios.js";
import router from "../router/index.js";

const store = createStore({
  state() {
    return {
      loggedIn: localStorage.getItem("token") ? true : false,
      role: null,
    };
  },
  getters: {
    token(state) {
      if (state.loggedIn === true) {
        return localStorage.getItem("token");
      } else {
        return null;
      }
    },
    role(state) {
      return state.role;
    },
  },
  mutations: {
    login(state, role) {
      state.loggedIn = true;
      state.role = role;
    },
    logout(state) {
      state.loggedIn = false;
    },
    resetRole(state) {
      state.role = null;
    },
  },

  actions: {
    async loginAdmin({ commit }, user) {
      try {
        const response = await axios.post("api/admin_login", user, {
          headers: {
            "Content-Type": "application/json",
          },
        });

        const authToken = response.data.access_token;
        const role = response.data.role;

        axios.defaults.headers.common["Authorization"] = "Bearer " + authToken;

        localStorage.setItem("token", authToken);

        commit("login", role);

        if (role == "admin") {
          router.push({ name: "admin_board" });
        } else {
          localStorage.removeItem("token");
          commit("logout");
          commit("resetRole");
          router.push({ name: "adminlogin" });
        }
      } catch (error) {
        throw error;
      }
    },

    async loginUser({ commit }, user) {
      try {
        const response = await axios.post("api/login", user, {
          headers: {
            "Content-Type": "application/json",
          },
        });

        const authToken = response.data.access_token;
        const role = response.data.role;

        axios.defaults.headers.common["Authorization"] = "Bearer " + authToken;

        localStorage.setItem("token", authToken);
        commit("login", role);

        if (role == "user") {
          router.push({ name: "user_board" });
        } else {
          localStorage.removeItem("token");
          commit("logout");
          commit("resetRole");
          router.push({ name: "login" });
        }
      } catch (error) {
        throw error;
      }
    },

    logoutUser({ commit }) {
      localStorage.removeItem("token");
      commit("logout");
      commit("resetRole");
      router.push({ name: "home" });
    },
  },
});

export default store;
