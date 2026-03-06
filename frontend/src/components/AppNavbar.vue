<template>

<header class="navbar">

<div class="logo">
🏥 Consultorio Médico
</div>

<nav class="menu">

<router-link to="/pacientes">Pacientes</router-link>

<router-link to="/citas">Citas</router-link>

<router-link to="/consultas">Consultas</router-link>

<router-link to="/recetas">Recetas</router-link>

<router-link to="/expedientes">Expedientes</router-link>

</nav>

<button class="logout" @click="logout">
Cerrar sesión
</button>

</header>

</template>

<script>

export default {

methods:{

logout(){

localStorage.removeItem("token")

this.$router.push("/login")

}

}

}

</script>

<style>

.navbar{
display:flex;
align-items:center;
justify-content:space-between;
background:#2c3e50;
padding:12px 40px;
color:white;
}

.logo{
font-size:20px;
font-weight:bold;
}

.menu{
display:flex;
gap:25px;
}

.menu a{
color:white;
text-decoration:none;
font-weight:500;
}

.menu a:hover{
color:#3498db;
}

.logout{

font-size:13px;
padding:5px 12px;
background:#e74c3c;
border:none;
border-radius:6px;
color:white;
cursor:pointer;

}

.logout:hover{
background:#c0392b;
}

</style>