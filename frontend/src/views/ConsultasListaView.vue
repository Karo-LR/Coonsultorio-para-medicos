<template>
<div class="container">

<h1>Consultas Médicas</h1>

<table>
<thead>
<tr>
<th>ID</th>
<th>Cita</th>
<th>Diagnóstico</th>
<th>Tratamiento</th>
</tr>
</thead>

<tbody>
<tr v-for="consulta in consultas" :key="consulta.id">
<td>{{ consulta.id }}</td>
<td>{{ consulta.cita }}</td>
<td>{{ consulta.diagnostico }}</td>
<td>{{ consulta.tratamiento }}</td>
</tr>
</tbody>
</table>

</div>
</template>

<script>
import api from "@/services/api";

export default {
data(){
return{
consultas:[]
}
},

mounted(){
this.obtenerConsultas()
},

methods:{

async obtenerConsultas(){
try{

const res = await api.get("consultas/")
this.consultas = res.data

}catch(error){
console.error("Error consultas",error)
}

}

}
}
</script>