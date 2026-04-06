<template>
  <section class="grid">
    <PageHeader
      eyebrow="Agenda"
      title="Citas"
      description="Gestiona citas con paciente, doctor, estado y doble vista de lista/calendario."
    >
      <template #actions>
        <select v-model="filters.estado" class="select">
          <option value="">Todos los estados</option>
          <option value="pendiente">Pendiente</option>
          <option value="confirmada">Confirmada</option>
          <option value="completada">Completada</option>
        </select>
        <button class="primary-button" @click="openCreate">Nueva cita</button>
      </template>
    </PageHeader>

    <div class="toolbar">
      <button class="ghost-button" @click="viewMode = 'lista'">Lista</button>
      <button class="ghost-button" @click="viewMode = 'calendario'">Calendario</button>
    </div>

    <div v-if="error" class="error-state">{{ error }}</div>

    <div class="grid grid--2">
      <article v-show="viewMode === 'lista'" class="card">
        <p class="eyebrow">Lista</p>
        <h3>Citas programadas</h3>

        <div v-if="loading" class="loading-state">Cargando citas...</div>
        <div v-else-if="filteredAppointments.length === 0" class="empty-state">Sin citas registradas.</div>
        <div v-else class="table-wrap">
          <table class="table">
            <thead>
              <tr>
                <th>Paciente</th>
                <th>Doctor</th>
                <th>Fecha</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in filteredAppointments" :key="item.id">
                <td>{{ item.paciente_nombre }}</td>
                <td>{{ item.doctor_nombre }}</td>
                <td>{{ formatDateTime(item.fecha) }}</td>
                <td><span :class="['badge', `badge--${item.estado}`]">{{ item.estado }}</span></td>
                <td class="actions">
                  <button class="ghost-button" @click="openEdit(item)">Editar</button>
                  <button class="danger-button" @click="removeAppointment(item.id)">Eliminar</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </article>

      <article v-show="viewMode === 'calendario'" class="card">
        <p class="eyebrow">Calendario</p>
        <h3>Agenda agrupada por día</h3>

        <div v-if="loading" class="loading-state">Preparando agenda...</div>
        <div v-else-if="calendarGroups.length === 0" class="empty-state">No hay eventos para mostrar.</div>
        <div v-else class="grid">
          <article v-for="group in calendarGroups" :key="group.date" class="card">
            <strong>{{ group.label }}</strong>
            <div class="grid" style="margin-top: 12px;">
              <div v-for="item in group.items" :key="item.id">
                <p>{{ timeOnly(item.fecha) }} · {{ item.paciente_nombre }}</p>
                <p class="muted">{{ item.doctor_nombre }} · {{ item.estado }}</p>
              </div>
            </div>
          </article>
        </div>
      </article>
    </div>

    <BaseModal :open="modalOpen" :title="modalTitle" eyebrow="Citas" @close="closeModal">
      <form class="grid grid--2" @submit.prevent="saveAppointment">
        <label>
          Paciente
          <select v-model="form.paciente" class="select" required>
            <option value="">Selecciona</option>
            <option v-for="item in patients" :key="item.id" :value="item.id">{{ item.nombre_completo }}</option>
          </select>
        </label>
        <label>
          Doctor
          <select v-model="form.medico" class="select" required>
            <option value="">Selecciona</option>
            <option v-for="item in doctors" :key="item.id" :value="item.id">{{ item.nombre }}</option>
          </select>
        </label>
        <label>
          Fecha
          <input v-model="form.fecha" class="input" type="datetime-local" required />
        </label>
        <label>
          Estado
          <select v-model="form.estado" class="select" required>
            <option value="pendiente">Pendiente</option>
            <option value="confirmada">Confirmada</option>
            <option value="completada">Completada</option>
          </select>
        </label>
        <label class="grid" style="grid-column: 1 / -1;">
          Motivo
          <textarea v-model="form.motivo" class="textarea" required />
        </label>
        <p v-if="formError" class="error-state" style="grid-column: 1 / -1;">{{ formError }}</p>
        <div class="actions" style="grid-column: 1 / -1; justify-content: flex-end;">
          <button class="ghost-button" type="button" @click="closeModal">Cancelar</button>
          <button class="primary-button" :disabled="saving" type="submit">
            {{ saving ? "Guardando..." : "Guardar cita" }}
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
const viewMode = ref("lista");
const appointments = ref([]);
const patients = ref([]);
const doctors = ref([]);
const filters = reactive({ estado: "" });
const form = reactive({
  paciente: "",
  medico: "",
  fecha: "",
  motivo: "",
  estado: "pendiente",
});

const filteredAppointments = computed(() =>
  appointments.value.filter((item) =>
    filters.estado ? item.estado === filters.estado : true
  )
);

const calendarGroups = computed(() => {
  const groups = filteredAppointments.value.reduce((acc, item) => {
    const dateKey = new Date(item.fecha).toDateString();
    if (!acc[dateKey]) {
      acc[dateKey] = [];
    }
    acc[dateKey].push(item);
    return acc;
  }, {});

  return Object.entries(groups).map(([date, items]) => ({
    date,
    label: new Date(date).toLocaleDateString("es-MX", { dateStyle: "full" }),
    items,
  }));
});

const modalTitle = computed(() => (editingId.value ? "Editar cita" : "Nueva cita"));

function resetForm() {
  form.paciente = "";
  form.medico = "";
  form.fecha = "";
  form.motivo = "";
  form.estado = "pendiente";
  editingId.value = null;
}

function normalizeDate(value) {
  return value ? new Date(value).toISOString() : value;
}

function formatDateTime(value) {
  return new Date(value).toLocaleString("es-MX", {
    dateStyle: "medium",
    timeStyle: "short",
  });
}

function timeOnly(value) {
  return new Date(value).toLocaleTimeString("es-MX", {
    hour: "2-digit",
    minute: "2-digit",
  });
}

function extractError(requestError) {
  const data = requestError.response?.data;
  if (!data) return "No se pudo guardar la cita.";
  const firstKey = Object.keys(data)[0];
  const firstValue = data[firstKey];
  return Array.isArray(firstValue) ? firstValue[0] : "No se pudo guardar la cita.";
}

function openCreate() {
  resetForm();
  formError.value = "";
  modalOpen.value = true;
}

function openEdit(item) {
  editingId.value = item.id;
  form.paciente = item.paciente;
  form.medico = item.medico;
  form.fecha = new Date(item.fecha).toISOString().slice(0, 16);
  form.motivo = item.motivo;
  form.estado = item.estado;
  formError.value = "";
  modalOpen.value = true;
}

function closeModal() {
  modalOpen.value = false;
}

async function loadData() {
  loading.value = true;
  error.value = "";

  try {
    const [citasRes, pacientesRes, doctoresRes] = await Promise.all([
      api.get("citas/"),
      api.get("pacientes/"),
      api.get("doctores/"),
    ]);
    appointments.value = citasRes.data;
    patients.value = pacientesRes.data;
    doctors.value = doctoresRes.data;
  } catch {
    error.value = "No fue posible cargar la agenda.";
  } finally {
    loading.value = false;
  }
}

async function saveAppointment() {
  saving.value = true;
  formError.value = "";

  try {
    const payload = {
      ...form,
      fecha: normalizeDate(form.fecha),
    };
    if (editingId.value) {
      await api.put(`citas/${editingId.value}/`, payload);
    } else {
      await api.post("citas/", payload);
    }
    closeModal();
    await loadData();
  } catch (requestError) {
    formError.value = extractError(requestError);
  } finally {
    saving.value = false;
  }
}

async function removeAppointment(id) {
  if (!window.confirm("¿Eliminar cita?")) return;
  await api.delete(`citas/${id}/`);
  await loadData();
}

onMounted(loadData);
</script>
