<template>
    <div class="login-container">
        <div class="box">
            <h1 class="main-tag brand-font bigger-font">Register</h1>
            <div class="input-group">
                <input type="text" class="form-control input-field" placeholder="Username" required
                    v-model="signUpData.username" />
                <input type="email" class="form-control input-field" placeholder="Email" required
                    v-model="signUpData.email" />
                <input type="password" class="form-control input-field" placeholder="Password" required
                    v-model="signUpData.password" />

                <button @click="SignUp" class="btn text-white c2 login-button">Sign me up</button>
                <p class="register-link">Already have an account? <a @click="entrylogin" class="link-text">Login</a></p>
            </div>
        </div>

        <error-popup :error-message="errorPopupMessage" @close="closeErrorPopup"></error-popup>
    </div>
</template>
  
<script>
import { mapActions } from 'vuex';
import ErrorPopup from '../components/ErrorPopUp.vue'; 
import axios from "../axios.js";

export default {
    name: 'Register',

    components: {
        'error-popup': ErrorPopup
    },

    data() {
        return {
            signUpData: {
                username: null,
                email: null,
                password: null
            },
            errorPopupMessage: ''
        };
    },

    methods: {
        entrylogin() {
            this.$router.push({ name: 'login' });
        },

        async SignUp() {
            try {
                console.log("hihi")
                const res = await axios.post("api/user", this.signUpData, {
                    headers: {
                        "Content-Type": "application/json",
                    },
                });

                alert('User Created');

                await this.loginUser({
                    email: this.signUpData.email,
                    password: this.signUpData.password
                });

            } catch (error) {
                const errorMessage = error.response?.data?.error_message || 'Registration failed. Please try again.';
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
    height: 420px;
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
    border-radius: 4px;
    font-size: 14px;
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
  