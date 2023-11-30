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
            <ImageCarousel :imageUrls="imageUrls" @delete-image="handleDelete" />

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
import { defineComponent } from 'vue';
import ImageCarousel from './ImageCarousel.vue' // Import ImageCarousel
import ImageAPI from '@/api/ImageAPI'; // Import the API handler
import { ToastMethods } from '@/types';

export default defineComponent({
    inject: {
        showToast: 'showToast' as keyof ToastMethods
    },
    name: 'ImageReader',
    components: {
        ImageCarousel // Register ImageCarousel
    },
    data() {
        return {
            images: [], // This will be populated via WebSocket
            currentPage: 1,
            imagesPerPage: 10,
            socket: null as WebSocket | null,
        };
    },
    mounted() {
        this.connectWebSocket();
    },
    computed: {
        paginatedImages() {
            let start = (this.currentPage - 1) * this.imagesPerPage;
            let end = this.currentPage * this.imagesPerPage;
            return this.images.slice(start, end);
        },
        totalPages() {
            return Math.ceil(this.images.length / this.imagesPerPage);
        },
        imageUrls() {
            return this.images.map(filename => `http://localhost:8000/static/${filename}`);
        },
    },
    methods: {
        getImageUrl(filename: string) {
            console.log('Getting image URL for:', filename)
            // Directly use the filename to construct the URL
            const url = `http://localhost:8000/static/${filename}`;
            return url;
        },
        selectImage(image: string) {
            console.log('Selected image:', image);
            // Implementation for selecting an image
        },
        previousPage() {
            if (this.currentPage > 1) this.currentPage--;
        },
        nextPage() {
            if (this.currentPage < this.totalPages) this.currentPage++;
        },
        // Placeholder methods for CRUD operations
        uploadImage() { /* ... */ },
        updateImage() { /* ... */ },
        async handleDelete(filename: string) {
            const api = new ImageAPI('http://localhost:8000');
            try {
                await api.deleteImage(filename);
                this.images = this.images.filter((image) => image !== filename);
                (this.showToast as ToastMethods['showToast'])('Image deleted successfully');
            } catch (error: any) {
                console.error('Error deleting image:', error);
                (this.showToast as ToastMethods['showToast'])('Error deleting image');
            }
        },

        connectWebSocket() {
            this.socket = new WebSocket('ws://localhost:8000/ws');
            this.socket.onmessage = (event: MessageEvent) => {
                const data = JSON.parse(event.data);
                if (Array.isArray(data.images)) {
                    this.images = data.images;
                } else {
                    console.error('Received non-array images data:', data.images);
                }
                this.currentPage = 1;
            };
            this.socket.onerror = (error: Event) => {
                console.error(`WebSocket Error: ${error}`, error);
            };
        }
    },
})
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