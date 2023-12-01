<template>
  <div id="app" >
    <ToastComponent />
    <ImageReader class="bg-slate-600"/>
  </div>
</template>

<script lang="ts">
import { defineComponent, provide } from 'vue';
import ImageReader from './components/ImageReader.vue';
import ToastComponent from './components/ToastComponent.vue';
import useToast from '@/composables/useToast'; 

export default defineComponent({
  name: 'App',
  components: {
    ImageReader,
    ToastComponent
  },
  setup() {
    const { showToast } = useToast();

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
