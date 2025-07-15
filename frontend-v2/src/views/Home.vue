<!-- <template>
  <div class="home-container d-flex flex-column min-vh-100">

    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
      <div class="container-fluid">
        <router-link class="navbar-brand fw-bold text-violet" to="/">Quiz Master</router-link>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link class="nav-link text-violet fw-medium" to="/login">Login</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link text-violet fw-medium" to="/register">Register</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link text-violet fw-medium" to="/about">About</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="flex-grow-1 d-flex justify-content-center align-items-center text-center">
      <div class="content p-3">
        <h1 class="display-4 fw-bold text-violet">Welcome to Quiz Master!</h1>
        <p class="lead text-dark">Sharpen your skills. Compete. Learn.</p>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  mounted() {
    const token = localStorage.getItem("access_token");
    const role = localStorage.getItem("user_role");

    if (token) {
      if (role === "admin") {
        this.$router.push("/admin");
      } else {
        this.$router.push("/user");
      }
    }
  }
};
</script>

<style scoped>
.home-container {
  background: url("@/assets/quiz-background.jpg") no-repeat center center;
  background-size: cover;
}

/* Custom violet for navbar links and brand */
.text-violet {
  color: #6a1b9a !important;
}

/* Ensure navbar stays visible on light backgrounds */
.navbar {
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.nav-link:hover {
  color: #361f44 !important;
}
</style> -->

<template>
  <div class="content p-3">
    <h1 class="display-4 fw-bold text-violet">Welcome to Quiz Master!</h1>
    <p class="lead text-bold">Sharpen your skills. Compete. Learn.</p>
  </div>
</template>

<script>
export default {};
</script>

<style scoped>

.text-violet {
  color: #6a1b9a !important;
}
</style>
