<template>

<div class="container">

<h2>Registrar Cita</h2>

<form @submit.prevent="crearCita">

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

<input
type="datetime-local"
v-model="fecha"
/>

<input
v-model="motivo"
placeholder="Motivo de la cita"
/>

<button>Guardar</button>

</form>

<h2>Lista de Citas</h2>

<div class="lista">

<div
class="card"
v-for="c in citas"
:key="c.id"
>

<h3>Paciente {{ c.paciente }}</h3>

<p>
<strong>Fecha:</strong>
{{ c.fecha }}
</p>

<p>
<strong>Motivo:</strong>
{{ c.motivo }}
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

citas:[],
pacientes:[],

paciente:"",
fecha:"",
motivo:""

}

},

mounted(){

this.cargarPacientes()
this.cargarCitas()

},

methods:{


async cargarPacientes(){

const res = await api.get("pacientes/")
this.pacientes = res.data

},

async cargarCitas(){

const res = await api.get("citas/")
this.citas = res.data

},

async crearCita(){

await api.post("citas/",{

paciente:this.paciente,
fecha:this.fecha,
motivo:this.motivo

})

this.cargarCitas()

this.paciente=""
this.fecha=""
this.motivo=""

}

}

}

</script>