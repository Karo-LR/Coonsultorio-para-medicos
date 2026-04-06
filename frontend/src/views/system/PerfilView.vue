<template>
  <section class="grid">
    <PageHeader
      eyebrow="Sistema"
      title="Perfil"
      description="Información de sesión y rol actual dentro del sistema clínico."
    />

    <div v-if="loading" class="loading-state">Cargando perfil...</div>
    <div v-else-if="error" class="error-state">{{ error }}</div>
    <div v-else class="grid grid--2">
      <article class="card">
        <p class="eyebrow">Usuario</p>
        <h3>{{ profile.nombre }}</h3>
        <p class="muted">{{ profile.email || "Sin correo registrado" }}</p>
      </article>
      <article class="card">
        <p class="eyebrow">Permisos</p>
        <h3>{{ profile.rol || "Sin rol" }}</h3>
        <p class="muted">El acceso a módulos sensibles se gobierna por rol.</p>
      </article>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from "vue";

import PageHeader from "../../components/PageHeader.vue";
import api from "../../services/api";
import { setSession } from "../../services/session";

const loading = ref(true);
const error = ref("");
const profile = ref({});

async function loadProfile() {
  loading.value = true;
  error.value = "";

  try {
    const { data } = await api.get("auth/me/");
    profile.value = data;
    setSession({ user: data });
  } catch {
    error.value = "No fue posible cargar el perfil actual.";
  } finally {
    loading.value = false;
  }
}

onMounted(loadProfile);
</script>
