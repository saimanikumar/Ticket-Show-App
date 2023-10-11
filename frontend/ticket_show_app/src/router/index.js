import { createRouter, createWebHistory } from 'vue-router'
import Login from "../views/Login.vue"
import Signup from "../views/Register.vue"
import Home from "../views/Home.vue"
import Board from "../views/Board.vue"
import AdminLogin from "../views/AdminLogin.vue"
import AdminBoard from "../views/AdminBoard.vue"
import TheatreForm from "../views/TheatreForm.vue"
import ShowForm from "../views/ShowForm.vue"
import Summary from "../views/Summary.vue"
import BookingForm from "../views/BookingForm.vue"
import Bookings from "../views/Bookings.vue"

import store from "../store";

function check_route_admin(to, from, next) {
  var isAuthenticated = false

  if (store.state.loggedIn)
      isAuthenticated = true
  else
      isAuthenticated = false
  
  if (isAuthenticated && store.state.role == 'admin') {
      next()
  }
  else {
      next('/adminlogin')
  }
}

function check_route_user(to, from, next) {
  var isAuthenticated = false

  if (store.state.loggedIn)
      isAuthenticated = true
  else
      isAuthenticated = false
  
  if (isAuthenticated && store.state.role == 'user') {
      next()
  }
  else {
      next('/login')
  }
}

function clearToken(to, from, next) {
  localStorage.removeItem('token');
  next();
}
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    { path: '/login', name: 'login', component: Login },
    { path: '/adminlogin', name: 'adminlogin', component: AdminLogin },

    { path: '/register', name: 'register', component: Signup },

    { path: '/', name: 'home', component: Home },
    
    { path: '/adminboard', name: 'admin_board', component: AdminBoard, beforeEnter: check_route_admin},
    { path: '/summary', name: 'summary', component: Summary, beforeEnter: check_route_admin},

    { path: '/theatre/create', name: 'create_theatre', component: TheatreForm, beforeEnter: check_route_admin},
    { path: '/theatre/update/:id', name: 'update_theatre', component: TheatreForm, beforeEnter: check_route_admin },
    
    { path: '/show/create/:th_id', name: 'create_show', component: ShowForm, beforeEnter: check_route_admin },
    { path: '/show/update/:th_id/:s_id', name: 'update_show', component: ShowForm, beforeEnter: check_route_admin },

    
    { path: '/board', name: 'user_board', component: Board, beforeEnter: check_route_user},
    { path: '/board/book/:th_id/:s_id', name: 'user_booking', component: BookingForm, beforeEnter: check_route_user},

    { path: '/board/bookings', name: 'bookings', component: Bookings, beforeEnter: check_route_user},


    
  ]
})

export default router
