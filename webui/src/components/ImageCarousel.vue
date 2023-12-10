<template>
  <div class="carousel-container">
    <q-carousel
      v-model="slide"
      animated
      navigation
      infinite
      arrows
      @mouseenter="autoplay = false"
      @mouseleave="autoplay = true"
    >
      <q-carousel-slide
        v-for="(image, index) in images"
        :key="index"
        :name="index"
      >
        <ImageCard
          :filename="image.filename"
          :tags="image.tags"
          :notes="image.notes"
          :path="image.path"
          :captions="image.captions"
          @delete="deleteImage(image.filename)"
        />
      </q-carousel-slide>
    </q-carousel>
    <div class="flex justify-center mt-4">
      <button @click="prev" data-testid="prev-button" class="custom-button">
        Previous
      </button>
      <button @click="next" data-testid="next-button" class="custom-button">
        Next
      </button>
    </div>
  </div>
</template>


<script setup lang="ts">
import ImageCard from './ImageCard.vue';
import { ref, watch, onMounted, onBeforeUnmount } from 'vue';
import { DBImageData } from '@/types'; // Replace with your actual type import

const props = defineProps<{
  images: DBImageData[]
}>();

const slide = ref(1)
const autoplay = ref(true)
const emit = defineEmits(['delete-image']);

const next = () => {
  console.log("Next")
};

const prev = () => {
  console.log("Prev")
};

watch(() => props.images, (newImages) => {
  console.log('Received new images from parent:', newImages);
});

const deleteImage = (filename: string) => {
  emit('delete-image', filename);
};

// Example of using lifecycle hooks in <script setup>
onMounted(() => {
  console.log('Carousel component mounted');
});

onBeforeUnmount(() => {
  console.log('Carousel component about to unmount');
});
</script>

<style>
.carousel-container {
  height: 100%;
}
</style> 