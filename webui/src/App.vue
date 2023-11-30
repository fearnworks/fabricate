<template>
  <div id="app">
    <ToastComponent ref="toast" />
    <ImageReader /> <!-- Add the ImageReader component -->
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, provide } from 'vue';
import ImageReader from './components/ImageReader.vue' // Import ImageReader
import ToastComponent from './components/ToastComponent.vue' // Import ToastComponent
import { ToastMethods } from  './types'; // Import the type

export default defineComponent({
  name: 'App',
  components: {
    ImageReader,
    ToastComponent
  },
  setup() {
    const toast = ref<ToastMethods | null>(null);

    const showToast: ToastMethods['showToast'] = (message) => {
      toast.value?.showToast(message);
    };

    provide('showToast', showToast);

    return {
      toast
    };
  }
})
</script>


<style>
html,
body {
  margin: 0;
  padding: 0;
  overflow: hidden;
  /* Prevent scrolling on the entire body */
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  height: 100vh;
  /* Set the app height to the viewport height */
  display: flex;
  flex-direction: column;
}</style>
