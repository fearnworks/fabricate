<template>
    <div class="max-w-xs mx-auto" data-testid="image-card">
        <div class="bg-white rounded-lg border border-gray-200 shadow-md dark:bg-gray-800 dark:border-gray-700">
            <img class="rounded-t-lg object-cover h-512 w-full" :src="src" alt="Image" />
            <div class="p-5">
                <h5 class="text-gray-900 dark:text-white text-xl font-medium mb-2">{{ filename }}</h5>
                <div class="flex justify-between mt-4">
                    <button @click="emitDelete" data-testid="delete-button"
                        class="text-white bg-red-500 hover:bg-red-700 focus:ring-4 focus:ring-red-300 font-medium rounded-lg text-sm px-4 py-2 dark:bg-red-600 dark:hover:bg-red-700 focus:outline-none dark:focus:ring-red-800">Delete</button>
                    <button @click="moveImage"
                        class="text-white bg-blue-500 hover:bg-blue-700 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800">Move</button>
                </div>
            </div>
        </div>
    </div>
</template>
  
<script>
export default {
    props: {
        src: String,
        filename: String,
    },
    methods: {
    emitDelete() {
      this.$emit('delete', this.filename);
    },
        moveImage() {
            // Placeholder for move image logic
            console.log("Move image:", this.filename);
        },
    },
};
</script>
  
<style scoped>
/* Styles for ImageCard */
</style>
  