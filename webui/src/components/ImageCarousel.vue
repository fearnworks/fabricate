<template>
  <div @wheel="handleWheel" class="carousel-container">
    <Carousel ref="carousel" :itemsToShow="3" :mouseDrag="true" :touchDrag="true">
      <Slide v-for="(image, index) in images" :key="index">
        <ImageCard :filename="image.filename" :tags="image.tags" :notes="image.notes"
          :captions="image.captions" @delete="deleteImage(image.filename)" />
      </Slide>
    </Carousel>
    <div class="flex justify-center mt-4">
      <button @click="prev" data-testid="prev-button"
        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded m-1">
        Previous
      </button>
      <button @click="next" data-testid="next-button"
        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded m-1">
        Next
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Carousel, Slide } from 'vue3-carousel';
import ImageCard from './ImageCard.vue';
import { ref, watch, onMounted, onBeforeUnmount } from 'vue';
import { createImageListProps } from '@/types'; // Replace with your actual type import

const props = createImageListProps();
const images = props.images;
const emit = defineEmits(['delete-image']);

// const carouselRef = ref<InstanceType<typeof Carousel> | null>(null);
const isThrottled = ref(false);

const next = () => {
  console.log("Next")
};

const prev = () => {
  console.log("Prev")
};

const handleWheel = (event: WheelEvent) => {
  if (!isThrottled.value) {
    isThrottled.value = true;
    setTimeout(() => (isThrottled.value = false), 200);
    event.deltaY > 0 ? next() : prev();
  }
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

