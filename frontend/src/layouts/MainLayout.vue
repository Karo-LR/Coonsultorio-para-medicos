<template>
  <div class="shell">
    <AppSidebar
      :user="user"
      :mobile-open="mobileOpen"
      @close-mobile="mobileOpen = false"
      @logout="logout"
    />

    <div class="shell__content">
      <header class="shell__header card">
        <div>
          <p class="eyebrow">Gestión clínica</p>
          <h1>{{ currentTitle }}</h1>
        </div>

        <div class="shell__header-actions">
          <button class="ghost-button mobile-only" @click="mobileOpen = !mobileOpen">
            Menú
          </button>
          <router-link class="ghost-button" to="/sistema/perfil">
            {{ user?.nombre || "Mi perfil" }}
          </router-link>
        </div>
      </header>

      <main class="shell__main">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

import AppSidebar from "../components/AppSidebar.vue";
import { clearSession, getStoredUser } from "../services/session";

const route = useRoute();
const router = useRouter();
const mobileOpen = ref(false);
const user = ref(getStoredUser());

const currentTitle = computed(() => route.meta.title || "Panel");

function logout() {
  clearSession();
  router.push("/login");
}
</script>

<style scoped>
.shell {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 300px 1fr;
  background:
    radial-gradient(circle at top left, rgba(209, 250, 229, 0.9), transparent 30%),
    linear-gradient(180deg, #f8fafc 0%, #eef2f7 100%);
}

.shell__content {
  min-width: 0;
  padding: 24px;
}

.shell__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 24px;
}

.shell__header-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.shell__main {
  min-width: 0;
}

.mobile-only {
  display: none;
}

@media (max-width: 960px) {
  .shell {
    grid-template-columns: 1fr;
  }

  .shell__content {
    padding: 16px;
  }

  .mobile-only {
    display: inline-flex;
  }
}
</style>
