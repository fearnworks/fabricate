<template>
    <div class="bg-gray-100 min-h-screen">
        <!-- Top Bar -->
        <div class="bg-white px-4 py-2 shadow-md">
            <div class="flex items-center justify-between max-w-7xl mx-auto">
                <h1 class="text-3xl font-bold text-blue-600">FABRICATE</h1>
                <div class="relative inline-block w-10 mr-2 align-middle select-none transition duration-200 ease-in">
                    <input type="checkbox" name="toggle" id="toggle" class="toggle-checkbox hidden"
                        @change="toggleViewMode" />
                    <label for="toggle"
                        class="toggle-label block overflow-hidden h-6 rounded-full bg-gray-300 cursor-pointer"></label>
                </div>
                <span class="text-gray-700" v-if="viewMode === 'grid'">
                    {{viewMode}}
                    <i aria-label="grid-toggle" class="fas fa-th"></i> <!-- Grid icon -->
                </span>
                <span class="text-gray-700" v-else>
                    <i  aria-label="carousel-toggle" class="fas fa-images"></i> <!-- Carousel icon -->
                </span>
            </div>
        </div>

        <!-- Search Bar -->
        <div class="max-w-7xl mx-auto px-4 py-6">
            <input type="search" placeholder="Want to search for something?" class="w-full p-4 border rounded shadow-sm">
        </div>

        <!-- Loading Placeholder -->
        <div v-if="isLoading">
            <p>Loading images...</p>
        </div>
        <!-- Conditional Rendering Based on View Mode -->
        <div v-else>
            <div v-if="isGridView" class="max-w-7xl mx-auto px-4 py-6">
                <!-- Grid Component Here -->
                Grid
                <ImageGrid :images="images" @delete-image="handleDelete" @update-image="handleUpdate" />
            </div>
            <div v-else>
                Carousel
                <ImageCarousel :images="images" @delete-image="handleDelete" />
            </div>
        </div>

        <!-- Pagination Controls -->
        <div class="max-w-7xl mx-auto px-4 py-6 flex justify-between items-center">
            <!-- Pagination Here -->
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, provide } from 'vue';
import ImageCarousel from './ImageCarousel.vue';
import ImageGrid from './ImageGrid.vue';
import ImageAPI from '../api/ImageAPI';
import {DBImageData } from '../types';
import useToast from '@/composables/useToast';

const toast = useToast();
const images = ref<DBImageData[] >([]);
const currentPage = ref(1);
const socket = ref<WebSocket | null>(null);
const isGridView = ref(true); // State for toggling between grid and carousel
const isLoading = ref(true);
const viewMode = computed(() => (isGridView.value ? 'grid' : 'carousel'));

const fetchImages = async () => {
    isLoading.value = true; 
    const api = new ImageAPI('http://server:28100');
    try {
        const fetchedImages = await api.fetchImages();
        images.value = fetchedImages;
        console.log('Fetched images:', fetchedImages);
        toast.showToast('Fetched images successfully');
        isLoading.value = false;  // Set isLoading to false after images are fetched
    } catch (error) {
        console.error('Error fetching images:', error);
        toast.showToast('Error fetching images');
        isLoading.value = false;  // Also set isLoading to false in case of error
    }
};

// WebSocket connection to get real-time updates
const connectWebSocket = () => {
    try {
        socket.value = new WebSocket('ws://server:28100/ws');
        socket.value.onmessage = (event: MessageEvent) => {
            const data = JSON.parse(event.data);
            if (Array.isArray(data.images)) {
                images.value = data.images;
                isLoading.value = false;
            } else {
                console.error('Received non-array images data:', data.images);
            }
        };
        socket.value.onerror = (error: Event) => {
            console.error(`WebSocket Error: ${error}`);
        };
    }
    catch (error) {
        console.error('Failed to connect to WebSocket:', error);
    }
};


// Provide handleUpdate method to children components
const handleUpdate = async (filename: string, updateData: DBImageData) => {
    const api = new ImageAPI('http://server:28100');
    console.log('Updating image:', filename, updateData);
    try {
        await api.updateImage(filename, updateData);
        toast.showToast('Image updated successfully');
        await fetchImages(); // Re-fetch images to update the list
    } catch (error) {
        console.error('Error updating image:', error);
        toast.showToast('Error updating image');
    }
};

const handleDelete = async (filename: string) => {
    const api = new ImageAPI('http://server:28100');
    try {
        await api.deleteImage(filename);
        images.value = images.value.filter((image) => image.filename !== filename);
        toast.showToast?.('Image deleted successfully');
    } catch (error: any) {
        console.error('Error deleting image:', error);
        toast.showToast?.('Error deleting image');
    }
};


onMounted(() => {
    fetchImages();
    connectWebSocket();
});

watch(currentPage, (newPage) => {
    console.log('Current page changed:', newPage);
});

const toggleViewMode = () => {
    isGridView.value = !isGridView.value;
};

provide('handleUpdate', handleUpdate);

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