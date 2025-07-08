<template>
  <div class="container-fluid">
    <h2 class="fw-bold text-dark mb-3">Search</h2>

    <!-- Tabs -->
    <ul class="nav nav-tabs mb-3">
      <li class="nav-item" v-for="tab in tabs" :key="tab">
        <a
          class="nav-link"
          :class="{ active: selectedTab === tab }"
          @click="selectedTab = tab"
          href="#"
        >
          {{ tab }}
        </a>
      </li>
    </ul>

    <!-- Search Box -->
    <div class="input-group mb-4">
      <input
        type="text"
        class="form-control"
      
        :placeholder="'Search ' + selectedTab.toLowerCase()"
        v-model="searchQuery"
        @input="debouncedSearch"
      />
    </div>

    <!-- Results -->
    <div v-if="loading" class="text-center text-muted">Searching...</div>

    <div v-else>
      <ul v-if="results.length > 0" class="list-group">
        <li v-for="item in results" :key="item.id" class="list-group-item d-flex justify-content-between">
          <span>
            <strong v-if="selectedTab === 'Users'">{{ item.email }}</strong>
            <strong v-if="selectedTab === 'Subjects'">{{ item.name }}</strong>
            <strong v-if="selectedTab === 'Quizzes'">{{ item.title }}</strong>
          </span>
          <span class="text-muted small">
            ID: {{ item.id }}
          </span>
        </li>
      </ul>
      <div v-else class="text-muted">No {{ selectedTab.toLowerCase() }} found.</div>
    </div>
  </div>
</template>

<script> 
import api from '@/axios';
import debounce from 'lodash/debounce';

export default {
  data() {
    return {
      tabs: ['Users', 'Subjects', 'Quizzes'],
      selectedTab: 'Users',
      searchQuery: '',
      results: [],
      loading: false,
    };
  },

  methods: {
    debouncedSearch: debounce(function () {
      if (!this.searchQuery.trim()) {
        this.results = [];
        return;
      }

      this.loading = true;
      let endpoint = '';

      if (this.selectedTab === 'Users') endpoint = `/search/users?q=${this.searchQuery}`;
      if (this.selectedTab === 'Subjects') endpoint = `/search/subjects?q=${this.searchQuery}`;
      if (this.selectedTab === 'Quizzes') endpoint = `/search/quizzes?q=${this.searchQuery}`;

      api.get(endpoint)
        .then((res) => {
          this.results = res.data;
        })
        .catch(() => {
          this.results = [];
        })
        .finally(() => {
          this.loading = false;
        });
    }, 400),
  },
};

</script>