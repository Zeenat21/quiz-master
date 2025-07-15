<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
export default {
  computed: {
    showNav() {
      const authPages = ['/login', '/register'];
      return !authPages.includes(this.$route.path);
    }
  }
}
</script>

<style>
#app {
  font-family: 'Poppins', 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
   min-height: 100vh;
}


a, a.router-link-exact-active, a:visited, a:hover {
  color: #6a1b9a !important; 
  text-decoration: none;
} 

button, .btn {
  background-color: #6a1b9a !important; /* Violet background */
  border-color: #6a1b9a !important;
  color: white !important;
}

button:hover, .btn:hover{
  background-color: #6a1b9a !important; /* Darker violet on hover */
  border-color: #361f44 !important;
}
</style>
