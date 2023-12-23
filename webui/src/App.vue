<template>
  <div id="app" >
    <ToastComponent />

    <Layout/>
  </div>
</template>

<script lang="ts">
import { defineComponent, provide } from 'vue';
import { useImageStore } from './stores/image_store';
import ToastComponent from './components/ToastComponent.vue';
import useToast from '@/composables/useToast'; 
import Layout from '@/components/Layout.vue';
export default defineComponent({
  name: 'App',
  components: {
    Layout,
    ToastComponent
  },
  setup() {
    const { showToast } = useToast();
    const image_store = useImageStore()
    console.log(image_store)
    // Provide the showToast method to all child components
    provide('showToast', showToast);
  }
});
</script>

<style>
/* Keep global styles if necessary, but consider scoping them */
html, body {
  margin: 0;
  padding: 0;
  overflow: hidden;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>
