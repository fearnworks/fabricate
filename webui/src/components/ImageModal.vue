<template>
    <div class="fixed inset-0 bg-gray-900 bg-opacity-75 flex justify-center items-center p-4">
        <div class="modal-content bg-gray-800 text-white rounded-lg shadow-lg overflow-hidden max-w-4xl w-full mx-auto">
            <div class="fixed inset-0 bg-gray-900 bg-opacity-75 flex justify-center items-center p-4" @click="closeModal">
                <div class="modal-content bg-gray-800 text-white rounded-lg shadow-lg overflow-hidden max-w-4xl w-full mx-auto p-6"
                    @click.stop>
                    <!-- Modal content goes here -->
                    <div class="p-6">
                        <!-- ImageCard component -->
                        <ImageCard :filename="image.filename" :tags="image.tags" :notes="image.notes" :path="image.path"
                            :captions="image.captions" @delete="handleDelete" @update="handleUpdate" />
                        <!-- Close button -->
                        <button @click="closeModal" class="absolute top-3 right-3 text-gray-400 hover:text-gray-300">
                            <!-- Icon or text for close button -->
                            Close
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { inject, defineEmits, ref } from 'vue';
import ImageCard from './ImageCard.vue';
import type { DBImageData } from '@/types'; // Assuming Image type is defined in types.ts

// Define props and emits
const props = defineProps<{
    image: DBImageData;
}>();
const image = ref(props.image);
const emit = defineEmits(['close', 'delete-image']);

const handleUpdate = inject<(filename: string, data: any) => void>('handleUpdate');

const handleDelete = (filename: string) => {
    // You can handle the delete logic here or emit an event to the parent
    console.log('Delete image:', filename);
    emit('delete-image', filename); // Emitting to the parent component
};

const closeModal = () => {
    emit('close');
};
</script>
<style>
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.7);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.modal-content {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    max-width: 500px;
    max-height: 80vh;
    overflow-y: auto;
}

.modal-content img {
    width: 100%;
    border-radius: 8px;
}
</style>
  