<template>
  <section class="grid">
    <PageHeader
      eyebrow="Resumen"
      title="Dashboard clínico"
      description="Indicadores clave, actividad reciente y seguimiento diario del consultorio."
    />

    <div v-if="loading" class="loading-state">Cargando métricas...</div>
    <div v-else-if="error" class="error-state">{{ error }}</div>
    <template v-else>
      <div class="grid grid--4">
        <article v-for="card in metricCards" :key="card.title" class="card">
          <p class="eyebrow">{{ card.title }}</p>
          <h2>{{ card.value }}</h2>
          <p class="muted">{{ card.caption }}</p>
        </article>
      </div>

      <div class="grid grid--2">
        <article class="card">
          <p class="eyebrow">Actividad</p>
          <h3>Citas recientes</h3>
          <div class="table-wrap">
            <table class="table">
              <thead>
                <tr>
                  <th>Paciente</th>
                  <th>Doctor</th>
                  <th>Fecha</th>
                  <th>Estado</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in dashboard.citas_recientes" :key="item.id">
                  <td>{{ item.paciente }}</td>
                  <td>{{ item.doctor }}</td>
                  <td>{{ formatDateTime(item.fecha) }}</td>
                  <td>
                    <span :class="['badge', badgeClass(item.estado)]">{{ item.estado }}</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </article>

        <article class="card">
          <p class="eyebrow">Consultas</p>
          <h3>Actividad reciente</h3>
          <div class="grid">
            <article
              v-for="item in dashboard.consultas_recientes"
              :key="item.id"
              class="card dashboard-note"
            >
              <strong>{{ item.paciente }}</strong>
              <p class="muted">{{ formatDateTime(item.fecha) }}</p>
              <p>{{ item.diagnostico }}</p>
            </article>
          </div>
        </article>
      </div>
    </template>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";

import PageHeader from "../../components/PageHeader.vue";
import api from "../../services/api";

const loading = ref(true);
const error = ref("");
const dashboard = ref({
  metricas: {},
  citas_recientes: [],
  consultas_recientes: [],
});

const metricCards = computed(() => [
  {
    title: "Pacientes totales",
    value: dashboard.value.metricas.pacientes_totales || 0,
    caption: "Base activa de pacientes registrados.",
  },
  {
    title: "Citas del día",
    value: dashboard.value.metricas.citas_hoy || 0,
    caption: "Agenda prevista para hoy.",
  },
  {
    title: "Doctores activos",
    value: dashboard.value.metricas.doctores_activos || 0,
    caption: "Usuarios clínicos habilitados.",
  },
  {
    title: "Consultas recientes",
    value: dashboard.value.metricas.consultas_recientes || 0,
    caption: "Consultas acumuladas en el sistema.",
  },
]);

function formatDateTime(value) {
  return new Date(value).toLocaleString("es-MX", {
    dateStyle: "medium",
    timeStyle: "short",
  });
}

function badgeClass(status) {
  return `badge--${status}`;
}

async function loadDashboard() {
  loading.value = true;
  error.value = "";

  try {
    const { data } = await api.get("dashboard/");
    dashboard.value = data;
  } catch {
    error.value = "No fue posible cargar el dashboard.";
  } finally {
    loading.value = false;
  }
}

onMounted(loadDashboard);
</script>

<style scoped>
.dashboard-note {
  padding: 16px;
}
</style>
