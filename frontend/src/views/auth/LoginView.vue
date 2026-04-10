<template>
  <div class="auth-page">
    <section class="auth-page__hero">
      <div class="auth-page__content">
        <p class="eyebrow">Acceso clinico seguro</p>
        <h1>Te brindamos todas las herramientas.</h1>
        <p class="muted">
          Para registrar la información de sus pacientes y administrar eficientemente su oficina.
        </p>
        <img class="auth-logo" src="@/assets/LogoConsultorio.jpg" alt="Logo Consultorio" />
      </div>
    </section>

    <section class="auth-page__form-wrap">
      <form class="card auth-form" @submit.prevent="submit">
        <div>
          <p class="eyebrow">Login</p>
          <h2>Entrar al sistema</h2>
          <p class="muted">Usa tu correo registrado o tu nombre de usuario.</p>
        </div>

        <label>
          Correo o usuario
          <input v-model="form.email" class="input" type="text" required />
        </label>

        <label>
          Contrasena
          <input v-model="form.password" class="input" type="password" required />
        </label>

        <p class="muted auth-note">
          El alta de doctores y recepcionistas se realiza desde el panel administrativo.
        </p>

        <p v-if="success" class="empty-state">{{ success }}</p>
        <p v-if="error" class="error-state">{{ error }}</p>

        <button class="primary-button" :disabled="loading" type="submit">
          {{ loading ? "Ingresando..." : "Entrar" }}
        </button>
      </form>
    </section>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

import api from "../../services/api";
import { setSession } from "../../services/session";

const route = useRoute();
const router = useRouter();
const loading = ref(false);
const error = ref("");
const success = ref(route.query.verified ? "Correo verificado. Ya puedes iniciar sesion." : "");
const form = reactive({
  email: "",
  password: "",
});

function extractError(requestError) {
  if (!requestError.response) {
    return "El backend no esta corriendo o no responde en http://localhost:8000/api/.";
  }

  const data = requestError.response?.data;
  if (!data) return "No fue posible iniciar sesion.";
  if (data.detail) return data.detail;
  const firstKey = Object.keys(data)[0];
  const firstValue = data[firstKey];
  return Array.isArray(firstValue) ? firstValue[0] : "No fue posible iniciar sesion.";
}

async function submit() {
  loading.value = true;
  error.value = "";
  success.value = "";

  try {
    const { data } = await api.post("auth/login/", form);
    setSession({
      access: data.access,
      refresh: data.refresh,
      user: data.user,
    });
    router.push("/dashboard");
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
  grid-template-columns: 1.1fr 0.9fr;
  background:
    radial-gradient(circle at left top, rgba(20, 83, 45, 0.16), transparent 34%),
    linear-gradient(135deg, #f8fafc 0%, #e2f3ef 100%);
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
  max-width: 580px;
}

.auth-logo {
  width: 220px;
  height: auto;
  margin-top: 20px;
  display: block;
}

.auth-page__content h1 {
  font-size: clamp(2.2rem, 5vw, 4.2rem);
  line-height: 1.05;
}

.auth-page__form-wrap {
  padding: 24px;
}

.auth-form {
  width: min(460px, 100%);
  display: grid;
  gap: 16px;
}

.auth-form label {
  display: grid;
  gap: 8px;
  color: var(--muted);
}

.auth-note {
  margin: 0;
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
