<template>
  <section class="grid">
    <PageHeader
      eyebrow="Prescripción"
      title="Recetas"
      description="Múltiples recetas por consulta para un seguimiento terapéutico claro."
    >
      <template #actions>
        <button class="primary-button" @click="openCreate">Nueva receta</button>
      </template>
    </PageHeader>

    <div v-if="error" class="error-state">{{ error }}</div>

    <article class="card">
      <div v-if="loading" class="loading-state">Cargando recetas...</div>
      <div v-else-if="prescriptions.length === 0" class="empty-state">Sin recetas registradas.</div>
      <div v-else class="table-wrap">
        <table class="table">
          <thead>
            <tr>
              <th>Paciente</th>
              <th>Consulta</th>
              <th>Medicamento</th>
              <th>Dosis</th>
              <th>Indicaciones</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in prescriptions" :key="item.id">
              <td>{{ item.paciente_nombre }}</td>
              <td>#{{ item.consulta }}</td>
              <td>{{ item.medicamento }}</td>
              <td>{{ item.dosis }}</td>
              <td>{{ item.indicaciones }}</td>
              <td class="actions">
                <button class="ghost-button" @click="openEdit(item)">Editar</button>
                <button class="danger-button" @click="removePrescription(item.id)">Eliminar</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </article>

    <BaseModal :open="modalOpen" :title="editingId ? 'Editar receta' : 'Nueva receta'" eyebrow="Recetas" @close="closeModal">
      <form class="grid grid--2" @submit.prevent="savePrescription">
        <label style="grid-column: 1 / -1;">
          Consulta
          <select v-model="form.consulta" class="select" required>
            <option value="">Selecciona</option>
            <option v-for="item in consultations" :key="item.id" :value="item.id">
              {{ item.paciente_nombre }} · #{{ item.id }}
            </option>
          </select>
        </label>
        <label>
          Medicamento
          <input v-model="form.medicamento" class="input" required />
        </label>
        <label>
          Dosis
          <input v-model="form.dosis" class="input" required />
        </label>
        <label class="grid" style="grid-column: 1 / -1;">
          Indicaciones
          <textarea v-model="form.indicaciones" class="textarea" required />
        </label>
        <div class="actions" style="grid-column: 1 / -1; justify-content: flex-end;">
          <button class="ghost-button" type="button" @click="closeModal">Cancelar</button>
          <button class="primary-button" :disabled="saving" type="submit">
            {{ saving ? "Guardando..." : "Guardar receta" }}
          </button>
        </div>
      </form>
    </BaseModal>
  </section>
</template>

<script setup>
import { onMounted, reactive, ref } from "vue";

import BaseModal from "../../components/BaseModal.vue";
import PageHeader from "../../components/PageHeader.vue";
import api from "../../services/api";

const loading = ref(true);
const saving = ref(false);
const error = ref("");
const modalOpen = ref(false);
const editingId = ref(null);
const prescriptions = ref([]);
const consultations = ref([]);
const form = reactive({
  consulta: "",
  medicamento: "",
  dosis: "",
  indicaciones: "",
});

function resetForm() {
  form.consulta = "";
  form.medicamento = "";
  form.dosis = "";
  form.indicaciones = "";
  editingId.value = null;
}

function openCreate() {
  resetForm();
  modalOpen.value = true;
}

function openEdit(item) {
  editingId.value = item.id;
  form.consulta = item.consulta;
  form.medicamento = item.medicamento;
  form.dosis = item.dosis;
  form.indicaciones = item.indicaciones;
  modalOpen.value = true;
}

function closeModal() {
  modalOpen.value = false;
}

async function loadData() {
  loading.value = true;
  error.value = "";

  try {
    const [prescriptionsRes, consultationsRes] = await Promise.all([
      api.get("recetas/"),
      api.get("consultas/"),
    ]);
    prescriptions.value = prescriptionsRes.data;
    consultations.value = consultationsRes.data;
  } catch {
    error.value = "No fue posible cargar las recetas.";
  } finally {
    loading.value = false;
  }
}

async function savePrescription() {
  saving.value = true;

  try {
    if (editingId.value) {
      await api.put(`recetas/${editingId.value}/`, form);
    } else {
      await api.post("recetas/", form);
    }
    closeModal();
    await loadData();
  } finally {
    saving.value = false;
  }
}

async function removePrescription(id) {
  if (!window.confirm("¿Eliminar receta?")) return;
  await api.delete(`recetas/${id}/`);
  await loadData();
}

onMounted(loadData);
</script>
