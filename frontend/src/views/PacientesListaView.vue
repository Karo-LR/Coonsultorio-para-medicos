<template>

<div class="container">

<h2>Pacientes Registrados</h2>

<table>

<thead>

<tr>
<th>Nombre</th>
<th>Apellido</th>
<th>Teléfono</th>
</tr>

</thead>

<tbody>

<tr v-for="p in pacientes" :key="p.id">

<td>{{ p.nombre }}</td>

<td>{{ p.apellido }}</td>

<td>{{ p.telefono }}</td>

</tr>

</tbody>

</table>

</div>

</template>

<script>

import api from "../services/api"

export default{

data(){
return{
pacientes:[]
}
},

mounted(){
this.cargarPacientes()
},

methods:{

async cargarPacientes(){

const res = await api.get("pacientes/")
this.pacientes = res.data

}

}

}

</script>