<template>
  <div class="d-flex justify-content-center align-items-center min-vh-100 bg-light">
    <div class="card p-4 shadow rounded-4" style="max-width: 450px; width: 100%;">
      <h3 class="text-center text-dark mb-3">Register</h3>
      <form @submit.prevent="registerUser">
        <div class="mb-3" style="text-align: left;">
         <label for="email" class="form-label">Email:</label>
          <input
            v-model="email"
            type="email"
            class="form-control"
         
            required
          />
        </div>
        <div class="mb-3" style="text-align: left;">
          <label for="password" class="form-label">Password:</label>
          <input
            v-model="password"
            type="password"
            class="form-control"
           
            required
          />
        </div>
        <div class="mb-3" style="text-align: left;">
          <label for="fullName" class="form-label">Full Name:</label>
          <input
            v-model="full_name"
            type="text"
            class="form-control"
           
            required
          />
        </div>
        <div class="mb-3" style="text-align: left;">
          <label for="qualification" class="form-label">Qualification:</label>
          <input
            v-model="qualification"
            type="text"
            class="form-control"
            
          />
        </div>
        <div class="form-floating mb-3" style="text-align: left;">
          <label for="dob" class="form-label">Date of Birth:</label>
          <input
            v-model="dob"
            type="date"
            id="dob"
            class="form-control"
            placeholder="Date of Birth"
          />
        </div>
        <button type="submit" class="btn btn-primary w-100 text-white">
          Register
        </button>
        <p v-if="error" class="text-danger mt-3 text-center">{{ error }}</p>
        <p v-if="success" class="text-success mt-3 text-center">{{ success }}</p>
        <p class="mt-3 text-center text-muted">
          Already have an account?
          <router-link to="/login" class="text-decoration-underline">
            Login
          </router-link>
        </p>
      </form>
    </div>
  </div>
</template>


<script>
import axios from 'axios'
export default {
  data() {
    return {
      email: '',
      password: '',
      full_name: '',
      qualification: '',
      dob: '',
      error: '',
      success: ''
    }
  },
  methods: {
    async registerUser() {
      this.error = ''
      this.success = ''
      try {
        const response = await axios.post('http://localhost:5000/api/register', {
          email: this.email,
          password: this.password,
          full_name: this.full_name,
          qualification: this.qualification,
          dob: this.dob
        })
        this.success = response.data.message
        setTimeout(() => {
        this.$router.push('/login');
      }, 2000); 

      } catch (err) {
        this.error = err.response?.data?.error || 'Registration failed'
      }
    }
  }
}
</script>
