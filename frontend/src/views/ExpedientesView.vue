<template>

<div class="container">

<h2>Registrar Expediente</h2>

<form @submit.prevent="crearExpediente">

<select v-model="paciente">

<option disabled value="">Selecciona paciente</option>

<option
v-for="p in pacientes"
:key="p.id"
:value="p.id"
>

{{ p.nombre }} {{ p.apellido }}

</option>

</select>

<textarea
v-model="historial"
placeholder="Historial médico"
></textarea>

<button>Guardar</button>

</form>

<h2>Lista de Expedientes</h2>

<div class="lista">

<div
class="card"
v-for="e in expedientes"
:key="e.id"
>

<h3>Paciente {{ e.paciente }}</h3>

<p>{{ e.historial }}</p>

</div>

</div>

</div>

</template>


<script>

import api from "../services/api"

export default{

data(){

return{

expedientes:[],
pacientes:[],

paciente:"",
historial:""

}

},

mounted(){

this.cargarPacientes()
this.cargarExpedientes()

},

methods:{


async cargarPacientes(){

const res = await api.get("pacientes/")
this.pacientes = res.data

},

async cargarExpedientes(){

const res = await api.get("expedientes/")
this.expedientes = res.data

},

async crearExpediente(){

await api.post("expedientes/",{

paciente:this.paciente,
historial:this.historial

})

this.cargarExpedientes()

this.paciente=""
this.historial=""

}

}

}

</script>