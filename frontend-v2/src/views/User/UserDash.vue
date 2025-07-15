<template>
  <div class="d-flex vh-100 overflow-hidden">
    <UserSidebar :collapsed="isSidebarCollapsed" @toggle="toggleSidebar" />
    <div class="flex-grow-1 bg-light overflow-auto">
      <main class="p-4" style="min-height: 100%; overflow-y: auto; overflow-x: auto;">
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
