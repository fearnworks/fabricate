<template>
    <div class="grid-container">
        <div v-for="(image, index) in images" :key="index">
            <img :src="image.path" :alt="image.path" @click="showModal(image)" :data-testid="`image-${index}`" />
        </div>
        <ImageModal v-if="selectedImage" :image="selectedImage" @close="selectedImage = null" />
    </div>
</template>
  
<script setup lang="ts">
import { ref } from 'vue';
import ImageModal from './ImageModal.vue';
import { DBImageData } from '@/types';

defineProps<{
    images: DBImageData[]
}>();

const selectedImage = ref<DBImageData | null>(null);

function showModal(image: DBImageData) {
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