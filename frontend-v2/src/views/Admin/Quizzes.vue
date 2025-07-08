<template>
  <div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h2 class="fw-bold text-dark">Manage Quizzes</h2>
      <button class="btn btn-primary" @click="openAddQuizModal">
        <i class="fa fa-plus"></i> Add Quiz
      </button>
    </div>

    <div class="row">
      <div
        v-for="quiz in quizzes"
        :key="quiz.id"
        class="col-md-6 col-xl-4 mb-4"
      >
        <div class="card h-100 shadow rounded-3">
          <div class="card-header bg-info text-white fw-bold">
            {{ quiz.title }}
          </div>
          <div class="card-body p-2">
            <table class="table table-sm table-hover mb-2">
              <thead class="table-light">
                <tr>
                  <th>ID</th>
                  <th>Question</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="q in quiz.questions" :key="q.id">
                  <td>{{ q.id }}</td>
                  <td>{{ q.question_statement }}</td>
                  <td>
                    <div class="d-flex flex-wrap">
                      <button class="btn btn-sm btn-warning me-2 mb-1" @click="openEditQuestionModal(q, quiz.id)" title="Edit">
                        <i class="fa fa-pencil"></i>
                      </button>
                      <button class="btn btn-sm btn-danger mb-1" @click="confirmDeleteQuestion(q.id)" title="Delete">
                        <i class="fa fa-trash"></i>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
            <button class="btn btn-sm btn-outline-success w-100" @click="openAddQuestionModal(quiz.id)">
              + Add Question
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <form @submit.prevent="handleModalSubmit">
            <div class="modal-header">
              <h5 class="modal-title">{{ modalTitle }}</h5>
              <button type="button" class="btn-close" @click="closeModal"></button>
            </div>
            <div class="modal-body">
              <div v-for="field in modalFields" :key="field.name" class="mb-3">
                <label :for="field.name" class="form-label">{{ field.label }}</label>
                <component
                  :is="field.type === 'textarea' ? 'textarea' : 'input'"
                  class="form-control"
                  v-model="formData[field.name]"
                  :type="field.type === 'textarea' ? undefined : field.type"
                  :id="field.name"
                  :required="field.required !== false"
                ></component>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
              <button type="submit" class="btn btn-success">Save</button>
            </div>
          </form>
        </div>
      </div>
    </div>
    <div v-if="showModal" class="modal-backdrop fade show"></div>
  </div>
</template>

<script>
import api from '@/axios';

export default {
  data() {
    return {
      quizzes: [],
      showModal: false,
      modalTitle: '',
      modalFields: [],
      formData: {},
      currentQuizId: null,
      editingQuestionId: null,
      isQuizModal: false,
    };
  },
  methods: {
    async fetchQuizzes() {
      try {
        const res = await api.get('/quizzes/with-details');
        this.quizzes = res.data;
      } catch (e) {
        console.error('Error fetching quizzes:', e);
      }
    },

    openAddQuizModal() {
      this.modalTitle = 'Add New Quiz';
      this.modalFields = [
        { name: 'title', label: 'Quiz Title', type: 'text' },
        { name: 'chapter_id', label: 'Chapter ID', type: 'number' },
        { name: 'date_of_quiz', label: 'Date (YYYY-MM-DD)', type: 'text' },
        { name: 'time_duration', label: 'Time Duration (in minutes)', type: 'number' },
        { name: 'remarks', label: 'Remarks', type: 'textarea', required: false }
      ];
      this.formData = {};
      this.isQuizModal = true;
      this.showModal = true;
    },

    openAddQuestionModal(quizId) {
      this.modalTitle = 'Add Question';
      this.modalFields = [
        { name: 'question_statement', label: 'Question Text', type: 'textarea' },
        { name: 'option1', label: 'Option 1', type: 'text' },
        { name: 'option2', label: 'Option 2', type: 'text' },
        { name: 'option3', label: 'Option 3', type: 'text' },
        { name: 'option4', label: 'Option 4', type: 'text' },
        { name: 'correct_option', label: 'Correct Option (1-4)', type: 'number' }
      ];
      this.formData = {};
      this.currentQuizId = quizId;
      this.editingQuestionId = null;
      this.isQuizModal = false;
      this.showModal = true;
    },

    openEditQuestionModal(question, quizId) {
      this.modalTitle = 'Edit Question';
      this.modalFields = [
        { name: 'question_statement', label: 'Question Text', type: 'textarea' },
        { name: 'option1', label: 'Option 1', type: 'text' },
        { name: 'option2', label: 'Option 2', type: 'text' },
        { name: 'option3', label: 'Option 3', type: 'text' },
        { name: 'option4', label: 'Option 4', type: 'text' },
        { name: 'correct_option', label: 'Correct Option (1-4)', type: 'number' }
      ];
      this.formData = { ...question };
      this.editingQuestionId = question.id;
      this.currentQuizId = quizId;
      this.isQuizModal = false;
      this.showModal = true;
    },

    async confirmDeleteQuestion(id) {
      if (confirm('Are you sure you want to delete the question?')) {
        try {
          await api.delete(`/questions/${id}`);
          this.fetchQuizzes();
        } catch (err) {
          alert('Failed to delete question.');
        }
      }
    },

    async handleModalSubmit() {
      try {
        if (this.isQuizModal) {
          await api.post('/quizzes', this.formData);
        } else if (this.editingQuestionId) {
          await api.put(`/questions/${this.editingQuestionId}`, this.formData);
        } else {
          await api.post('/questions', {
            ...this.formData,
            quiz_id: this.currentQuizId
          });
        }

        this.closeModal();
        this.fetchQuizzes();
      } catch (err) {
        console.error(err.response || err);
        alert(err.response?.data?.msg || 'Save failed');
      }
    },

    closeModal() {
      this.showModal = false;
      this.formData = {};
      this.modalFields = [];
      this.modalTitle = '';
      this.currentQuizId = null;
      this.editingQuestionId = null;
    }
  },
  mounted() {
    this.fetchQuizzes();
  }
};
</script>

<style scoped>
.card-header {
  background-color: #6a1b9a !important;
}
.card-body {
  overflow-x: auto;
}
.d-flex > .btn {
  margin-right: 8px;
}
.modal-backdrop {
  z-index: 1040;
}
.modal {
  z-index: 1050;
}
</style>
