<template>
    <div class="bg-slate-800 text-white">
        <div v-if="image" class="flex justify-center items-center h-screen">
            <!-- Use Tailwind's max-w and h-screen to make image responsive -->
            <q-img :src="image.path" fit="contain" height="90%" width="90%" position="0"
                class="max-w-3/4 h-auto max-h-full object-contain" />
        </div>
        <div v-else>
            <p>No image found for UID: {{ uid }}</p>
        </div>
        <q-drawer v-model="drawerOpen" side="right" bordered>
            <div class="bg-slate-700 text-white min-h-screen">
                <div class="q-pa-md">
                    <div class="q-gutter-y-md column" style="max-width: 300px">
                        <!-- Display image details -->
                        <p>Image UID: {{ image.uid }}</p>
                        <q-input filled v-model="editableImage.filename" label="Filename" dark />
                        <q-input filled v-model="editableImage.captions" label="Captions" type="textarea" dark />
                        <q-input filled v-model="editableImage.notes" label="Notes" type="textarea" dark />
                        <q-input filled v-model="editableImage.tags" label="Tags" dark />
                        <q-input filled v-model="editableImage.path" label="Path" dark readonly />
                        <q-btn label="Update" color="primary" class="q-mt-md" @click="submitUpdate"/>
                        <q-btn label="Delete" color="negative" class="q-mt-md" @click="submitDelete"/>

                    </div>
                </div>
            </div>
        </q-drawer>
    </div>
</template>
  
<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useImageStore } from '@/stores/image_store';

const route = useRoute();
const imageStore = useImageStore();
const drawerOpen = ref(true); // Reactive state for the drawer's visibility

// Extract UID from route parameters
const uid = computed(() => route.params.uid as string);

// Fetch image by UID
const image = computed(() => imageStore.getImageByUid(uid.value));
const editableImage = ref({ ...image.value }); // Make a reactive copy for editing
const submitUpdate = async () => {
  await imageStore.handleUpdate(editableImage.value.uid, editableImage.value);
};
const submitDelete = async () => {
  await imageStore.handleDelete(editableImage.value.uid);
};
watch(image, (newValue) => {
  editableImage.value = { ...newValue };
});
// You can also call fetchImages() if the images are not preloaded
// onMounted(() => {
//   imageStore.fetchImages();
// });
</script>
<style scoped>
.image-card {
    max-width: 90%;
    overflow: hidden;
    /* Prevent overflow if the image is too large */
}

.contained-image {
    max-width: 90%;
    max-height: 900vh;
    /* Set maximum height to the viewport height */
    object-fit: contain;
    /* Ensure the image is scaled properly */
}
</style>