<template>
  <div @wheel="handleWheel" class="carousel-container">
    <Carousel ref="carousel" :itemsToShow="3" :mouseDrag="true" :touchDrag="true">
      <Slide v-for="(image) in images" :key="image.filename">
        <ImageCard :src="image.src" :filename="image.filename" :tags="image.tags" :notes="image.notes"
          :captions="image.captions" @delete="$emit('delete-image', image.filename)" />
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
import { ref, defineComponent, PropType, watch, onMounted } from 'vue';
import ImageCard from './ImageCard.vue';
import 'vue3-carousel/dist/carousel.css';

interface Image {
  src: string;
  filename: string;
  tags: string[];
  notes: string;
  captions: string;
}

export default defineComponent({
  components: {
    Carousel,
    Slide,
    ImageCard,
  },
  props: {
    images: Array as PropType<Image[]>,
  },
  setup(props) {
    const carouselRef = ref<InstanceType<typeof Carousel> | null>(null);
    const isThrottled = ref(false);

    const next = () => {
      carouselRef.value?.next();
    };

    const prev = () => {
      carouselRef.value?.prev();
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


    // Expose reactive data and methods for the template
    return {
      carouselRef,
      isThrottled,
      next,
      prev,
      handleWheel,
    };
  },
});
</script>

