<template>
  <div class="page">

    <button @click="$router.back()">← Volver</button>

    <h1>Historial Clínico</h1>

    <!-- CONSULTAS -->
    <div class="section">
      <h2>Consultas</h2>

      <div v-if="consultas.length === 0">
        No hay consultas
      </div>

      <div v-for="c in consultas" :key="c.id" class="card">
        <p><strong>Fecha:</strong> {{ c.fecha }}</p>
        <p><strong>Diagnóstico:</strong> {{ c.diagnostico }}</p>
      </div>
    </div>

    <!-- CITAS -->
    <div class="section">
      <h2>Citas</h2>

      <div v-if="citas.length === 0">
        No hay citas
      </div>

      <div v-for="c in citas" :key="c.id" class="card">
        <p><strong>Fecha:</strong> {{ c.fecha }}</p>
        <p><strong>Motivo:</strong> {{ c.motivo }}</p>
      </div>
    </div>

  </div>
</template>

<script>
import api from "../../services/api"

export default{

data(){
return{
consultas:[],
citas:[]
}
},

mounted(){
this.cargarHistorial()
},

methods:{

async cargarHistorial(){

const id = this.$route.params.id

const consultas = await api.get(`consultas/?paciente=${id}`)
const citas = await api.get(`citas/?paciente=${id}`)

this.consultas = consultas.data
this.citas = citas.data

}

}
}
</script>

<style scoped>

.page{
padding:30px;
}

.section{
margin-top:30px;
}

.card{
background:white;
padding:15px;
margin-top:10px;
border-radius:10px;
box-shadow:0 3px 10px rgba(0,0,0,0.1);
}

</style>