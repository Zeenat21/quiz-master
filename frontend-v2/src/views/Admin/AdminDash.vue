<template>
  <div class="d-flex" style="min-height: 100vh;">
    <AdminSidebar :collapsed="isSidebarCollapsed" @toggle="toggleSidebar" />
    <div class="flex-grow-1 bg-light">
      <main class="p-4">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script>
import AdminSidebar from '@/components/AdminSidebar.vue';

export default {
  components: { AdminSidebar },
  data() {
    return {
      isSidebarCollapsed: false,
    };
  },
  methods: {
    toggleSidebar() {
      this.isSidebarCollapsed = !this.isSidebarCollapsed;
    },
  },
};
</script>
