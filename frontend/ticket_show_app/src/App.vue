<script setup>
import Navbar from './components/Navbar.vue'
</script>



<template>
  <div>
    <Navbar/>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
};
</script>


<style>

</style>
