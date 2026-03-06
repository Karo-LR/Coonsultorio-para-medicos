<template>

<div class="container">

<h2>Registrar Consulta</h2>

<form @submit.prevent="crearConsulta">

<select v-model="paciente">

<option disabled value="">Seleccionar paciente</option>

<option
v-for="p in pacientes"
:key="p.id"
:value="p.id"
>

{{ p.nombre }} {{ p.apellido }}

</option>

</select>

<textarea
v-model="diagnostico"
placeholder="Diagnóstico"
></textarea>

<textarea
v-model="tratamiento"
placeholder="Tratamiento"
></textarea>

<button>Guardar</button>

</form>

<h2>Lista de Consultas</h2>

<div class="lista">

<div
class="card"
v-for="c in consultas"
:key="c.id"
>

<h3>Paciente ID: {{ c.paciente }}</h3>

<p>
<strong>Diagnóstico:</strong>
{{ c.diagnostico }}
</p>

<p>
<strong>Tratamiento:</strong>
{{ c.tratamiento }}
</p>

</div>

</div>

</div>

</template>


<script>

import api from "../services/api"

export default{

data(){

return{

consultas:[],
pacientes:[],

paciente:"",
diagnostico:"",
tratamiento:""

}

},

mounted(){

this.cargarPacientes()
this.cargarConsultas()

},

methods:{


async cargarPacientes(){

const res = await api.get("pacientes/")
this.pacientes = res.data

},

async cargarConsultas(){

const res = await api.get("consultas/")
this.consultas = res.data

},

async crearConsulta(){

await api.post("consultas/",{

paciente:this.paciente,
diagnostico:this.diagnostico,
tratamiento:this.tratamiento

})

this.cargarConsultas()

this.paciente=""
this.diagnostico=""
this.tratamiento=""

}

}

}

</script>