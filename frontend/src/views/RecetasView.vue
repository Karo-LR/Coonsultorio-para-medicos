<template>

<div class="container">

<h2>Recetas Médicas</h2>

<form @submit.prevent="crearReceta">

<select v-model="consulta">
<option disabled value="">Selecciona consulta</option>

<option
v-for="c in consultas"
:key="c.id"
:value="c.id"
>
Consulta #{{ c.id }}
</option>

</select>

<input
v-model="medicamento"
placeholder="Medicamento"
/>

<input
v-model="dosis"
placeholder="Dosis"
/>

<textarea
v-model="indicaciones"
placeholder="Indicaciones"
></textarea>

<button>Generar receta</button>

</form>

</div>

</template>

<script>
import api from "../services/api"
export default {

data(){
return{
consultas:[],
consulta:"",
medicamento:"",
dosis:"",
indicaciones:""
}
},

mounted(){
this.cargarConsultas()
},

methods:{

async cargarConsultas(){

const token = localStorage.getItem("token")

const res = await axios.get(
"https://coonsultorio-para-medicos.onrender.com/api/consultas/",
{
headers:{
Authorization:`Bearer ${token}`
}
})

this.consultas = res.data

},

async crearReceta(){

const token = localStorage.getItem("token")

try{

await axios.post(
"https://coonsultorio-para-medicos.onrender.com/api/recetas/",
{
consulta:this.consulta,
medicamento:this.medicamento,
dosis:this.dosis,
indicaciones:this.indicaciones
},
{
headers:{
Authorization:`Bearer ${token}`
}
})

alert("Receta creada")

}catch(error){

console.log(error.response.data)
alert("Error al crear receta")

}

}

}

}
</script>