<template>
  <div class="modal fade" tabindex="-1" :class="{ show: show }" style="display: block;" v-if="show">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ title }}</h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="handleSubmit">
            <div v-for="(field, index) in fields" :key="index" class="mb-3 text-left">
              <label :for="field.name" class="form-label">{{ field.label }}</label>
              <component
                :is="field.type === 'textarea' ? 'textarea' : 'input'"
                :type="field.type !== 'textarea' ? field.type : undefined"
                class="form-control"
                :id="field.name"
                v-model="formData[field.name]"
                :placeholder="field.placeholder || field.label"
                :required="field.required !== false"
              ></component>
            </div>
            <div class="text-end">
              <button type="button" class="btn btn-secondary me-2" @click="$emit('close')">Cancel</button>
              <!-- <p></p> -->
              <button type="submit" class="btn btn-success">Create</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AddEntityModal',
  props: {
    title: { type: String, required: true },
    show: { type: Boolean, required: true },
    endpoint: { type: String, required: true },
    fields: { type: Array, required: true },
    initialData: { type: Object, default: () => ({})
  },
  data() {
    return {
      formData: {},
    };
  },
  watch: {
    show(val) {
      if (val) {
        this.initializeForm();
      }
    },
  },
  methods: {
      initializeForm() {
    this.formData = { ...this.initialData };
    this.fields.forEach(field => {
      if (!(field.name in this.formData)) {
        this.formData[field.name] = '';
      }
    });
  },

    async handleSubmit() {
      // try {
        this.$emit('save', this.formData);
        this.$emit('close');
        // const token = localStorage.getItem('token');
        // const response = await axios.post(this.endpoint, this.formData, {
        //   headers: {
        //     Authorization: `Bearer ${token}`,
        //   },
        // });
        // this.$emit('success', response.data);
        // this.$emit('close');
      // } catch (err) {
      //   alert(err.response?.data?.msg || 'Failed to submit form');
      }
    },
  },
};

</script>

<style scoped>
.modal.fade {
  background-color: rgba(0, 0, 0, 0.5);
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 1050;
  overflow: auto;
}
</style>
