<template>
  <section class="grid">
    <PageHeader
      eyebrow="Administracion"
      title="Gestion de usuarios"
      description="El administrador da de alta doctores y recepcionistas desde este panel seguro."
    >
      <template #actions>
        <button class="primary-button" @click="openCreateModal">Nuevo usuario</button>
      </template>
    </PageHeader>

    <div class="grid grid--3">
      <article class="card">
        <p class="eyebrow">Resumen</p>
        <h3>{{ stats.total }}</h3>
        <p class="muted">Usuarios operativos visibles para administracion.</p>
      </article>
      <article class="card">
        <p class="eyebrow">Doctores</p>
        <h3>{{ stats.doctors }}</h3>
        <p class="muted">Personal medico disponible en el sistema.</p>
      </article>
      <article class="card">
        <p class="eyebrow">Recepcion</p>
        <h3>{{ stats.receptionists }}</h3>
        <p class="muted">Usuarios administrativos de agenda y registro.</p>
      </article>
    </div>

    <article class="card">
      <div class="toolbar">
        <input
          v-model.trim="search"
          class="input users-search"
          type="text"
          placeholder="Buscar por nombre, email o rol"
        />
        <button class="ghost-button" :disabled="loading" @click="loadUsers">Actualizar</button>
      </div>

      <div v-if="loading" class="loading-state">Cargando usuarios...</div>
      <div v-else-if="error" class="error-state">{{ error }}</div>
      <div v-else-if="filteredUsers.length === 0" class="empty-state">
        No hay usuarios que coincidan con la busqueda.
      </div>
      <div v-else class="table-wrap">
        <table class="table">
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Usuario</th>
              <th>Email</th>
              <th>Rol</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in filteredUsers" :key="user.id">
              <td>{{ user.nombre }}</td>
              <td>{{ user.username }}</td>
              <td>{{ user.email }}</td>
              <td><span class="badge users-badge">{{ user.rol }}</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </article>

    <BaseModal
      :open="showCreateModal"
      title="Nuevo usuario"
      eyebrow="Alta interna"
      @close="closeCreateModal"
    >
      <form class="grid" @submit.prevent="submitUser">
        <div class="grid grid--2">
          <label>
            Nombre
            <input v-model="createForm.first_name" class="input" required />
          </label>
          <label>
            Apellido
            <input v-model="createForm.last_name" class="input" />
          </label>
        </div>

        <label>
          Email
          <input v-model="createForm.email" class="input" type="email" required />
        </label>

        <label>
          Rol
          <select v-model="createForm.rol" class="select" required>
            <option value="doctor">Doctor</option>
            <option value="recepcionista">Recepcionista</option>
          </select>
        </label>

        <div class="grid grid--2">
          <label>
            Contrasena
            <input v-model="createForm.password" class="input" type="password" required />
          </label>
          <label>
            Confirmar contrasena
            <input v-model="createForm.password_confirm" class="input" type="password" required />
          </label>
        </div>

        <p v-if="createSuccess" class="empty-state">{{ createSuccess }}</p>
        <p v-if="createError" class="error-state">{{ createError }}</p>

        <div class="actions">
          <button class="primary-button" :disabled="saving" type="submit">
            {{ saving ? "Guardando..." : "Crear usuario" }}
          </button>
          <button class="ghost-button" type="button" @click="closeCreateModal">Cancelar</button>
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
const createError = ref("");
const createSuccess = ref("");
const search = ref("");
const showCreateModal = ref(false);
const users = ref([]);
const createForm = reactive({
  first_name: "",
  last_name: "",
  email: "",
  password: "",
  password_confirm: "",
  rol: "doctor",
});

const filteredUsers = computed(() => {
  const query = search.value.toLowerCase();
  if (!query) {
    return users.value;
  }

  return users.value.filter((user) =>
    [user.nombre, user.username, user.email, user.rol].some((value) =>
      String(value || "").toLowerCase().includes(query)
    )
  );
});

const stats = computed(() => ({
  total: users.value.length,
  doctors: users.value.filter((user) => user.rol === "doctor").length,
  receptionists: users.value.filter((user) => user.rol === "recepcionista").length,
}));

function extractError(requestError, fallback) {
  if (!requestError.response) {
    return "El backend no esta corriendo o no responde en http://localhost:8000/api/.";
  }

  const data = requestError.response?.data;
  if (!data) return fallback;
  if (data.detail) return data.detail;
  const firstKey = Object.keys(data)[0];
  const firstValue = data[firstKey];
  return Array.isArray(firstValue) ? firstValue[0] : fallback;
}

function resetCreateForm() {
  createForm.first_name = "";
  createForm.last_name = "";
  createForm.email = "";
  createForm.password = "";
  createForm.password_confirm = "";
  createForm.rol = "doctor";
}

function openCreateModal() {
  createError.value = "";
  createSuccess.value = "";
  showCreateModal.value = true;
}

function closeCreateModal() {
  showCreateModal.value = false;
  createError.value = "";
  createSuccess.value = "";
  resetCreateForm();
}

async function loadUsers() {
  loading.value = true;
  error.value = "";

  try {
    const { data } = await api.get("perfiles/");
    users.value = data.filter((item) => item.rol !== "admin");
  } catch (requestError) {
    error.value = extractError(requestError, "No fue posible cargar los usuarios.");
  } finally {
    loading.value = false;
  }
}

async function submitUser() {
  saving.value = true;
  createError.value = "";
  createSuccess.value = "";

  try {
    const { data } = await api.post("auth/register/", createForm);
    createSuccess.value = data.detail;
    await loadUsers();
    resetCreateForm();
  } catch (requestError) {
    createError.value = extractError(requestError, "No fue posible crear el usuario.");
  } finally {
    saving.value = false;
  }
}

onMounted(loadUsers);
</script>

<style scoped>
.users-search {
  flex: 1 1 320px;
}

.users-badge {
  text-transform: capitalize;
}
</style>
