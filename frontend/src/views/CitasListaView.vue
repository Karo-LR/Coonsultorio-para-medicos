<template>

<div class="container">

<h2>Lista de Citas</h2>

<div class="lista">

<div
class="card"
v-for="c in citas"
:key="c.id"
>

<h3>{{ c.paciente_nombre }}</h3>

<p>
<strong>Fecha:</strong> {{ c.fecha }}
</p>

<p>
<strong>Motivo:</strong> {{ c.motivo }}
</p>

</div>

</div>

</div>

</template>

<script>

import api from "../services/api"

export default {

name:"CitasListaView",

data(){
return{
citas:[]
}
},

mounted(){
this.cargarCitas()
},

methods:{

async cargarCitas(){

try{

const res = await api.get("citas/")

this.citas = res.data

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