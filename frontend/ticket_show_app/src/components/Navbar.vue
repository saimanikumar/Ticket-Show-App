<template>
  <div>
    <nav class="navbar fixed-top navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <a class="navbar-brand brand-font" href="#">&nbsp;Ticket Show</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav ms-auto mb-2 mb-lg-0 ">

            <li class="nav-item">
              <a @click="nav_home" class="nav-link nav21"><i class="bi bi-house"></i> Home</a>
            </li>

            <li class="nav-item" v-show="!$store.state.loggedIn">
              <a @click="entrylogin" class="nav-link nav21"><i class="bi bi-box-arrow-in-right"></i> Login</a>
            </li>

            <li class="nav-item" v-show="!$store.state.loggedIn">
              <a @click="entryregister" class="nav-link nav21"><i class="bi bi-person-plus"></i> Register</a>
            </li>

            <li class="nav-item" v-show="$store.state.loggedIn && $store.state.role === 'admin'">
              <a @click="nav_summary" class="nav-link nav21"><i class="bi bi-bar-chart-line"></i> Summary</a>
            </li>

            <li class="nav-item" v-show="$store.state.loggedIn && $store.state.role === 'user'">
              <a @click="nav_bookings" class="nav-link nav21"><i class="bi bi-calendar-check"></i> Bookings</a>
            </li>

            <li class="nav-item" v-show="$store.state.loggedIn">
              <a @click="nav_logout" class="nav-link nav21"><i class="bi bi-box-arrow-left"></i> Log Out</a>
            </li>

            <li>
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            </li>


          </ul>

        </div>
      </div>
    </nav>
  </div>
</template>
  


<script>
export default {
  created() {

  },
  methods: {

    nav_home() {
      if (localStorage.getItem('token')) {
        if (this.$store.state.role == 'admin') {
          this.$router.push({ name: 'admin_board' })
        } else {
          this.$router.push({ name: 'user_board' })
        }
      }
      else {
        this.$router.push({ name: 'home' })
      }

    },
    entrylogin() {
      this.$router.push({ name: 'login' })
    },
    entryregister() {
      this.$router.push({ name: 'register' })
    },
    nav_summary() {
      this.$router.push({ name: 'summary' })
    },
    nav_bookings() {
      this.$router.push({ name: 'bookings' })
    },
    nav_logout() {
      this.$store.dispatch('logoutUser')
    },

  },
}
</script>


<style scoped>
</style>