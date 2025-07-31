<template>
  <div id="app" class="d-flex flex-column h-100">
    <router-view />
  </div>
</template>

<script>
  export default {
    name: "App",
  };
</script>

<style>
  html,body, #app {
    margin: 0;
    padding: 0;
    height: 100%;
    overflow: hidden;
  }

  #app {
    display: flex;
    flex-direction: column;
  }
</style>
