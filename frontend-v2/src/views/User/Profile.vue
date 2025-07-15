<template>
  <div class="container py-4">
    <h3 class="fw-bold text-dark mb-4">My Profile</h3>

    <div class="card shadow p-4">
      <form @submit.prevent="updateProfile">
        <div class="row g-3 align-items-center mb-3" v-for="field in fields" :key="field.model">
          <div class="col-md-4 text-md-end fw-bold">
            <label :for="field.model" class="form-label mb-0">
              <i :class="field.icon"></i> {{ field.label }}
            </label>
          </div>

          <div class="col-md-8">
            <input
              v-if="field.type !== 'date'"
              :type="field.type"
              class="form-control"
              :id="field.model"
              v-model="profile[field.model]"
              :placeholder="field.placeholder"
              :required="field.required"
              :disabled="field.readonly"
            />
            <input
              v-else
              type="date"
              class="form-control"
              :id="field.model"
              v-model="profile[field.model]"
            />
          </div>
        </div>

        <div class="text-center mt-4">
          <button type="submit" class="btn btn-primary px-5">
            Update Profile
          </button>
          <div v-if="message" class="alert alert-success mt-3">{{ message }}</div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import api from "@/axios";

export default {
  data() {
    return {
      profile: {
        email: "",
        full_name: "",
        qualification: "",
        dob: "",
        password: "",
      },
      message: "",
      fields: [
        { label: "Email", model: "email", icon: "fa fa-envelope", type: "email", readonly: true },
        { label: "Full Name", model: "full_name", icon: "fa fa-user", type: "text", required: true },
        { label: "Qualification", model: "qualification", icon: "fa fa-graduation-cap", type: "text" },
        { label: "Date of Birth", model: "dob", icon: "fa fa-calendar", type: "date" },
        { label: "New Password", model: "password", icon: "fa fa-key", type: "password", placeholder: "Leave blank to keep unchanged" },
      ],
    };
  },
  methods: {
    async fetchProfile() {
      try {
        const res = await api.get("/user/profile");
        this.profile = { ...this.profile, ...res.data, password: "" };
      } catch (err) {
        console.error("Failed to load profile:", err);
      }
    },
    async updateProfile() {
      try {
        const updateData = { ...this.profile };
        if (!updateData.password) delete updateData.password;

        await api.put("/user/profile", updateData);
        this.message = "Profile updated successfully!";
        setTimeout(() => (this.message = ""), 3000);
      } catch (err) {
        console.error("Failed to update profile:", err);
      }
    },
  },
  mounted() {
    this.fetchProfile();
  },
};
</script>

<style scoped>
.card {
  max-width: 800px;
  margin: auto;
}

.form-label {
  white-space: nowrap;
}

input:focus {
  border-color: #6a1b9a;
  box-shadow: 0 0 0 0.2rem rgba(106, 27, 154, 0.25);
}
</style>
