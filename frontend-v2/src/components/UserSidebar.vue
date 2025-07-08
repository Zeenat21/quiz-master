<template>
  <div :class="['sidebar', collapsed ? 'collapsed' : '']">
    <!-- Hamburger toggle icon inside sidebar -->
    <div class="text-left mb-3">
      <button class="btn btn-link text-white" @click="$emit('toggle')">
        <i class="fa fa-bars fa-lg"></i>
      </button>
    </div>
    <nav class="nav flex-column">
      <router-link to="/user" class="nav-link">
        <i class="fa fa-home"></i>
        <span class="link-text"> Home</span>
      </router-link>
      <router-link to="/user/scores" class="nav-link">
        <i class="fa fa-trophy"></i>
        <span class="link-text"> Scores</span>
      </router-link> 
      <router-link to="/user/summary" class="nav-link">
        <i class="fa fa-bar-chart"></i>
        <span class="link-text"> Summary</span>
      </router-link>     
      <router-link to="/user/profile" class="nav-link">
        <i class="fa fa-user"></i>
        <span class="link-text"> Profile</span>
      </router-link>
      <a href="#" @click.prevent="logout" class="nav-link">
        <i class="fa fa-sign-out"></i>
        <span class="link-text"> Logout</span>
      </a>

    </nav>
  </div>
</template>


<script>
import api from '@/axios';

export default{
methods: {
  async logout() {
    const confirmed = confirm('Are you sure you want to logout?');

    if (!confirmed) return;

    try {
      await api.post('/logout'); 
    } catch (error) {
      console.error('Logout failed:', error.response?.data || error.message);
    } finally {
      localStorage.removeItem('access_token');
      this.$router.push('/login'); // I can change this to application home page as well
    }
  }
}

}
</script>

<style scoped>

.sidebar {
  height: 100vh;
  background-color: #6a1b9a;
  padding: 20px 10px;
  transition: width 0.3s ease;
  overflow-x: hidden;
  white-space: nowrap;
  width: 220px;
}

.sidebar.collapsed {
  width: 60px;
}

.sidebar .nav {
  display: flex;
  flex-direction: column;
}

.sidebar .nav-link {
  color: white !important;
  font-size: 16px;
  margin: 10px 0;
  display: flex;
  align-items: center;
  padding: 8px 10px;
  border-radius: 4px;
  transition: background 0.3s ease;
}

.sidebar .nav-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
  text-decoration: none;
}

.sidebar .nav-link i {
  font-size: 18px;
  width: 30px;
  text-align: center;
}

.sidebar.collapsed .link-text {
  display: none;
}

</style>
