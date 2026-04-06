<template>
  <div v-if="open" class="modal-backdrop" @click.self="$emit('close')">
    <div class="modal-panel card">
      <div class="modal-panel__header">
        <div>
          <p v-if="eyebrow" class="eyebrow">{{ eyebrow }}</p>
          <h3>{{ title }}</h3>
        </div>
        <button class="ghost-button" @click="$emit('close')">Cerrar</button>
      </div>
      <slot />
    </div>
  </div>
</template>

<script setup>
/* global defineProps, defineEmits */
defineProps({
  open: {
    type: Boolean,
    default: false,
  },
  title: {
    type: String,
    required: true,
  },
  eyebrow: {
    type: String,
    default: "",
  },
});

defineEmits(["close"]);
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.54);
  display: grid;
  place-items: center;
  padding: 16px;
  z-index: 40;
}

.modal-panel {
  width: min(680px, 100%);
}

.modal-panel__header {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: flex-start;
  margin-bottom: 18px;
}
</style>
