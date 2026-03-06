import { createRouter, createWebHistory } from 'vue-router'

import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import PacientesView from '../views/PacientesView.vue'
import CitasView from '../views/CitasView.vue'
import ExpedientesView from '../views/ExpedientesView.vue'
import ConsultasView from '../views/ConsultasView.vue'

const routes = [

{
path:'/',
component:LoginView
},

{
path:'/dashboard',
component:DashboardView
},

{
path:'/pacientes',
component:PacientesView
},

{
path:'/citas',
component:CitasView
},

{
path:'/consultas',
component:ConsultasView
},

{
path:'/expedientes',
component:ExpedientesView
}

]

const router = createRouter({

history:createWebHistory(),
routes

})

export default router