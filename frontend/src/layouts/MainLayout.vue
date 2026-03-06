<template>

<div class="layout">

<aside class="sidebar">

<h2>Consultorio</h2>

<router-link to="/dashboard">Dashboard</router-link>
<router-link to="/pacientes">Pacientes</router-link>
<router-link to="/citas">Citas</router-link>
<router-link to="/expedientes">Expedientes</router-link>
<router-link to="/consultas">Consultas</router-link>

</aside>

<main class="content">
<router-view/>
</main>

</div>

</template>

<style>

.layout{
display:flex;
height:100vh;
}

.sidebar{
width:200px;
background:#2d8cf0;
color:white;
padding:20px;
display:flex;
flex-direction:column;
gap:15px;
}

.sidebar a{
color:white;
text-decoration:none;
}

.content{
flex:1;
padding:20px;
background:#f5f7fb;
}

</style>