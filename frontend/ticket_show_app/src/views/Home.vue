<template>
    <div class="main-box">
        <h1 class="main">Welcome to Ticket Show</h1>
        <p class="subtext">Explore and manage your tickets with ease</p>
        <button @click="entrylogin" class="btn text-white c2">User Login</button>
        <button @click="entryadminlogin" class="btn text-white c2">Admin Login</button>
    </div>
</template>

<script>
export default {
    methods: {
        entrylogin() {
            this.$router.push({ name: 'login' })
        },
        entryadminlogin() {
            this.$router.push({ name: 'adminlogin' })
        }
    },
}
</script>

<style scoped>
.main-box {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
    font-family: "Montserrat";
    background-color: #e3e9f8;
}

.main {
    font-size: 2.625rem;
    font-weight: bold;
    margin-bottom: 10px;
}

.subtext {
    font-size: 1.2rem;
    color: #777;
    text-align: center;
    margin-bottom: 20px;
}

.btn {
    display: block;
    width: 80%;
    max-width: 300px;
    padding: 12px;
    margin: 10px auto;
    font-size: 1rem;
    /* font-weight: bold; */
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s, color 0.3s;
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
