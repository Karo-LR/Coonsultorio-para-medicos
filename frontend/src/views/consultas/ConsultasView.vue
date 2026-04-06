<template>
  <section class="grid">
    <PageHeader
      eyebrow="Atención"
      title="Consultas"
      description="Consultas ligadas a cita con diagnóstico, tratamiento y exportación PDF."
    >
      <template #actions>
        <button class="primary-button" @click="openCreate">Nueva consulta</button>
      </template>
    </PageHeader>

    <div v-if="error" class="error-state">{{ error }}</div>

    <article class="card">
      <div v-if="loading" class="loading-state">Cargando consultas...</div>
      <div v-else-if="consultations.length === 0" class="empty-state">Sin consultas registradas.</div>
      <div v-else class="table-wrap">
        <table class="table">
          <thead>
            <tr>
              <th>Paciente</th>
              <th>Cita</th>
              <th>Diagnóstico</th>
              <th>Tratamiento</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in consultations" :key="item.id">
              <td>{{ item.paciente_nombre }}</td>
              <td>{{ formatDateTime(citaMap[item.cita]?.fecha) }}</td>
              <td>{{ item.diagnostico }}</td>
              <td>{{ item.tratamiento }}</td>
              <td class="actions">
                <button class="ghost-button" @click="openEdit(item)">Editar</button>
                <button class="ghost-button" @click="downloadPdf(item.id)">PDF</button>
                <button class="danger-button" @click="removeConsultation(item.id)">Eliminar</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </article>

    <BaseModal :open="modalOpen" :title="editingId ? 'Editar consulta' : 'Nueva consulta'" eyebrow="Consultas" @close="closeModal">
      <form class="grid" @submit.prevent="saveConsultation">
        <label>
          Cita
          <select v-model="form.cita" class="select" required>
            <option value="">Selecciona una cita</option>
            <option v-for="item in availableAppointments" :key="item.id" :value="item.id">
              {{ item.paciente_nombre }} · {{ formatDateTime(item.fecha) }}
            </option>
          </select>
        </label>
        <label>
          Diagnóstico
          <textarea v-model="form.diagnostico" class="textarea" required />
        </label>
        <label>
          Tratamiento
          <textarea v-model="form.tratamiento" class="textarea" required />
        </label>
        <p v-if="formError" class="error-state">{{ formError }}</p>
        <div class="actions" style="justify-content: flex-end;">
          <button class="ghost-button" type="button" @click="closeModal">Cancelar</button>
          <button class="primary-button" :disabled="saving" type="submit">
            {{ saving ? "Guardando..." : "Guardar consulta" }}
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
const formError = ref("");
const modalOpen = ref(false);
const editingId = ref(null);
const consultations = ref([]);
const appointments = ref([]);
const form = reactive({
  cita: "",
  diagnostico: "",
  tratamiento: "",
});

const citaMap = computed(() =>
  appointments.value.reduce((acc, item) => {
    acc[item.id] = item;
    return acc;
  }, {})
);

const availableAppointments = computed(() => {
  const usedIds = new Set(
    consultations.value
      .filter((item) => item.id !== editingId.value)
      .map((item) => item.cita)
  );
  return appointments.value.filter((item) => !usedIds.has(item.id) || item.id === Number(form.cita));
});

function formatDateTime(value) {
  if (!value) return "Sin fecha";
  return new Date(value).toLocaleString("es-MX", {
    dateStyle: "medium",
    timeStyle: "short",
  });
}

function extractError(requestError) {
  const data = requestError.response?.data;
  if (!data) return "No se pudo guardar la consulta.";
  const firstKey = Object.keys(data)[0];
  const firstValue = data[firstKey];
  return Array.isArray(firstValue) ? firstValue[0] : "No se pudo guardar la consulta.";
}

function resetForm() {
  form.cita = "";
  form.diagnostico = "";
  form.tratamiento = "";
  editingId.value = null;
}

function openCreate() {
  resetForm();
  formError.value = "";
  modalOpen.value = true;
}

function openEdit(item) {
  editingId.value = item.id;
  form.cita = item.cita;
  form.diagnostico = item.diagnostico;
  form.tratamiento = item.tratamiento;
  formError.value = "";
  modalOpen.value = true;
}

function closeModal() {
  modalOpen.value = false;
}

async function downloadPdf(id) {
  const response = await api.get(`consultas/${id}/pdf/`, {
    responseType: "blob",
  });
  const blobUrl = URL.createObjectURL(new Blob([response.data], { type: "application/pdf" }));
  window.open(blobUrl, "_blank");
}

async function loadData() {
  loading.value = true;
  error.value = "";

  try {
    const [consultasRes, citasRes] = await Promise.all([
      api.get("consultas/"),
      api.get("citas/"),
    ]);
    consultations.value = consultasRes.data;
    appointments.value = citasRes.data;
  } catch {
    error.value = "No fue posible cargar las consultas.";
  } finally {
    loading.value = false;
  }
}

async function saveConsultation() {
  saving.value = true;
  formError.value = "";

  try {
    if (editingId.value) {
      await api.put(`consultas/${editingId.value}/`, form);
    } else {
      await api.post("consultas/", form);
    }
    closeModal();
    await loadData();
  } catch (requestError) {
    formError.value = extractError(requestError);
  } finally {
    saving.value = false;
  }
}

async function removeConsultation(id) {
  if (!window.confirm("¿Eliminar consulta?")) return;
  await api.delete(`consultas/${id}/`);
  await loadData();
}

onMounted(loadData);
</script>
