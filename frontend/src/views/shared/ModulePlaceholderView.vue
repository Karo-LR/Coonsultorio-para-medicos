<template>
  <section class="grid">
    <PageHeader :eyebrow="'Módulo'" :title="title" :description="description" />

    <div class="grid grid--3">
      <article class="card" v-for="item in cards" :key="item.title">
        <p class="eyebrow">{{ item.eyebrow }}</p>
        <h3>{{ item.title }}</h3>
        <p class="muted">{{ item.description }}</p>
      </article>
    </div>
  </section>
</template>

<script setup>
/* global defineProps */
import { computed } from "vue";

import PageHeader from "../../components/PageHeader.vue";

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    default: "",
  },
  moduleKey: {
    type: String,
    default: "",
  },
});

const definitions = {
  doctores: [
    { eyebrow: "Personal", title: "Doctores activos", description: "Consulta la base operativa desde el menú y la API `/doctores/`." },
    { eyebrow: "Escalabilidad", title: "Agenda médica", description: "Preparado para evolucionar hacia disponibilidad por bloques y especialidades." },
    { eyebrow: "Operación", title: "Control de acceso", description: "Pensado para roles administrativos y trazabilidad por usuario." },
  ],
  medicamentos: [
    { eyebrow: "Catálogo", title: "Base terapéutica", description: "Espacio diseñado para centralizar medicamentos y sus indicaciones." },
    { eyebrow: "Recetas", title: "Conectable con consultas", description: "La estructura actual de recetas ya soporta múltiples registros por consulta." },
    { eyebrow: "Producción", title: "Próximo paso", description: "Agregar inventario, lotes y alertas de stock bajo." },
  ],
  facturacion: [
    { eyebrow: "Finanzas", title: "Corte diario", description: "Resumen ideal para ingresos por consulta, doctor o recepción." },
    { eyebrow: "Auditoría", title: "Trazabilidad", description: "Diseñado para crecer con folios, métodos de pago y exportes." },
    { eyebrow: "Negocio", title: "KPIs", description: "Listo para conectar indicadores y reportes administrativos." },
  ],
  "admin-panel": [
    { eyebrow: "Sistema", title: "Administración avanzada", description: "Accesos reservados para usuarios con rol admin." },
    { eyebrow: "Usuarios", title: "Gobernanza", description: "Punto natural para gestión de permisos, catálogos y bitácoras." },
    { eyebrow: "Seguridad", title: "Entorno protegido", description: "Las rutas sensibles ya están condicionadas por rol en frontend." },
  ],
  uploads: [
    { eyebrow: "Archivos", title: "Carga documental", description: "Vista preparada para expedientes adjuntos, estudios y formatos." },
    { eyebrow: "Flujo", title: "Interfaz escalable", description: "El layout soporta dropzones y estados de carga sin romper consistencia." },
    { eyebrow: "Próximo paso", title: "Backend", description: "Solo faltaría integrar almacenamiento y políticas de acceso por archivo." },
  ],
};

const cards = computed(() => definitions[props.moduleKey] || []);
</script>
