<template>
  <div @wheel="handleWheel" class="carousel-container">
    <Carousel ref="carousel" :itemsToShow="5" :mouseDrag="true" :touchDrag="true">
      <Slide v-for="(imageSrc, index) in imageUrls" :key="index">
        <ImageCard :src="imageSrc" :filename="extractFilename(imageSrc)"
          @delete="$emit('delete-image', extractFilename(imageSrc))" />
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

<script>
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
    imageUrls: Array,
  },
  setup() {
    // Carousel setup logic here (if needed)
  },
  data() {
    return {
      carousel: ref(null),
      isThrottled: false, // Prevent too many rapid scroll events
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
      // Use a simple throttle mechanism to prevent too many rapid invocations
      if (!this.isThrottled) {
        this.isThrottled = true;
        setTimeout(() => {
          this.isThrottled = false;
        }, 200);

        if (event.deltaY > 0) {
          this.next();
        } else {
          this.prev();
        }
      }
    },
    extractFilename(url) {
      // Extracts the filename from the URL
      const urlSegments = url.split('/');
      return urlSegments[urlSegments.length - 1] || 'No filename';
    },
  },
  // The 'mounted' hook can be used to perform actions once the component is mounted.
  // If you need to access the carousel's data properties or call its methods,
  // you can do so here since the carousel will be fully initialized at this point.
  mounted() {
    // Make sure the carousel is assigned after component is mounted
    this.carousel = this.$refs.carousel;
  },
};
</script>

<style scoped>
.carousel-container {
  /* styles if needed */
}</style>
