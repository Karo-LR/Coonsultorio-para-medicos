<template>
  <section class="grid">
    <PageHeader
      eyebrow="Paciente"
      :title="patient.nombre_completo || 'Detalle del paciente'"
      description="Vista clínica central con expediente, consultas, recetas y citas ligadas."
    >
      <template #actions>
        <router-link class="ghost-button" to="/pacientes">Volver</router-link>
      </template>
    </PageHeader>

    <div v-if="loading" class="loading-state">Cargando detalle...</div>
    <div v-else-if="error" class="error-state">{{ error }}</div>
    <template v-else>
      <div class="grid grid--3">
        <article class="card">
          <p class="eyebrow">Contacto</p>
          <h3>{{ patient.nombre_completo }}</h3>
          <p class="muted">{{ patient.telefono }}</p>
          <p>{{ patient.direccion }}</p>
        </article>
        <article class="card">
          <p class="eyebrow">Historial clínico</p>
          <h3>Alergias</h3>
          <p>{{ expediente?.alergias || "Sin registro" }}</p>
          <h3>Crónicas</h3>
          <p>{{ expediente?.enfermedades_cronicas || "Sin registro" }}</p>
        </article>
        <article class="card">
          <p class="eyebrow">Actividad</p>
          <h3>{{ appointments.length }} citas</h3>
          <p class="muted">{{ consultations.length }} consultas y {{ prescriptions.length }} recetas asociadas.</p>
        </article>
      </div>

      <div class="grid grid--2">
        <article class="card">
          <div class="actions" style="justify-content: space-between; margin-bottom: 16px;">
            <div>
              <p class="eyebrow">Citas</p>
              <h3>Agenda del paciente</h3>
            </div>
            <router-link class="ghost-button" to="/citas">Ver módulo</router-link>
          </div>

          <div v-if="appointments.length === 0" class="empty-state">Sin citas registradas.</div>
          <div v-else class="grid">
            <article v-for="item in appointments" :key="item.id" class="card">
              <div class="actions" style="justify-content: space-between;">
                <strong>{{ formatDateTime(item.fecha) }}</strong>
                <span :class="['badge', `badge--${item.estado}`]">{{ item.estado }}</span>
              </div>
              <p class="muted">{{ item.doctor_nombre }}</p>
              <p>{{ item.motivo }}</p>
            </article>
          </div>
        </article>

        <article class="card">
          <div class="actions" style="justify-content: space-between; margin-bottom: 16px;">
            <div>
              <p class="eyebrow">Consultas</p>
              <h3>Seguimiento médico</h3>
            </div>
            <router-link class="ghost-button" to="/consultas">Ver módulo</router-link>
          </div>

          <div v-if="consultations.length === 0" class="empty-state">Sin consultas registradas.</div>
          <div v-else class="grid">
            <article v-for="item in consultations" :key="item.id" class="card">
              <strong>{{ formatDateTime(item.cita_fecha || item.fecha || item.cita?.fecha) }}</strong>
              <p>{{ item.diagnostico }}</p>
              <p class="muted">{{ item.tratamiento }}</p>
            </article>
          </div>
        </article>
      </div>

      <article class="card">
        <div class="actions" style="justify-content: space-between; margin-bottom: 16px;">
          <div>
            <p class="eyebrow">Recetas</p>
            <h3>Prescripciones asociadas</h3>
          </div>
          <router-link class="ghost-button" to="/recetas">Ver módulo</router-link>
        </div>

        <div v-if="prescriptions.length === 0" class="empty-state">Sin recetas registradas.</div>
        <div v-else class="table-wrap">
          <table class="table">
            <thead>
              <tr>
                <th>Medicamento</th>
                <th>Dosis</th>
                <th>Indicaciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in prescriptions" :key="item.id">
                <td>{{ item.medicamento }}</td>
                <td>{{ item.dosis }}</td>
                <td>{{ item.indicaciones }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </article>
    </template>
  </section>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";

import PageHeader from "../../components/PageHeader.vue";
import api from "../../services/api";

const route = useRoute();
const loading = ref(true);
const error = ref("");
const patient = ref({});
const expediente = ref(null);
const appointments = ref([]);
const consultations = ref([]);
const prescriptions = ref([]);

function formatDateTime(value) {
  if (!value) return "Sin fecha";
  return new Date(value).toLocaleString("es-MX", {
    dateStyle: "medium",
    timeStyle: "short",
  });
}

async function loadData() {
  loading.value = true;
  error.value = "";

  try {
    const patientId = route.params.id;
    const [patientRes, expedienteRes, citasRes, consultasRes, recetasRes] = await Promise.all([
      api.get(`pacientes/${patientId}/`),
      api.get(`expedientes/?paciente=${patientId}`),
      api.get(`citas/?paciente=${patientId}`),
      api.get(`consultas/?paciente=${patientId}`),
      api.get(`recetas/?paciente=${patientId}`),
    ]);

    patient.value = patientRes.data;
    expediente.value = expedienteRes.data[0] || null;
    appointments.value = citasRes.data;
    consultations.value = consultasRes.data;
    prescriptions.value = recetasRes.data;
  } catch {
    error.value = "No fue posible cargar el detalle del paciente.";
  } finally {
    loading.value = false;
  }
}

onMounted(loadData);
</script>
