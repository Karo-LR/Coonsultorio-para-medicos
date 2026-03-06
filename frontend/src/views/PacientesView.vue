<template>

<div class="container">

<h2>Registrar Paciente</h2>

<form @submit.prevent="crearPaciente">

<input v-model="nombre" placeholder="Nombre">
<input v-model="apellido" placeholder="Apellido">
<input v-model="telefono" placeholder="Telefono">
<input v-model="direccion" placeholder="Direccion">
<input type="date" v-model="fecha">

<button>Guardar</button>

</form>

<h2>Lista de Pacientes</h2>

<div class="lista">

<div class="card"
v-for="p in pacientes"
:key="p.id">

<h3>{{ p.nombre }} {{ p.apellido }}</h3>
<p>{{ p.telefono }}</p>

</div>

</div>

</div>

</template>

<script>

import api from "../services/api"

export default{

data(){

return{

pacientes:[],
nombre:"",
apellido:"",
telefono:"",
direccion:"",
fecha:""

}

},

mounted(){
this.cargarPacientes()
},

methods:{

async cargarPacientes(){

const res = await api.get("pacientes/")
this.pacientes = res.data

},

async crearPaciente(){

await api.post("pacientes/",{

nombre:this.nombre,
apellido:this.apellido,
telefono:this.telefono,
direccion:this.direccion,
fecha_nacimiento:this.fecha

})

this.cargarPacientes()

}

}

}

</script>