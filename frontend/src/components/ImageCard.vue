<template>
    <div class="flex flex-col p-8 bg-white rounded-2xl shadow-2xl max-w mx-auto" data-testid="image-card">
      <div class="flex flex-row mb-8">
        <!-- Image display -->
        <div class="flex-none w-96 h-96 bg-gray-200 text-gray-700 p-8 rounded-2xl mr-8">
          <img :src="get_src(filename)" alt="Image" class="object-cover rounded-2xl" />
        </div>
        <!-- Filename and Caption -->
        <div class="flex-grow space-y-8">
          <input type="text" v-model="editableFilename" class="w-full text-2xl font-medium bg-transparent border-b-4 border-gray-300 focus:outline-none" readonly />
          <textarea v-model="editableCaptions" placeholder="Caption" class="w-full text-xl bg-transparent border-b-4 border-gray-300 focus:outline-none"></textarea>
        </div>
      </div>
      <!-- Other fields -->
      <textarea v-model="editableNotes" placeholder="Notes" class="w-full mb-8 text-xl bg-transparent border-b-4 border-gray-300 focus:outline-none"></textarea>
      <!-- Action buttons -->
      <div class="flex justify-between mt-8">
        <button @click="emitUpdate" class="px-8 py-4 text-2xl text-white bg-blue-500 rounded-2xl hover:bg-blue-700 focus:outline-none">
          Update
        </button>
        <button @click="moveImage" class="px-8 py-4 text-2xl text-white bg-yellow-500 rounded-2xl hover:bg-yellow-700 focus:outline-none">
          Move
        </button>
        <button @click="emitDelete" data-testid="delete-button" class="px-8 py-4 text-2xl text-white bg-red-500 rounded-2xl hover:bg-red-700 focus:outline-none">
          Delete
        </button>
      </div>
    </div>
</template>
  
  <script lang="ts">
  import { defineComponent, PropType } from 'vue';
  
  export default defineComponent({
    props: {
      filename: String,
      tags: Array as PropType<string[]>,
      notes: String,
      captions: String,
    },
    data() {
      return {
        editableFilename: this.filename,
        editableNotes: this.notes,
        editableCaptions: this.captions,
      };
    },
    methods: {
      get_src(filename: string): string {
        // Assuming there is a method defined elsewhere to get the source URL
        return `http://localhost:8000/static/${filename}`;
      },
      emitUpdate() {
        // Logic to emit an update event
        this.$emit('update', {
          filename: this.editableFilename,
          notes: this.editableNotes,
          captions: this.editableCaptions,
        });
      },
      emitDelete() {
        // Logic to emit a delete event
        this.$emit('delete', this.filename);
      },
      moveImage() {
        // Logic to emit a move event or handle moving
        console.log('Move image:', this.filename);
      },
    },
    watch: {
      filename(newVal: string) {
        this.editableFilename = newVal;
      },
      notes(newVal: string) {
        this.editableNotes = newVal;
      },
      captions(newVal: string) {
        this.editableCaptions = newVal;
      },
    },
  });
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
