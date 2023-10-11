<template>
  <div v-if="errorMessage" class="error-popup">
    <span>{{ errorMessage }} </span>
    <button @click="closeError" class="close-button">  &times;</button>
  </div>
</template>

<script>
export default {
  props: {
    errorMessage: String
  },
  methods: {
    closeError() {
      this.$emit('close');
    },
    scheduleClose() {
      this.clearTimeout(); 
      this.timeout = setTimeout(() => {
        this.closeError();
      }, 5000); 
    },
    clearTimeout() {
      if (this.timeout) {
        clearTimeout(this.timeout);
        this.timeout = null;
      }
    }
  },
  data() {
    return {
      timeout: null
    };
  },
  watch: {
    errorMessage: {
      immediate: true, 
      handler() {
        this.scheduleClose();
      }
    }
  },
  beforeDestroy() {
    this.clearTimeout();
  }
};
</script>

<style scoped>
.error-popup {
  position: fixed;
  top: 80px;
  right: 20px;
  background-color: #f44336;
  color: white;
  padding: 10px 20px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.close-button {
  background-color: transparent;
  border: none;
  color: white;
  font-size: 16px;
  cursor: pointer;
}
</style>
