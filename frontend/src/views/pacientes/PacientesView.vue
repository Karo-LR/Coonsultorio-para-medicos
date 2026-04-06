<template>
  <section class="grid">
    <PageHeader
      eyebrow="Gestión"
      title="Pacientes"
      description="CRUD completo con búsqueda rápida y acceso al detalle clínico."
    >
      <template #actions>
        <input
          v-model="search"
          class="input"
          placeholder="Buscar por nombre, teléfono o dirección"
        />
        <button class="primary-button" @click="openCreate">Nuevo paciente</button>
      </template>
    </PageHeader>

    <div v-if="error" class="error-state">{{ error }}</div>

    <article class="card">
      <div v-if="loading" class="loading-state">Cargando pacientes...</div>
      <div v-else-if="filteredPatients.length === 0" class="empty-state">
        No hay pacientes para mostrar.
      </div>
      <div v-else class="table-wrap">
        <table class="table">
          <thead>
            <tr>
              <th>Paciente</th>
              <th>Teléfono</th>
              <th>Fecha nac.</th>
              <th>Dirección</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="patient in filteredPatients" :key="patient.id">
              <td>
                <strong>{{ patient.nombre_completo }}</strong>
              </td>
              <td>{{ patient.telefono }}</td>
              <td>{{ patient.fecha_nacimiento }}</td>
              <td>{{ patient.direccion }}</td>
              <td class="actions">
                <router-link class="ghost-button" :to="`/pacientes/${patient.id}`">Detalle</router-link>
                <button class="ghost-button" @click="openEdit(patient)">Editar</button>
                <button class="danger-button" @click="removePatient(patient.id)">Eliminar</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </article>

    <BaseModal
      :open="modalOpen"
      :title="isEditing ? 'Editar paciente' : 'Nuevo paciente'"
      eyebrow="Pacientes"
      @close="closeModal"
    >
      <form class="grid grid--2" @submit.prevent="savePatient">
        <label>
          Nombre
          <input v-model="form.nombre" class="input" required />
        </label>
        <label>
          Apellido
          <input v-model="form.apellido" class="input" required />
        </label>
        <label>
          Teléfono
          <input v-model="form.telefono" class="input" required />
        </label>
        <label>
          Fecha de nacimiento
          <input v-model="form.fecha_nacimiento" class="input" type="date" required />
        </label>
        <label class="grid" style="grid-column: 1 / -1;">
          Dirección
          <textarea v-model="form.direccion" class="textarea" required />
        </label>

        <p v-if="formError" class="error-state" style="grid-column: 1 / -1;">{{ formError }}</p>

        <div class="actions" style="grid-column: 1 / -1; justify-content: flex-end;">
          <button class="ghost-button" type="button" @click="closeModal">Cancelar</button>
          <button class="primary-button" :disabled="saving" type="submit">
            {{ saving ? "Guardando..." : "Guardar" }}
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
const isEditing = ref(false);
const patients = ref([]);
const search = ref("");
const form = reactive({
  id: null,
  nombre: "",
  apellido: "",
  telefono: "",
  direccion: "",
  fecha_nacimiento: "",
});

const filteredPatients = computed(() =>
  patients.value.filter((item) =>
    `${item.nombre_completo} ${item.telefono} ${item.direccion}`
      .toLowerCase()
      .includes(search.value.toLowerCase())
  )
);

function resetForm() {
  form.id = null;
  form.nombre = "";
  form.apellido = "";
  form.telefono = "";
  form.direccion = "";
  form.fecha_nacimiento = "";
}

function openCreate() {
  resetForm();
  formError.value = "";
  isEditing.value = false;
  modalOpen.value = true;
}

function openEdit(patient) {
  Object.assign(form, patient);
  formError.value = "";
  isEditing.value = true;
  modalOpen.value = true;
}

function closeModal() {
  modalOpen.value = false;
}

function extractError(requestError) {
  const data = requestError.response?.data;
  if (!data) return "Ocurrió un error inesperado.";
  if (typeof data === "string") return data;
  const firstKey = Object.keys(data)[0];
  const firstValue = data[firstKey];
  return Array.isArray(firstValue) ? firstValue[0] : "No se pudo procesar la solicitud.";
}

async function loadPatients() {
  loading.value = true;
  error.value = "";

  try {
    const { data } = await api.get("pacientes/");
    patients.value = data;
  } catch {
    error.value = "No fue posible cargar los pacientes.";
  } finally {
    loading.value = false;
  }
}

async function savePatient() {
  saving.value = true;
  formError.value = "";

  try {
    if (isEditing.value) {
      await api.put(`pacientes/${form.id}/`, form);
    } else {
      await api.post("pacientes/", form);
    }
    closeModal();
    await loadPatients();
  } catch (requestError) {
    formError.value = extractError(requestError);
  } finally {
    saving.value = false;
  }
}

async function removePatient(id) {
  if (!window.confirm("¿Eliminar paciente?")) return;
  await api.delete(`pacientes/${id}/`);
  await loadPatients();
}

onMounted(loadPatients);
</script>
