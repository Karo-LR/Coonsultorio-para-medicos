<template>
  <aside :class="['sidebar', { 'sidebar--open': mobileOpen }]">
    <div>
      <div class="sidebar__brand">
        <p class="eyebrow">Clinical OS</p>
        <h2>Consultorio Pro</h2>
        <p class="sidebar__copy">
          Plataforma clinica moderna para operacion diaria y crecimiento.
        </p>
      </div>

      <nav class="sidebar__nav">
        <div v-for="section in sections" :key="section.title" class="sidebar__section">
          <p class="sidebar__section-title">{{ section.title }}</p>

          <router-link
            v-for="item in section.items"
            :key="item.to"
            :to="item.to"
            class="sidebar__link"
            @click="$emit('close-mobile')"
          >
            {{ item.label }}
          </router-link>
        </div>
      </nav>
    </div>

    <div class="sidebar__footer">
      <div class="sidebar__user">
        <strong>{{ user?.nombre || "Equipo clinico" }}</strong>
        <span>{{ user?.rol || "staff" }}</span>
      </div>

      <button class="danger-button" @click="$emit('logout')">Logout</button>
    </div>
  </aside>
</template>

<script setup>
/* global defineProps, defineEmits */
import { computed } from "vue";

const props = defineProps({
  mobileOpen: {
    type: Boolean,
    default: false,
  },
  user: {
    type: Object,
    default: null,
  },
});

defineEmits(["close-mobile", "logout"]);

const sectionDefinitions = [
  {
    title: "Principal",
    items: [
      { label: "Dashboard", to: "/dashboard", roles: ["admin", "doctor", "recepcionista"] },
      { label: "Pacientes", to: "/pacientes", roles: ["admin", "doctor", "recepcionista"] },
      { label: "Citas", to: "/citas", roles: ["admin", "doctor", "recepcionista"] },
      { label: "Expedientes", to: "/expedientes", roles: ["admin", "doctor"] },
      { label: "Consultas", to: "/consultas", roles: ["admin", "doctor"] },
      { label: "Recetas", to: "/recetas", roles: ["admin", "doctor"] },
    ],
  },
  {
    title: "Administracion",
    items: [
      { label: "Doctores", to: "/administracion/doctores", roles: ["admin"] },
      { label: "Medicamentos", to: "/administracion/medicamentos", roles: ["admin"] },
      { label: "Facturacion", to: "/administracion/facturacion", roles: ["admin"] },
    ],
  },
  {
    title: "Sistema",
    items: [
      { label: "Panel Admin", to: "/sistema/admin-panel", roles: ["admin"] },
      { label: "Subir archivos", to: "/sistema/uploads", roles: ["admin"] },
      { label: "Perfil", to: "/sistema/perfil", roles: ["admin", "doctor", "recepcionista"] },
    ],
  },
];

const sections = computed(() => {
  const role = props.user?.rol;

  return sectionDefinitions
    .map((section) => ({
      ...section,
      items: section.items.filter((item) => item.roles.includes(role)),
    }))
    .filter((section) => section.items.length > 0);
});
</script>

<style scoped>
.sidebar {
  background:
    linear-gradient(180deg, rgba(8, 47, 73, 0.98), rgba(15, 23, 42, 0.98)),
    #0f172a;
  color: #e2e8f0;
  padding: 28px 22px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 100vh;
  position: sticky;
  top: 0;
}

.sidebar__brand h2 {
  margin: 6px 0;
}

.sidebar__copy {
  color: #94a3b8;
  line-height: 1.5;
}

.sidebar__nav {
  margin-top: 28px;
  display: grid;
  gap: 24px;
}

.sidebar__section {
  display: grid;
  gap: 8px;
}

.sidebar__section-title {
  font-size: 0.76rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #64748b;
  margin: 0 0 6px;
}

.sidebar__link {
  color: #dbeafe;
  text-decoration: none;
  padding: 12px 14px;
  border-radius: 14px;
  transition: background-color 0.2s ease, transform 0.2s ease;
}

.sidebar__link:hover,
.sidebar__link.router-link-active {
  background: rgba(148, 163, 184, 0.16);
  transform: translateX(2px);
}

.sidebar__footer {
  display: grid;
  gap: 16px;
}

.sidebar__user {
  display: grid;
  gap: 4px;
  padding: 14px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.08);
}

.sidebar__user span {
  text-transform: capitalize;
  color: #93c5fd;
}

@media (max-width: 960px) {
  .sidebar {
    position: fixed;
    inset: 0 auto 0 0;
    width: min(320px, 90vw);
    transform: translateX(-100%);
    transition: transform 0.25s ease;
    z-index: 30;
  }

  .sidebar--open {
    transform: translateX(0);
  }
}
</style>
