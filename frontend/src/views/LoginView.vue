<template>
  <div class="login-container">

    <div class="login-card">

      <h1 class="title">Consultorio Médico</h1>
      <p class="subtitle">Sistema de Gestión Clínica</p>

      <form @submit.prevent="login">

        <input
          v-model="username"
          type="text"
          placeholder="Usuario"
          required
        />

        <input
          v-model="password"
          type="password"
          placeholder="Contraseña"
          required
        />

        <button type="submit">
          Ingresar
        </button>

      </form>

      <p v-if="error" class="error">
        Usuario o contraseña incorrectos
      </p>

    </div>

  </div>
</template>

<script>
import axios from "axios"

export default {

  data(){
    return{
      username:"",
      password:"",
      error:false
    }
  },

  methods:{

    async login(){

      try{

        const response = await axios.post(
          "https://coonsultorio-para-medicos.onrender.com/api/token/",
          {
            username:this.username,
            password:this.password
          }
        )

        localStorage.setItem("token",response.data.access)

        this.$router.push("/dashboard")

      }catch{

        this.error=true

      }

    }

  }

}
</script>

<style>

.login-container{
  height:100vh;
  display:flex;
  justify-content:center;
  align-items:center;
  background:linear-gradient(135deg,#4facfe,#00f2fe);
}

.login-card{
  background:white;
  padding:40px;
  border-radius:12px;
  width:320px;
  box-shadow:0 10px 25px rgba(0,0,0,0.2);
  text-align:center;
}

.title{
  margin-bottom:5px;
}

.subtitle{
  margin-bottom:20px;
  color:#777;
}

input{
  width:100%;
  padding:10px;
  margin-bottom:15px;
  border-radius:6px;
  border:1px solid #ccc;
}

button{
  width:100%;
  padding:10px;
  border:none;
  border-radius:6px;
  background:#2d8cf0;
  color:white;
  font-weight:bold;
  cursor:pointer;
}

button:hover{
  background:#1c6ed5;
}

.error{
  color:red;
  margin-top:10px;
}

</style>