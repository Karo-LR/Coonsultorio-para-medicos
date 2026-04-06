<template>
  <section class="grid">
    <PageHeader
      eyebrow="Historial"
      title="Expedientes"
      description="Historial clínico por paciente con alergias y enfermedades crónicas."
    >
      <template #actions>
        <button class="primary-button" @click="openCreate">Nuevo expediente</button>
      </template>
    </PageHeader>

    <div v-if="error" class="error-state">{{ error }}</div>

    <article class="card">
      <div v-if="loading" class="loading-state">Cargando expedientes...</div>
      <div v-else-if="records.length === 0" class="empty-state">Sin expedientes registrados.</div>
      <div v-else class="table-wrap">
        <table class="table">
          <thead>
            <tr>
              <th>Paciente</th>
              <th>Alergias</th>
              <th>Enfermedades crónicas</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in records" :key="item.id">
              <td>{{ item.paciente_nombre }}</td>
              <td>{{ item.alergias || "Sin registro" }}</td>
              <td>{{ item.enfermedades_cronicas || "Sin registro" }}</td>
              <td class="actions">
                <button class="ghost-button" @click="openEdit(item)">Editar</button>
                <button class="danger-button" @click="removeRecord(item.id)">Eliminar</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </article>

    <BaseModal :open="modalOpen" :title="editingId ? 'Editar expediente' : 'Nuevo expediente'" eyebrow="Expedientes" @close="closeModal">
      <form class="grid" @submit.prevent="saveRecord">
        <label>
          Paciente
          <select v-model="form.paciente" class="select" required>
            <option value="">Selecciona</option>
            <option v-for="item in availablePatients" :key="item.id" :value="item.id">{{ item.nombre_completo }}</option>
          </select>
        </label>
        <label>
          Alergias
          <textarea v-model="form.alergias" class="textarea" />
        </label>
        <label>
          Enfermedades crónicas
          <textarea v-model="form.enfermedades_cronicas" class="textarea" />
        </label>
        <div class="actions" style="justify-content: flex-end;">
          <button class="ghost-button" type="button" @click="closeModal">Cancelar</button>
          <button class="primary-button" :disabled="saving" type="submit">
            {{ saving ? "Guardando..." : "Guardar expediente" }}
          </button>
        </div>
      </form>
    </BaseModal>
  </section>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from "vue";

import BaseModal from "../../components/BaseModal.vue";
import PageHeader from "../../components/PageHeader.vue";
import api from "../../services/api";

const loading = ref(true);
const saving = ref(false);
const error = ref("");
const modalOpen = ref(false);
const editingId = ref(null);
const records = ref([]);
const patients = ref([]);
const form = reactive({
  paciente: "",
  alergias: "",
  enfermedades_cronicas: "",
});

const availablePatients = computed(() => {
  const usedIds = new Set(
    records.value
      .filter((item) => item.id !== editingId.value)
      .map((item) => item.paciente)
  );
  return patients.value.filter((item) => !usedIds.has(item.id) || item.id === Number(form.paciente));
});

function resetForm() {
  form.paciente = "";
  form.alergias = "";
  form.enfermedades_cronicas = "";
  editingId.value = null;
}

function openCreate() {
  resetForm();
  modalOpen.value = true;
}

function openEdit(item) {
  editingId.value = item.id;
  form.paciente = item.paciente;
  form.alergias = item.alergias;
  form.enfermedades_cronicas = item.enfermedades_cronicas;
  modalOpen.value = true;
}

function closeModal() {
  modalOpen.value = false;
}

async function loadData() {
  loading.value = true;
  error.value = "";

  try {
    const [recordsRes, patientsRes] = await Promise.all([
      api.get("expedientes/"),
      api.get("pacientes/"),
    ]);
    records.value = recordsRes.data;
    patients.value = patientsRes.data;
  } catch {
    error.value = "No fue posible cargar los expedientes.";
  } finally {
    loading.value = false;
  }
}

async function saveRecord() {
  saving.value = true;

  try {
    if (editingId.value) {
      await api.put(`expedientes/${editingId.value}/`, form);
    } else {
      await api.post("expedientes/", form);
    }
    closeModal();
    await loadData();
  } finally {
    saving.value = false;
  }
}

async function removeRecord(id) {
  if (!window.confirm("¿Eliminar expediente?")) return;
  await api.delete(`expedientes/${id}/`);
  await loadData();
}

onMounted(loadData);
</script>
