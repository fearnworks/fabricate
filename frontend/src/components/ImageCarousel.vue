<template>
  <div @wheel="handleWheel" class="carousel-container">
    <Carousel ref="carousel" :itemsToShow="3" :mouseDrag="true" :touchDrag="true">
      <Slide v-for="(image) in images" :key="image.filename">
        <ImageCard
          :src="image.src"
          :filename="image.filename"
          :tags="image.tags"
          :notes="image.notes"
          :captions="image.captions"
          @delete="$emit('delete-image', image.filename)" />
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

<script lang="ts">
import { Carousel, Slide } from 'vue3-carousel';
import { ref } from 'vue';
import ImageCard from './ImageCard.vue';
import 'vue3-carousel/dist/carousel.css';

export default {
  components: {
    Carousel,
    Slide,
    ImageCard,
  },
  props: {
    images: Array,
  },
  data() {
    return {
      carousel: ref(null),
      isThrottled: false,
    };
  },
  methods: {
    next() {
      this.carousel.next();
    },
    prev() {
      this.carousel.prev();
    },
    handleWheel(event) {
      if (!this.isThrottled) {
        this.isThrottled = true;
        setTimeout(() => this.isThrottled = false, 200);
        event.deltaY > 0 ? this.next() : this.prev();
      }
    },
  },
  mounted() {
    this.carousel = this.$refs.carousel;
  },
  watch: {
    images(newImages) {
      console.log('Received new images from parent:', newImages);
    },
  },
};
</script>

<style scoped>
.carousel-container {
  /* Add styles here */
}
</style>
