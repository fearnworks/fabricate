<template>
    <div class="grid-container">
        <q-card v-for="(image, index) in images" :key="index">
            <router-link :to="`/images/${image.filename}`">
                <q-img :src="image.path" :alt="image.path" :data-testid="`image-${index}`">

                </q-img>
            </router-link>
        </q-card>
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
</script>
  
<style>
.grid-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 16px;
    padding: 16px;
}

.grid-item {
    cursor: pointer;
}

.grid-item .q-img {
    border-radius: 8px;
    width: 100%;
    height: auto;
    /* Adjust height as needed */
}
</style>