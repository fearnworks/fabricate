<template>
    <div class="flex flex-col p-8 bg-gray-900 rounded-3xl shadow-xl max-w mx-auto transition duration-300 ease-in-out transform hover:shadow-2xl" data-testid="image-card">
      <div class="flex flex-row mb-8">
        <div class="flex-none w-96 h-96 bg-black p-4 rounded-3xl mr-8">
          <img :src="get_src(filename)" alt="Image" class="object-cover rounded-2xl" />
        </div>
        <div class="flex-grow space-y-6">
          <input type="text" v-model="editableFilename"
            class="form-input w-full text-2xl font-semibold bg-transparent border-b-2 border-gray-500 focus:outline-none text-white" />
          <textarea v-model="editableCaptions"
            class="form-textarea w-full bg-transparent border-b-2 border-gray-500 focus:outline-none text-white placeholder-gray-400"></textarea>
        </div>
      </div>
      <textarea v-model="editableNotes"
        class="form-textarea w-full mb-8 bg-transparent border-b-2 border-gray-500 focus:outline-none text-white placeholder-gray-400"></textarea>
      <div class="flex justify-between mt-4 bg-gray-800 p-4 rounded-b-3xl">
        <button @click="emitUpdate"
          class="px-6 py-3 text-lg bg-slate-700 rounded-lg hover:bg-blue-800 focus:outline-none text-white transition duration-300">
          Update
        </button>
        <button @click="moveImage"
          class="px-6 py-3 text-lg bg-slate-600 rounded-lg hover:bg-yellow-700 focus:outline-none text-white transition duration-300">
          Move
        </button>
        <button @click="emitDelete" data-testid="delete-button"
          class="px-6 py-3 text-lg bg-red-900 rounded-lg hover:bg-red-800 focus:outline-none text-white transition duration-300">
          Delete
        </button>
      </div>
    </div>
  </template>
  
  
  
  <script setup lang="ts">
  import { ref, watch, inject } from 'vue';
  import type { Image } from '@/types'; // Assuming Image type is defined in types.ts
  
  const props = defineProps({
    filename: String,
    tags: Array,
    notes: String,
    captions: String
  });
  
  const emit = defineEmits(['update', 'delete']);
  
  const handleUpdate = inject('handleUpdate') as (filename: string, data: any) => void;
  
  const editableFilename = ref(props.filename);
  const editableNotes = ref(props.notes);
  const editableCaptions = ref(props.captions);
  
  watch(() => props.filename, (newVal) => editableFilename.value = newVal);
  watch(() => props.notes, (newVal) => editableNotes.value = newVal);
  watch(() => props.captions, (newVal) => editableCaptions.value = newVal);
  
  const emitUpdate = () => {
    handleUpdate(editableFilename.value, {
      filename: editableFilename.value,
      notes: editableNotes.value,
      captions: editableCaptions.value,
      tags: props.tags
    });
  };
  
  const emitDelete = () => emit('delete', props.filename);
  
  const moveImage = () => console.log('Move image:', props.filename);
  
  const get_src = (filename: string) => `http://localhost:8000/static/${filename}`;
  </script>
  

<style scoped>
/* Styles for ImageCard */
.tags {
    /* Styles for tags */
}

.tag {
    /* Individual tag styles */
}
</style>
