<template>
  <div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="fw-bold text-dark">Manage Users</h2>
    </div>

    <!-- Stats Row -->
    <div class="row g-4 mb-4">
      <div class="col-md-4">
        <div class="card shadow-sm text-center p-3 bg-light">
          <h5 class="text-primary">Total Users</h5>
          <h3>{{ totalUsers }}</h3>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card shadow-sm text-center p-3 bg-light">
          <h5 class="text-success">Active Users</h5>
          <h3>{{ activeUsers }}</h3>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card shadow-sm text-center p-3 bg-light">
          <h5 class="text-warning">Blocked Users</h5>
          <h3>{{ inactiveUsers }}</h3>
        </div>
      </div>
    </div>

    <!-- Users Table -->
    <div class="card shadow-sm">
      <div class="card-header bg-primary text-white fw-bold">
        User Details
      </div>
      <div class="card-body p-2 table-responsive">
        <table class="table table-sm table-hover align-middle">
          <thead class="table-light">
            <tr>
              <th>ID</th>
              <th>Full Name</th>
              <th>Email</th>
              <th>Qualification</th>
              <th>Last Seen</th>
              <th>Active</th>
              <th>Roles</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.id }}</td>
              <td>{{ user.full_name }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.qualification || '-' }}</td>
              <td>{{ formatDate(user.last_seen) }}</td>
              <td>
                <span :class="user.active ? 'text-success' : 'text-danger'">
                  {{ user.active ? 'Yes' : 'No' }}
                </span>
              </td>
              <td>
                <span v-if="user.roles.length > 0">
                  {{ user.roles.map(r => r.name).join(', ') }}
                </span>
                <span v-else class="text-muted">None</span>
              </td>
              <td>
                <div class="d-flex gap-2">
                    <!-- Toggle Active -->
                    <button
                        class="btn btn-sm"
                        :class="user.active ? 'btn-outline-danger' : 'btn-outline-success'"
                        @click="toggleActive(user)"
                        :title="user.active ? 'Deactivate' : 'Activate'"
                    >
                        <i :class="user.active ? 'fa fa-ban' : 'fa fa-check'"></i>
                    </button>

                    <!-- Delete User -->
                    <button
                        class="btn btn-sm btn-outline-danger"
                        @click="deleteUser(user.id)"
                        title="Delete"
                    >
                        <i class="fa fa-trash"></i>
                    </button>
                </div>

              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/axios';

export default {
  name: 'ManageUsers',
  data() {
    return {
      users: []
    };
  },
  computed: {
    totalUsers() {
      return this.users.length;
    },
    activeUsers() {
      return this.users.filter(u => u.active).length;
    },
    inactiveUsers() {
      return this.users.filter(u => !u.active).length;
    }
  },
  methods: {
    async fetchUsers() {
      try {
        const res = await api.get('/manage-users');
        this.users = res.data;
      } catch (err) {
        console.error('Failed to load users:', err);
        alert('Error loading users');
      }
    },
    formatDate(dateString) {
      if (!dateString) return '-';
      const date = new Date(dateString);
      return date.toLocaleString();
    },
    async toggleActive(user) {
      try {
        await api.put(`/manage-users/${user.id}/toggle-active`);
        this.fetchUsers();
      } catch (err) {
        console.error('Toggle failed:', err);
        alert('Failed to toggle active status');
      }
    },
    async deleteUser(userId) {
      if (!confirm('Are you sure you want to delete this user?')) return;
      try {
        await api.delete(`/manage-users/${userId}`);
        this.fetchUsers();
      } catch (err) {
        alert('Failed to delete user');
      }
    }
  },
  mounted() {
    this.fetchUsers();
  }
};
</script>

<style scoped>
.card-header {
  background-color: #6a1b9a !important;
}
</style>
