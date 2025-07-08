<template>
  <div class="d-flex" style="min-height: 100vh;">
    <UserSidebar :collapsed="isSidebarCollapsed" @toggle="toggleSidebar" />
    <div class="flex-grow-1 bg-light">
      <main class="p-4">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script>
import UserSidebar from '@/components/UserSidebar.vue';

export default {
  components: { UserSidebar },
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
