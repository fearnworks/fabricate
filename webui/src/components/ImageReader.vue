// src/components/ImageReader.vue

<template>
    <div class="bg-gray-100 min-h-screen">
        <!-- Top Bar -->
        <div class="bg-white px-4 py-2 shadow-md">
            <div class="flex items-center justify-between max-w-7xl mx-auto">
                <h1 class="text-3xl font-bold text-blue-600">FABRICATE</h1>
                <button class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-700 transition">Upload media</button>
            </div>
        </div>

        <!-- Search Bar -->
        <div class="max-w-7xl mx-auto px-4 py-6">
            <input type="search" placeholder="Want to search for something?" class="w-full p-4 border rounded shadow-sm">
        </div>

        <div v-if="images.length > 0">
            <ImageCarousel :images="images" @delete-image="handleDelete" />

        </div>
        <div v-else>
            <p>Loading images...</p>
        </div>
        <!-- Pagination Controls -->
        <div class="max-w-7xl mx-auto px-4 py-6 flex justify-between items-center">
        </div>
    </div>
</template>
  
<script lang="ts">
import { defineComponent, ref, computed, onMounted, watch, inject, provide } from 'vue';
import ImageCarousel from './ImageCarousel.vue';
import ImageAPI from '../api/ImageAPI';
import { ToastMethods, Image } from '../types';

export default defineComponent({
    name: 'ImageReader',
    components: {
        ImageCarousel
    },
    setup(_, {}) {
        const images = ref<Image[]>([]);
        const currentPage = ref(1);
        const imagesPerPage = ref(10);
        const socket = ref<WebSocket | null>(null);
        const showToast = inject<ToastMethods>('showToast')!;

        const totalPages = computed(() => Math.ceil(images.value.length / imagesPerPage.value));


        // Fetch images from the server
        const fetchImages = async () => {
            const api = new ImageAPI('http://localhost:8000');
            try {
                const fetchedImages = await api.fetchImages();
                images.value = fetchedImages;
                showToast('Fetched images successfully');
            } catch (error) {
                console.error('Error fetching images:', error);
                showToast('Error fetching images');
            }
        };

        // WebSocket connection to get real-time updates
        const connectWebSocket = () => {
            socket.value = new WebSocket('ws://localhost:8000/ws');
            socket.value.onmessage = (event: MessageEvent) => {
                const data = JSON.parse(event.data);
                if (Array.isArray(data.images)) {
                    images.value = data.images;
                } else {
                    console.error('Received non-array images data:', data.images);
                }
            };
            socket.value.onerror = (error: Event) => {
                console.error(`WebSocket Error: ${error}`);
            };
        };

        // Provide handleUpdate method to children components
        const handleUpdate = async (filename: string, updateData: Image) => {
            const api = new ImageAPI('http://localhost:8000');
            console.log('Updating image:', filename, updateData);
            try {
                await api.updateImage(filename, updateData);
                showToast('Image updated successfully');
                await fetchImages(); // Re-fetch images to update the list
            } catch (error) {
                console.error('Error updating image:', error);
                showToast('Error updating image');
            }
        };

        const handleDelete = async (filename: string) => {
            const api = new ImageAPI('http://localhost:8000');
            try {
                await api.deleteImage(filename);
                images.value = images.value.filter((image) => image.filename !== filename);
                showToast?.('Image deleted successfully');
            } catch (error: any) {
                console.error('Error deleting image:', error);
                showToast?.('Error deleting image');
            }
        };
        onMounted(() => {
            fetchImages();
            connectWebSocket();
        });

        watch(currentPage, (newPage) => {
            console.log('Current page changed:', newPage);
        });

        provide('showToast', showToast);
        provide('handleUpdate', handleUpdate);

        // Export reactive data and methods for the template
        return {
            images,
            currentPage,
            totalPages,
            handleUpdate,
            handleDelete,
            fetchImages,
            connectWebSocket,
        };
    },
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