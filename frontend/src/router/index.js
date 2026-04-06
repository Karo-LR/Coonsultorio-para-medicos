import { createRouter, createWebHistory } from "vue-router";

import MainLayout from "../layouts/MainLayout.vue";
import LoginView from "../views/auth/LoginView.vue";
import RegisterView from "../views/auth/RegisterView.vue";
import CitasView from "../views/citas/CitasView.vue";
import ConsultasView from "../views/consultas/ConsultasView.vue";
import DashboardView from "../views/dashboard/DashboardView.vue";
import ExpedientesView from "../views/expedientes/ExpedientesView.vue";
import PacientesDetalle from "../views/pacientes/PacientesDetalle.vue";
import PacientesView from "../views/pacientes/PacientesView.vue";
import RecetasView from "../views/recetas/RecetasView.vue";
import ModulePlaceholderView from "../views/shared/ModulePlaceholderView.vue";
import AdminUsersView from "../views/system/AdminUsersView.vue";
import PerfilView from "../views/system/PerfilView.vue";
import { getStoredUser, hasSession } from "../services/session";

const routes = [
  {
    path: "/login",
    name: "login",
    component: LoginView,
    meta: { public: true },
  },
  {
    path: "/register",
    redirect: "/login",
  },
  {
    path: "/register-disabled",
    name: "register",
    component: RegisterView,
    meta: { public: true },
  },
  {
    path: "/",
    component: MainLayout,
    children: [
      {
        path: "",
        redirect: "/dashboard",
      },
      {
        path: "dashboard",
        name: "dashboard",
        component: DashboardView,
        meta: { title: "Dashboard" },
      },
      {
        path: "pacientes",
        name: "pacientes",
        component: PacientesView,
        meta: { title: "Pacientes" },
      },
      {
        path: "pacientes/:id",
        name: "paciente-detalle",
        component: PacientesDetalle,
        meta: { title: "Detalle del paciente" },
      },
      {
        path: "citas",
        name: "citas",
        component: CitasView,
        meta: { title: "Citas" },
      },
      {
        path: "consultas",
        name: "consultas",
        component: ConsultasView,
        meta: { title: "Consultas" },
      },
      {
        path: "expedientes",
        name: "expedientes",
        component: ExpedientesView,
        meta: { title: "Expedientes" },
      },
      {
        path: "recetas",
        name: "recetas",
        component: RecetasView,
        meta: { title: "Recetas" },
      },
      {
        path: "administracion/doctores",
        name: "doctores",
        component: ModulePlaceholderView,
        props: {
          title: "Doctores",
          description: "Directorio operativo de doctores activos y disponibilidad base.",
          moduleKey: "doctores",
        },
        meta: { title: "Doctores", roles: ["admin"] },
      },
      {
        path: "administracion/medicamentos",
        name: "medicamentos",
        component: ModulePlaceholderView,
        props: {
          title: "Medicamentos",
          description: "Catalogo clinico listo para crecer con inventario y prescripcion.",
          moduleKey: "medicamentos",
        },
        meta: { title: "Medicamentos", roles: ["admin"] },
      },
      {
        path: "administracion/facturacion",
        name: "facturacion",
        component: ModulePlaceholderView,
        props: {
          title: "Facturacion",
          description: "Resumen financiero con enfoque administrativo y trazabilidad.",
          moduleKey: "facturacion",
        },
        meta: { title: "Facturacion", roles: ["admin"] },
      },
      {
        path: "sistema/admin-panel",
        name: "admin-panel",
        component: AdminUsersView,
        meta: { title: "Panel Admin", roles: ["admin"] },
      },
      {
        path: "sistema/uploads",
        name: "uploads",
        component: ModulePlaceholderView,
        props: {
          title: "Subir Archivos",
          description: "Area preparada para cargas clinicas y documentacion operativa.",
          moduleKey: "uploads",
        },
        meta: { title: "Subir archivos", roles: ["admin"] },
      },
      {
        path: "sistema/perfil",
        name: "perfil",
        component: PerfilView,
        meta: { title: "Perfil" },
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.meta.public) {
    if ((to.name === "login" || to.name === "register") && hasSession()) {
      next("/dashboard");
      return;
    }
    next();
    return;
  }

  if (!hasSession()) {
    next("/login");
    return;
  }

  const requiredRoles = to.meta.roles || [];
  const user = getStoredUser();

  if (requiredRoles.length && !requiredRoles.includes(user?.rol)) {
    next("/dashboard");
    return;
  }

  next();
});

export default router;
