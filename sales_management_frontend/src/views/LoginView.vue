<template>
  <div>
    <h1>Login</h1>
    <form @submit.prevent="handleLogin">
      <input type="text" v-model="username" placeholder="Username" />
      <input type="password" v-model="password" placeholder="Password" />
      <button type="submit">Login</button>
    </form>
  </div>
</template>
<script>
import axios from "../plugins/axios";

export default {
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    async handleLogin() {
      try {
        await axios.post("login/", {
          username: this.username,
          password: this.password,
        });
        // Save token or perform other actions
        this.$router.push("/dashboard");
      } catch (error) {
        console.error(error);
        this.$router.push("/error");
      }
    },
  },
};
</script>
