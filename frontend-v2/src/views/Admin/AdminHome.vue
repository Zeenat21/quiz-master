<template>
  <div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h2 class="fw-bold text-dark">Welcome Admin!</h2>
      <button class="btn btn-primary" @click="openAddSubjectModal">
        <i class="fa fa-plus"></i> Add Subject
      </button>
    </div>

    <div class="row">
      <div
        v-for="subject in subjects"
        :key="subject.id"
        class="col-md-6 col-xl-4 mb-4"
      >
        <div class="card h-100 shadow rounded-3">
          <div class="card-header bg-primary text-white fw-bold">
            {{ subject.name }}
          </div>
          <div class="card-body p-2">
            <table class="table table-sm table-hover mb-2">
              <thead class="table-light">
                <tr>
                  <th>Chapter</th>
                  <th>Quizzes</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="chapter in subject.chapters" :key="chapter.id">
                  <td>{{ chapter.name }}</td>
                  <td>{{ chapter.quiz_count }}</td>
                  <td>
                    <div class="d-flex flex-wrap">
                      <button class="btn btn-sm btn-warning me-2 mb-1" @click="openEditChapterModal(chapter, subject.id)" title="Edit">
                       <i class="fa fa-pencil"></i>
                      </button>
                      <button class="btn btn-sm btn-danger mb-1" @click="confirmDeleteChapter(chapter.id)" title="Delete">
                        <i class="fa fa-trash"></i>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
            <button class="btn btn-sm btn-outline-success w-100" @click="openAddChapterModal(subject.id)">
              + Add Chapter
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog">
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
                  required
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
    <!-- Modal Backdrop -->
    <div v-if="showModal" class="modal-backdrop fade show"></div>
  </div>
</template>

<script>
import api from '@/axios';

export default {
  data() {
    return {
      subjects: [],
      showModal: false,
      modalTitle: '',
      modalFields: [],
      formData: {},
      currentSubjectId: null,
      editingChapterId: null,
      isSubjectModal: false,
    };
  },
  methods: {
    async fetchSubjects() {
      try {
        const res = await api.get('/subjects/with-details');
        this.subjects = res.data;
      } catch (e) {
        console.error('Error fetching subjects:', e);
      }
    },

    openAddSubjectModal() {
      this.modalTitle = 'Add New Subject';
      this.modalFields = [
        { name: 'name', label: 'Subject Name', type: 'text' },
        { name: 'description', label: 'Description', type: 'textarea' }
      ];
      this.formData = {};
      this.showModal = true;
      this.isSubjectModal = true;
    },

    openAddChapterModal(subjectId) {
      this.modalTitle = 'Add Chapter';
      this.modalFields = [
        { name: 'name', label: 'Chapter Name', type: 'text' },
        { name: 'description', label: 'Description', type: 'textarea' }
      ];
      this.formData = {};
      this.currentSubjectId = subjectId;
      this.editingChapterId = null;
      this.isSubjectModal = false;
      this.showModal = true;
    },

    openEditChapterModal(chapter, subjectId) {
      this.modalTitle = 'Edit Chapter';
      this.modalFields = [
        { name: 'name', label: 'Chapter Name', type: 'text' },
        { name: 'description', label: 'Description', type: 'textarea' }
      ];
      this.formData = { ...chapter };
      this.currentSubjectId = subjectId;
      this.editingChapterId = chapter.id;
      this.isSubjectModal = false;
      this.showModal = true;
    },

    async confirmDeleteChapter(chapterId) {
      if (confirm('Are you sure you want to delete this chapter?')) {
        try {
          await api.delete(`/chapters/${chapterId}`);
          this.fetchSubjects();
        } catch (err) {
          alert('Failed to delete chapter.');
        }
      }
    },

    async handleModalSubmit() {
      try {
        if (this.isSubjectModal) {
          await api.post('/subjects', this.formData);
        } else if (this.editingChapterId) {
          await api.put(`/chapters/${this.editingChapterId}`, this.formData);
        } else {
          await api.post('/chapters', {
            ...this.formData,
            subject_id: this.currentSubjectId
          });
        }
        this.closeModal();
        this.fetchSubjects();
      } catch (err) {
        // alert('Failed to save data.');
         console.error('Save failed:', err.response || err);
        alert(err.response?.data?.msg || 'Failed to save data.'); 

      }
    },

    closeModal() {
      this.showModal = false;
      this.formData = {};
      this.modalTitle = '';
      this.modalFields = [];
      this.editingChapterId = null;
      this.currentSubjectId = null;
    }
  },
  mounted() {
    this.fetchSubjects();
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

/* d-flex.gap-2 > .btn {
  margin-right: 10rem; 
} */

.modal-backdrop {
  z-index: 1040;
}
.modal {
  z-index: 1050;
}
/* 
.table td {
  vertical-align: middle;} */
</style>
