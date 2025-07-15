<template>
  <div class="d-flex justify-content-center align-items-center min-vh-100 bg-light">
    <div class="card p-4 shadow rounded-4" style="max-width: 380px; width: 100%;">
      <h4 class="text-center text-dark fw-bold">Welcome back</h4>
      <p></p>
      <form @submit.prevent="loginUser">
        <div class="mb-3">
          <!-- <label for="email" class="form-label text-muted">Email</label> -->
          <input
            id="email"
            v-model="email"
            type="email"
            class="form-control"
            placeholder="Email"
            required
          />
        </div>
        <div class="mb-3">
          <!-- <label for="password" class="form-label text-muted">Password</label> -->
          <input
            id="password"
            v-model="password"
            type="password"
            class="form-control"
            placeholder="Password"
            required
          />
        </div>
        <button type="submit" class="btn w-100 text-white">
          Login
        </button>
        <p v-if="error" class="text-danger mt-3 text-center">{{ error }}</p>
        <p class="mt-3 text-center text-muted">
          Not a student yet?
          <router-link to="/register" class="text-decoration-underline">
            Register
          </router-link>
        </p>

      </form>
    </div>
  </div>
</template>


<script>
import api from '@/axios';
export default {
  data() {
    return {
      email: '',
      password: '',
      error: ''
    }
  },
  methods: {
    async loginUser() {
      this.error = ''
      try {
        const response = await api.post('/login', {
          email: this.email,
          password: this.password
        })
        const { access_token, roles, full_name } = response.data
        localStorage.setItem('user_roles', JSON.stringify(roles))
        localStorage.setItem('access_token', access_token)
        localStorage.setItem('full_name', full_name)
        
        if (roles.includes('admin')) {
            this.$router.push('/admin');
        } else {
            this.$router.push('/user');}

            
        // localStorage.setItem('access_token', response.data.access_token)
        // this.$router.push('/admin') // or dashboard route
      } catch (err) {
        this.error = err.response?.data?.error || 'Login failed'
      }
    }
  }
}
</script>
