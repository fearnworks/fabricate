<template>
    <div class="grid-container">
        <div v-for="(image, index) in images" :key="index" class="grid-item">
            <img :src="getImageUrl(image.filename)" :alt="image.filename" @click="showModal(image)" />
        </div>
        <ImageModal v-if="selectedImage" :image="selectedImage" @close="selectedImage = null" />
    </div>
</template>
  


<script setup lang="ts">
import { ref } from 'vue';
import ImageModal from './ImageModal.vue';
import { Image, createImageListProps } from '@/types';

const props = createImageListProps();
const images = ref(props.images);
const selectedImage = ref<Image | null>(null);

function getImageUrl(filename: string) {
    return `http://server:28100/static/${filename}`;
}

function showModal(image: Image) {
    selectedImage.value = image;
}
</script>
  
<style>
.grid-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 16px;
    padding: 16px;
}

.grid-item img {
    width: 100%;
    cursor: pointer;
    border-radius: 8px;
}
</style>