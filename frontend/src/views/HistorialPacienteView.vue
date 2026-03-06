<template>

<div class="container">

<h2>Historial del Paciente</h2>

<select v-model="pacienteId" @change="cargarHistorial">

<option disabled value="">Selecciona paciente</option>

<option
v-for="p in pacientes"
:key="p.id"
:value="p.id"
>
{{ p.nombre }} {{ p.apellido }}
</option>

</select>

<div v-if="historial">

<h3>Expediente</h3>
<p><b>Alergias:</b> {{ historial.expediente?.alergias }}</p>
<p><b>Enfermedades:</b> {{ historial.expediente?.enfermedades_cronicas }}</p>

<h3>Citas</h3>
<ul>
<li v-for="c in historial.citas" :key="c.id">
{{ c.fecha }} - {{ c.motivo }}
</li>
</ul>

<h3>Consultas</h3>
<ul>
<li v-for="c in historial.consultas" :key="c.id">
Diagnóstico: {{ c.diagnostico }}
</li>
</ul>

<h3>Recetas</h3>
<ul>
<li v-for="r in historial.recetas" :key="r.id">
{{ r.medicamento }} - {{ r.dosis }}
</li>
</ul>

</div>

</div>

</template>

<script>
import api from "../services/api"
export default {

data(){
return{
pacientes:[],
pacienteId:"",
historial:null
}
},

mounted(){
this.cargarPacientes()
},

methods:{

async cargarPacientes(){

const token = localStorage.getItem("token")

const res = await axios.get(
"https://coonsultorio-para-medicos.onrender.com/api/pacientes/",
{
headers:{ Authorization:`Bearer ${token}` }
})

this.pacientes = res.data

},

async cargarHistorial(){

const token = localStorage.getItem("token")

const res = await axios.get(
`https://coonsultorio-para-medicos.onrender.com/api/historial/${this.pacienteId}/`,
{
headers:{ Authorization:`Bearer ${token}` }
})

this.historial = res.data

}

}

}
</script>