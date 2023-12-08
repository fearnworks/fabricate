<template>
  <div>
    <div
      class="flex flex-row gap-4 p-8 bg-gray-900 rounded-3xl shadow-xl transition duration-300 ease-in-out hover:shadow-2xl w-full "
      data-testid="image-card">
      <!-- Image Container -->
      <div class="relative group w-1/2">
        <img :src="get_src(filename)" alt="Image" class="object-cover rounded-2xl w-full h-auto" />
        <button
          class="absolute inset-0 w-full h-full opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-black bg-opacity-50 flex items-center justify-center text-white text-xl"
          @click="showZoomed = true">
          Zoom
        </button>
      </div>

      <!-- Form Container -->
      <div class="space-y-6 w-1/2 ">
        <!-- Filename and Caption -->
        <div>
          <label class="block text-sm font-medium text-gray-400">Filename</label>
          <input type="text" v-model="editableFilename"
            class="form-input w-full text-xl font-semibold bg-transparent border-b-2 border-gray-500 focus:outline-none text-white"
            readonly />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-400">Caption</label>
          <textarea v-model="editableCaptions"
            class="form-textarea w-full h-24 bg-transparent border-b-2 border-gray-500 focus:outline-none text-white placeholder-gray-400 resize-none"></textarea>
        </div>
        <div>
          <!-- Notes -->
          <label class="block text-sm font-medium text-gray-400">Notes</label>
          <textarea v-model="editableNotes"
            class="form-textarea w-full h-24 bg-transparent border-b-2 border-gray-500 focus:outline-none text-white placeholder-gray-400 resize-none"></textarea>
        </div>
      </div>
    </div>
    <div>
      <!-- Action buttons -->
      <div class="flex justify-between mt-8 bg-gray-800 p-4 rounded-b-3xl">
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
  </div>

  <!-- Zoomed Image Modal -->
  <div v-if="showZoomed" class="fixed inset-0 bg-black bg-opacity-75 flex justify-center items-center p-4 z-50"
    @click.self="showZoomed = false">
    <div class="modal-content" @click.stop>
      <img :src="get_src(filename)" alt="Zoomed Image" class="max-w-full max-h-full" style="transform: scale(1);" />
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
const showZoomed = ref(false);


const zoomLevel = ref(1); // 1 is the initial zoom level (100%)

const zoomIn = () => {
  zoomLevel.value *= 1.2; // Increase zoom by 20%
};

const zoomOut = () => {
  zoomLevel.value = Math.max(1, zoomLevel.value / 1.2); // Decrease zoom by 20%, but not less than 100%
};

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

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  max-width: 90vw;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-content img {
  width: 100%;
  height: auto;
  border-radius: 8px;
}
</style>
