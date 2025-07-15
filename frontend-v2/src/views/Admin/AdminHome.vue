<template>
  <div class="container-fluid mt-3">
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
        <div class="card h-100 shadow rounded-3" style="height: 350px;">
          <div class="card-header bg-primary text-white fw-bold"
          style="cursor: pointer;"
          @click="openSubjectDetailModal(subject)"
          title="Click to view/edit subject"
          >
            {{ subject.name }}
          </div>

          <div class="card-body p-2 d-flex flex-column">
            <div class="chapter-table-wrapper flex-grow-1">
            <!-- <div class="flex-grow-1 overflow-auto"> -->
              <table class="table table-sm table-hover mb-0">
                <thead class="table-light sticky-top bg-white">
                  <tr>
                    <th>Chapter</th>
                    <th>Quizzes</th>
                    <th class="text-center">Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="chapter in subject.chapters" :key="chapter.id">
                    <td>{{ chapter.name }}</td>
                    <td>{{ chapter.quiz_count }}</td>
                    <td class="text-center align-middle">
                      <div class="d-flex justify-content-center align-items-center">
                        <button class="btn btn-sm btn-warning me-2" @click="openEditChapterModal(chapter, subject.id)" title="Edit">
                          <i class="fa fa-pencil"></i>
                        </button>
                        <button class="btn btn-sm btn-danger" @click="confirmDeleteChapter(chapter.id)" title="Delete">
                          <i class="fa fa-trash"></i>
                        </button>
                      </div>


                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div class="pt-2 mt-auto">
              <button class="btn btn-sm btn-outline-success w-100" @click="openAddChapterModal(subject.id)" title="Add Chapter">
                + Add Chapter
              </button>
            </div>
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
                  :value="formData[field.name]"
                  @input="formData[field.name] = $event.target.value"
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

    <div v-if="showModal" class="modal-backdrop fade show"></div>
  </div>


   <!-- Subject detailed view  -->
    <SubjectDetailModal
      :show="showSubjectModal"
      :subject="selectedSubject"
      @close="showSubjectModal = false"
      @save="updateSubject"
      @delete="deleteSubject"
    />
</template>





<script>
import api from '@/axios';
import SubjectDetailModal from "@/components/SubjectDetailModal.vue";

export default {
  components: { SubjectDetailModal },
  data() {
    return {
      // subjects: [],
      showSubjectModal: false,
      selectedSubject: {
        id: null,
        name: "",
        description: "",
      },

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
      // this.formData = {};
      this.formData = {
        name: '',
        description: ''
      };
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
    },

      openSubjectDetailModal(subject) {
      this.selectedSubject = { ...subject };
      this.showSubjectModal = true;
    },

    async updateSubject(updatedSubject) {
      try {
        await api.put(`/subjects/${updatedSubject.id}`, updatedSubject);
        this.showSubjectModal = false;
        this.fetchSubjects();
      } catch (err) {
        console.error(err);
        alert(err.response?.data?.msg || "Failed to update subject.");
      }
    },

    async deleteSubject(subjectId) {
      try {
        await api.delete(`/subjects/${subjectId}`);
        this.showSubjectModal = false;
        this.fetchSubjects();
      } catch (err) {
        console.error(err);
        alert(err.response?.data?.msg || "Failed to delete subject.");
      }
    },
  





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

.card-header:hover {
  background-color: #7b1fa2 !important; /* slightly lighter violet */
}

.modal-backdrop {
  z-index: 1040;
}
.modal {
  z-index: 1050;
}

.d-flex > .btn {
  margin-right: 2px;
}
.chapter-table-wrapper {
  max-height: 180px; 
  overflow-y: auto;
}
</style>
