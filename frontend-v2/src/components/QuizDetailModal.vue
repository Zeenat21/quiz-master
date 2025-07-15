<template>
  <div>
    <div
      class="modal fade"
      :class="{ show: show }"
      :style="{ display: show ? 'block' : 'none', zIndex: 1050 }"
      tabindex="-1"
    >
      <div class="modal-dialog modal-lg modal-dialog-scrollable">
        <div class="modal-content">
          <form @submit.prevent="handleSave">
            <div class="modal-header">
              <h5 class="modal-title">Edit Quiz Details</h5>
              <button type="button" class="btn-close" @click="$emit('close')" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <div class="mb-3">
                <label class="form-label">Quiz Title</label>
                <input type="text" class="form-control" v-model="localQuiz.title" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Date of Quiz</label>
                <input type="date" class="form-control" v-model="localQuiz.date_of_quiz" />
              </div>
              <div class="mb-3">
                <label class="form-label">Duration (minutes)</label>
                <input type="number" class="form-control" v-model="localQuiz.time_duration" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Remarks</label>
                <textarea class="form-control" rows="3" v-model="localQuiz.remarks"></textarea>
              </div>
            </div>
            <div class="modal-footer d-flex justify-content-between">
              <button type="button" class="btn btn-danger" @click="handleDelete">Delete</button>
              <button type="submit" class="btn btn-success">Save and Close</button>
            </div>
          </form>
        </div>
      </div>
    </div>
    <div
      class="modal-backdrop fade"
      :class="{ show: show }"
      v-show="show"
      :style="{ zIndex: 1040 }"
    ></div>
  </div>
</template>

<script>
export default {
  name: "QuizDetailModal",
  props: {
    show: Boolean,
    quiz: {
      type: Object,
      required: true,
    },
  },
  emits: ["close", "save", "delete"],
  data() {
    return {
      localQuiz: { ...this.quiz },
    };
  },
  watch: {
    quiz: {
      handler(newVal) {
        this.localQuiz = { ...newVal };
        
      },
      deep: true,
    },
  },
  methods: {
    handleSave() {
      this.$emit("save", { ...this.localQuiz });
    },
    handleDelete() {
      if (confirm("Are you sure you want to delete this quiz?")) {
        this.$emit("delete", this.quiz.id);
      }
    },
  },
};
</script>

<style scoped>
.modal-backdrop {
  z-index: 1040;
}
.modal {
  z-index: 1050;
}
.modal-body {
  max-height: calc(100vh - 200px);
  overflow-y: auto;
}
</style>