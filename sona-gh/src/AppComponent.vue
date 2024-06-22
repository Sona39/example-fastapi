<template>
  <div>
    <HeaderComponent />
    <router-view />
  </div>
</template>

<script>
import HeaderComponent from './components/HeaderComponent.vue';

export default {
  components: {
    HeaderComponent,
  },
};
</script>

<style>
/* Your styles here */
</style>