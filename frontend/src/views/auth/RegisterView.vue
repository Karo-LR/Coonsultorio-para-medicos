<template>
  <div class="auth-page">
    <section class="auth-page__hero">
      <div class="auth-page__content">
        <p class="eyebrow">Registro seguro</p>
        <h1>Crea una cuenta clinica con acceso controlado.</h1>
        <p class="muted">
          El primer usuario del sistema debe ser admin. Despues, solo un admin autenticado puede crear doctores y recepcionistas.
        </p>
      </div>
    </section>

    <section class="auth-page__form-wrap">
      <form class="card auth-form" @submit.prevent="submit">
        <div>
          <p class="eyebrow">Registro</p>
          <h2>Crear cuenta</h2>
          <p class="muted">Si ya existe un admin, el registro publico queda desactivado.</p>
        </div>

        <div class="grid grid--2">
          <label>
            Nombre
            <input v-model="form.first_name" class="input" required />
          </label>
          <label>
            Apellido
            <input v-model="form.last_name" class="input" />
          </label>
        </div>

        <label>
          Email
          <input v-model="form.email" class="input" type="email" required />
        </label>

        <label>
          Rol
          <select v-model="form.rol" class="select" required>
            <option value="doctor">Doctor</option>
            <option value="recepcionista">Recepcionista</option>
          </select>
        </label>

        <div class="grid grid--2">
          <label>
            Contrasena
            <input v-model="form.password" class="input" type="password" required />
          </label>
          <label>
            Confirmar contrasena
            <input v-model="form.password_confirm" class="input" type="password" required />
          </label>
        </div>

        <p v-if="success" class="empty-state">{{ success }}</p>
        <p v-if="error" class="error-state">{{ error }}</p>

        <button class="primary-button" :disabled="loading" type="submit">
          {{ loading ? "Registrando..." : "Crear cuenta" }}
        </button>

        <router-link class="ghost-button auth-form__link" to="/login">
          Ya tengo cuenta
        </router-link>
      </form>
    </section>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue";

import api from "../../services/api";

const loading = ref(false);
const error = ref("");
const success = ref("");
const form = reactive({
  first_name: "",
  last_name: "",
  email: "",
  password: "",
  password_confirm: "",
  rol: "doctor",
});

function extractError(requestError) {
  if (!requestError.response) {
    return "El backend no esta corriendo o no responde en http://127.0.0.1:8000/api/.";
  }

  const data = requestError.response?.data;
  if (!data) return "No fue posible completar el registro.";
  if (data.detail) return data.detail;
  const firstKey = Object.keys(data)[0];
  const firstValue = data[firstKey];
  return Array.isArray(firstValue) ? firstValue[0] : "No fue posible completar el registro.";
}

async function submit() {
  loading.value = true;
  error.value = "";
  success.value = "";

  try {
    const { data } = await api.post("auth/register/", form);
    success.value = data.detail;
    form.first_name = "";
    form.last_name = "";
    form.email = "";
    form.password = "";
    form.password_confirm = "";
    form.rol = "doctor";
  } catch (requestError) {
    error.value = extractError(requestError);
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 1.05fr 0.95fr;
  background:
    radial-gradient(circle at left top, rgba(8, 47, 73, 0.14), transparent 34%),
    linear-gradient(135deg, #f8fafc 0%, #e8f5f4 100%);
}

.auth-page__hero,
.auth-page__form-wrap {
  display: grid;
  align-items: center;
}

.auth-page__hero {
  padding: 56px;
}

.auth-page__content {
  max-width: 560px;
}

.auth-page__content h1 {
  font-size: clamp(2.1rem, 4.6vw, 4rem);
  line-height: 1.06;
}

.auth-page__form-wrap {
  padding: 24px;
}

.auth-form {
  width: min(560px, 100%);
  display: grid;
  gap: 16px;
}

.auth-form label {
  display: grid;
  gap: 8px;
  color: var(--muted);
}

.auth-form__link {
  text-align: center;
  text-decoration: none;
}

@media (max-width: 900px) {
  .auth-page {
    grid-template-columns: 1fr;
  }

  .auth-page__hero {
    padding: 28px 24px 0;
  }
}
</style>
