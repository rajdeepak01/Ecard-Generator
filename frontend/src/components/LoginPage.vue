<script>
import axios from 'axios'
export default {
    data() {
        return {
            formData: {
                username: "",
                password: ""
            },
            token:""
        }
    },
    methods:{
        loginUser(){
            const response = axios.post(
                "http://127.0.0.1:5000/api/login",
             this.formData,{
              headers : {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Authorization" : `Bearer ${localStorage.getItem("token")}`
            },
            });
            response
            .then(res => {
                if(res.status == 200) {
                    this.token = res.data.access_tocken
                    localStorage.setItem("token", res.data.access_tocken)
                    console.log(res.data);
                    
                } else{
                    console.log(res.response.data);
                    
                }
            })
        },
        logoutUser() {
            localStorage.clear();
        }
    }
}

</script>

<template>
    <div id="main">
        <div id="canvas">
            <div id="form-body">
                <h1>Login Form</h1>
                <form @submit.prevent="loginUser">
                    <div class="mb-3">
                        <label for="Input1" class="form-label">Username</label>
                        <input type="text" class="form-control" id="Input1" placeholder="shiv123" v-model="formData.username">
                    </div>
                    <div class="mb-3">
                        <label for="Input2" class="form-label">Password</label>
                        <input type="password" class="form-control" id="Input2" placeholder="********" v-model="formData.password">
                    </div>
                    <div style="text-align: center;">
                        <input type="submit" class="btn btn-primary" value="Login">
                        <!-- <button @click="loginUser" class="btn-btn-primary">Login</button> -->
                    </div>
                    <div style="text-align: center;">
                        Are you a user? <a href="/register">Register</a>
                    </div>
                    <button @click="logoutUser" class="btn-btn-danger">Logout</button>
                </form>
            </div>

        </div>
    </div>
</template>

<style>
</style>