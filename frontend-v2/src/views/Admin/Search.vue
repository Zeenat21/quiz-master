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
        <li v-for="item in results" :key="item.id" class="list-group-item d-flex justify-content-between"
       @click="handleItemClick(item, $event)"
        style="cursor: pointer;"
        >
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

    <QuizDetailModal
    v-show="selectedQuiz !== null"
    :show="showQuizModal"
    :quiz="selectedQuiz"
    @save="handleQuizSave"
    @delete="handleQuizDelete"
    @close="showQuizModal = false"
    />

    <SubjectDetailModal
    v-show="selectedSubject !== null"
    :show="showSubjectModal"
    :subject="selectedSubject"
    @save="handleSubjectSave"
    @delete="handleSubjectDelete"
    @close="showSubjectModal = false"
    />


  </div>
</template>

<script> 
import api from '@/axios';
import debounce from 'lodash/debounce';

import QuizDetailModal from "@/components/QuizDetailModal.vue";
import SubjectDetailModal from "@/components/SubjectDetailModal.vue";

export default {
  components: {QuizDetailModal, SubjectDetailModal},
  data() {
    return {
      tabs: ['Users', 'Subjects', 'Quizzes'],
      selectedTab: 'Users',
      searchQuery: '',
      results: [],
      loading: false,

      showQuizModal: false,
      selectedQuiz: null,

      showSubjectModal: false,
      selectedSubject: null,
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


  handleItemClick(item, event) {
  if (['BUTTON', 'INPUT', 'TEXTAREA'].includes(event.target.tagName)) return;

  if (this.selectedTab === "Subjects") {
    this.selectedSubject = { ...item };
    this.showSubjectModal = true;
  } else if (this.selectedTab === "Quizzes") {
    this.selectedQuiz = { ...item };
    this.showQuizModal = true;
  }
},

  handleQuizDelete(quizId) {
    if (confirm("Are you sure you want to delete this quiz?")) {
      api.delete(`/quizzes/${quizId}`)
        .then(() => {
          this.debouncedSearch();
          this.showQuizModal = false;
        })
        .catch(err => alert(err.response?.data?.msg || "Failed to delete quiz."));
    }
  },

  handleSubjectDelete(subjectId) {
    if (confirm("Are you sure you want to delete this subject?")) {
      api.delete(`/subjects/${subjectId}`)
        .then(() => {
          this.debouncedSearch();
          this.showSubjectModal = false;
        })
        .catch(err => alert(err.response?.data?.msg || "Failed to delete subject."));
    }
  },

    handleQuizSave(updatedQuiz) {
      if (updatedQuiz.date_of_quiz) {
        updatedQuiz.date_of_quiz = updatedQuiz.date_of_quiz.split("T")[0];
      }

      api.put(`/quizzes/${updatedQuiz.id}`, updatedQuiz)
        .then(() => {
          this.debouncedSearch();
          this.showQuizModal = false;
        })
        .catch(err => alert(err.response?.data?.msg || "Failed to update quiz."));
    },


    handleSubjectSave(updatedSubject) {
      api.put(`/subjects/${updatedSubject.id}`, updatedSubject)
        .then(() => this.debouncedSearch())
        .catch(err => alert(err.response?.data?.msg || "Failed to update subject."));
      this.showSubjectModal = false;
    },


  

  },
};

</script>