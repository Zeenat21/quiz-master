<template>
  <div>
    <!-- Modal -->
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
              <h5 class="modal-title">Edit Subject Details</h5>
            </div>
            <div class="modal-body">
              <div class="mb-3">
                <label for="subjectName" class="form-label">Subject Name</label>
                <input
                  id="subjectName"
                  type="text"
                  class="form-control"
                  v-model="localSubject.name"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="subjectDescription" class="form-label">Description</label>
                <textarea
                  id="subjectDescription"
                  class="form-control"
                  rows="3"
                  v-model="localSubject.description"
                  required
                ></textarea>
              </div>
            </div>
            <div class="modal-footer d-flex justify-content-between">
              <button type="button" class="btn btn-danger" @click="handleDelete">
                Delete
              </button>
              <button type="submit" class="btn btn-success">
                Save and Close
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Backdrop -->
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
  name: "SubjectDetailModal",
  props: {
    show: Boolean,
    subject: {
      type: Object,
      required: true,
    },
  },
  emits: ["close", "save", "delete"],
  data() {
    return {
      localSubject: { ...this.subject },
    };
  },
  watch: {
    subject: {
      handler(newVal) {
        this.localSubject = { ...newVal };
      },
      deep: true,
    },
  },
  methods: {
    handleSave() {
      this.$emit("save", { ...this.localSubject });
    },
    handleDelete() {
      if (confirm("Are you sure you want to delete this subject?")) {
        this.$emit("delete", this.subject.id);
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
