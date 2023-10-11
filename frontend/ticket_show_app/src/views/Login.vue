<template>
  <div class="login-container">
    <div class="box">
      <h1 class="main-tag brand-font bigger-font">Login</h1>
      <div class="input-group">
        <input type="email" class="form-control input-field" placeholder="Email" required v-model="userInfo.email" />
        <input type="password" class="form-control input-field" placeholder="Password" required
          v-model="userInfo.password" />
        <button @click="login_user(userInfo)" class="btn text-white login-button c2">Let me in</button>
        <p class="register-link">Don't have an account? <a @click="entryregister" class="link-text">Register</a></p>
      </div>
    </div>

    <error-popup :error-message="errorPopupMessage" @close="closeErrorPopup"></error-popup>
  </div>
</template>

<script>
import { mapActions } from 'vuex';
import ErrorPopup from '../components/ErrorPopUp.vue'; 

export default {
  name: 'Login',

  components: {
    'error-popup': ErrorPopup
  },

  data() {
    return {
      userInfo: {
        email: null,
        password: null
      },
      errorPopupMessage: ''
    };
  },

  methods: {
    entryregister() {
      this.$router.push({ name: 'register' });
    },

    async login_user(userInfo) {
      try {
        var x = await this.loginUser(userInfo);
      } catch (error) {
        console.log("hi")
        console.log(error)
        const errorMessage = error.response?.data?.error_message || 'Login failed. Please check your credentials.';
        this.showErrorPopup(errorMessage);
      }
    },

    showErrorPopup(message) {
      this.errorPopupMessage = message;
    },

    closeErrorPopup() {
      this.errorPopupMessage = '';
    },

    ...mapActions(['loginUser'])
  }
};
</script>


<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #e3e9f8;
}

.box {
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  padding: 40px;
  width: 400px;
  height: 380px;
  text-align: center;
}

.main-tag {
  margin: 0;
  padding: 10px 0;
  font-size: 36px;
  color: #333333;
}

.bigger-font {
  font-size: 40px;
}

.input-group {
  margin-top: 20px;
  text-align: left;
}

.input-field {
  width: 100%;
  padding: 12px;
  font-size: 14px;
  /* border-radius: 5px; */
}

.login-button {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  margin-top: 10px;
}

.register-link {
  font-size: 14px;
  color: #666666;
}

.link-text {
  color: #007bff;
  text-decoration: none;
  cursor: pointer;
}

.login-button {
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.c2 {
  background-color: #44afe9;

}

.btn.c2:hover {
  background-color: #1aa5f0;
}

.btn.c2:active {
  background-color: #2faaec;
}
</style>