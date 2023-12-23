<template>
    <div>
        <!-- Search Bar -->
        <div class="max-w-7xl mx-auto px-4 py-6">
            <input type="search" placeholder="Want to search for something?" class="w-full p-4 border rounded shadow-sm">
        </div>
        <!-- Conditional Rendering Based on View Mode -->
        <div>
            <div class="max-w-8xl mx-auto px-4 py-6">
                <!-- Grid Component Here -->
                <ImageGrid :images="imageStore.images" @delete-image="imageStore.handleDelete" @update-image="imageStore.handleUpdate" />
            </div>
        </div>
    </div>
</template>


<script setup lang="ts">
import { onMounted } from 'vue';
import ImageGrid from './ImageGrid.vue';
import { useImageStore } from '@/stores/image_store';

const imageStore = useImageStore();

onMounted(async () => {
    await imageStore.fetchImages();
    // connectWebSocket(); // Uncomment this if you need WebSocket connection
});
</script>

<style scoped>
/* Add this to hide the scrollbar */
.scrollbar-hidden::-webkit-scrollbar {
    display: none;
}

.scrollbar-hidden {
    -ms-overflow-style: none;
    scrollbar-width: none;
}
</style>