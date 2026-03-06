<template>

<div class="dashboard">

<!-- SIDEBAR -->

<aside class="sidebar">

<h2 class="logo">MedSystem</h2>

<nav>

<router-link to="/dashboard">
<Home size="20"/> Dashboard
</router-link>

<router-link to="/pacientes">
<Users size="20"/> Pacientes
</router-link>

<router-link to="/citas">
<Calendar size="20"/> Citas
</router-link>

<router-link to="/consultas">
<Stethoscope size="20"/> Consultas
</router-link>

<router-link to="/expedientes">
<FileText size="20"/> Expedientes
</router-link>

</nav>

<button class="logout" @click="logout">

<LogOut size="18"/> Cerrar sesión

</button>

</aside>

<!-- CONTENIDO -->

<main class="content">

<h1>Panel del Consultorio</h1>

<div class="cards">

<div class="card">

<Users size="40"/>

<h3>Pacientes</h3>

<p>{{ pacientes }}</p>

</div>

<div class="card">

<Calendar size="40"/>

<h3>Citas</h3>

<p>{{ citas }}</p>

</div>

<div class="card">

<Stethoscope size="40"/>

<h3>Consultas</h3>

<p>{{ consultas }}</p>

</div>

<div class="card">

<FileText size="40"/>

<h3>Expedientes</h3>

<p>{{ expedientes }}</p>

</div>

</div>

</main>

</div>

</template>

<script>

import api from "../services/api"

import {
Home,
Users,
Calendar,
Stethoscope,
FileText,
LogOut
} from "lucide-vue-next"

export default{

components:{
Home,
Users,
Calendar,
Stethoscope,
FileText,
LogOut
},

data(){

return{

pacientes:0,
citas:0,
consultas:0,
expedientes:0

}

},

mounted(){

this.cargarDatos()

},

methods:{


async cargarDatos(){

try{

const p = await api.get("pacientes/")
const c = await api.get("citas/")
const co = await api.get("consultas/")
const e = await api.get("expedientes/")

this.pacientes = p.data.length
this.citas = c.data.length
this.consultas = co.data.length
this.expedientes = e.data.length

}catch(error){

console.log(error)

}

},

logout(){

localStorage.removeItem("token")
this.$router.push("/")

}

}

}

</script>

<style>

.dashboard{
display:flex;
height:100vh;
background:#f4f6f9;
}

/* SIDEBAR */

.sidebar{
width:250px;
background:#1e293b;
color:white;
padding:20px;
display:flex;
flex-direction:column;
justify-content:space-between;
}

.logo{
text-align:center;
margin-bottom:30px;
}

.sidebar nav{
display:flex;
flex-direction:column;
gap:15px;
}

.sidebar a{
color:white;
text-decoration:none;
display:flex;
align-items:center;
gap:10px;
padding:10px;
border-radius:6px;
}

.sidebar a:hover{
background:#334155;
}

.logout{
background:#ef4444;
border:none;
padding:10px;
color:white;
cursor:pointer;
border-radius:6px;
display:flex;
align-items:center;
gap:10px;
}

/* CONTENT */

.content{
flex:1;
padding:40px;
}

.cards{
display:grid;
grid-template-columns:repeat(4,1fr);
gap:20px;
margin-top:30px;
}

.card{
background:white;
padding:30px;
border-radius:10px;
text-align:center;
box-shadow:0 4px 10px rgba(0,0,0,0.1);
}

.card h3{
margin-top:10px;
}

.card p{
font-size:30px;
font-weight:bold;
}

</style>