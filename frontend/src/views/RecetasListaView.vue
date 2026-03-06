<template>

<div class="container">

<h1>Recetas Médicas</h1>

<table>

<thead>

<tr>
<th>ID</th>
<th>Consulta</th>
<th>Medicamento</th>
<th>Dosis</th>
<th>Indicaciones</th>
</tr>

</thead>

<tbody>

<tr v-for="receta in recetas" :key="receta.id">

<td>{{ receta.id }}</td>
<td>{{ receta.consulta }}</td>
<td>{{ receta.medicamento }}</td>
<td>{{ receta.dosis }}</td>
<td>{{ receta.indicaciones }}</td>

</tr>

</tbody>

</table>

</div>

</template>

<script>
import api from "@/services/api"

export default{

data(){
return{
recetas:[]
}
},

mounted(){
this.obtenerRecetas()
},

methods:{

async obtenerRecetas(){

try{

const res = await api.get("recetas/")
this.recetas = res.data

}catch(error){

console.error("Error recetas",error)

}

}

}

}
</script>