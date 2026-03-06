<template>

<div class="container">

<h2>Lista de Expedientes</h2>

<div class="lista">

<div
class="card"
v-for="e in expedientes"
:key="e.id"
>

<h3>Paciente ID: {{ e.paciente }}</h3>

<p>
<strong>Alergias:</strong> {{ e.alergias }}
</p>

<p>
<strong>Enfermedades:</strong> {{ e.enfermedades_cronicas }}
</p>

</div>

</div>

</div>

</template>

<script>

import api from "../services/api"

export default {

name:"ExpedientesListaView",

data(){

return{

expedientes:[]

}

},

mounted(){

this.obtenerExpedientes()

},

methods:{

async obtenerExpedientes(){

try{

const res = await api.get("expedientes/")

this.expedientes = res.data

}catch(error){

console.log(error)

}

}

}

}

</script>

<style scoped>

.container{
max-width:900px;
margin:auto;
padding:20px;
}

.lista{
display:grid;
grid-template-columns:repeat(auto-fill,minmax(250px,1fr));
gap:20px;
margin-top:20px;
}

.card{
background:white;
padding:20px;
border-radius:10px;
box-shadow:0 4px 10px rgba(0,0,0,0.1);
}

</style>