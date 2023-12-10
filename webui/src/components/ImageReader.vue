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
                <ImageGrid :images="images" @delete-image="handleDelete" @update-image="handleUpdate" />
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, provide } from 'vue';
import ImageGrid from './ImageGrid.vue';
import ImageAPI from '../api/ImageAPI';
import {DBImageData } from '../types';
import useToast from '@/composables/useToast';

const toast = useToast();
const images = ref<DBImageData[] >([]);
const currentPage = ref(1);
const isGridView = ref(true); // State for toggling between grid and carousel
const isLoading = ref(true);

const fetchImages = async () => {
    isLoading.value = true; 
    const api = new ImageAPI('http://localhost:28100');
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


// Provide handleUpdate method to children components
const handleUpdate = async (filename: string, updateData: DBImageData) => {
    const api = new ImageAPI('http://localhost:28100');
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
    const api = new ImageAPI('http://localhost:28100');
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
    // connectWebSocket();
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