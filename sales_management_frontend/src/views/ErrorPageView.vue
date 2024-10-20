<template>
  <div>
    <h1>An error occurred!</h1>
    <p>
      Something went wrong while processing your request. Please try again
      later.
    </p>
    <router-link to="/">Go back to the dashboard</router-link>
  </div>
</template>

<script>
export default {
  name: "ErrorPageView",
};
</script>

<style scoped>
h1 {
  color: red;
}
</style>
