<template>
    <div class="flex flex-col p-8 bg-white rounded-2xl shadow-2xl max-w mx-auto" data-testid="image-card">
        <div class="flex flex-row mb-8">
            <!-- Image display -->
            <div class="flex-none w-96 h-96 bg-gray-200 text-gray-700 p-8 rounded-2xl mr-8">
                <img :src="get_src(filename)" alt="Image" class="object-cover rounded-2xl" />
            </div>
            <!-- Filename and Caption -->
            <div class="flex-grow space-y-8">
                <input type="text" v-model="editableFilename"
                    class="w-full text-2xl font-medium bg-transparent border-b-4 border-gray-300 focus:outline-none"
                    readonly />
                <textarea v-model="editableCaptions" placeholder="Caption"
                    class="w-full text-xl bg-transparent border-b-4 border-gray-300 focus:outline-none"></textarea>
            </div>
        </div>
        <!-- Other fields -->
        <textarea v-model="editableNotes" placeholder="Notes"
            class="w-full mb-8 text-xl bg-transparent border-b-4 border-gray-300 focus:outline-none"></textarea>
        <!-- Action buttons -->
        <div class="flex justify-between mt-8">
            <button @click="emitUpdate"
                class="px-8 py-4 text-2xl text-white bg-blue-500 rounded-2xl hover:bg-blue-700 focus:outline-none">
                Update
            </button>
            <button @click="moveImage"
                class="px-8 py-4 text-2xl text-white bg-yellow-500 rounded-2xl hover:bg-yellow-700 focus:outline-none">
                Move
            </button>
            <button @click="emitDelete" data-testid="delete-button"
                class="px-8 py-4 text-2xl text-white bg-red-500 rounded-2xl hover:bg-red-700 focus:outline-none">
                Delete
            </button>
        </div>
    </div>
</template>
  
<script lang="ts">
import { defineComponent, ref, computed, inject, PropType, watch } from 'vue';

interface ImageProps {
    filename: string;
    tags: string[];
    notes: string;
    captions: string;
}

export default defineComponent({
    props: {
        filename: {
            type: String,
            required: true,
        },
        tags: {
            type: Array as PropType<string[]>,
            default: () => [],
        },
        notes: {
            type: String,
            default: '',
        },
        captions: {
            type: String,
            default: '',
        },
    },
    setup(props, { emit }) {
        // Reactive references for the editable properties
        const editableFilename = ref(props.filename);
        const editableNotes = ref(props.notes);
        const editableCaptions = ref(props.captions);

        // Inject the handleUpdate method from parent if it's provided
        const handleUpdate = inject<(filename: string, data: any) => void>('handleUpdate');

        // Computed property for the image source URL
        const imageSrc = computed(() => `http://localhost:8000/static/${props.filename}`);

        // Method to emit the update event
        const emitUpdate = () => {
            if (handleUpdate) {
                handleUpdate(editableFilename.value, {
                    filename: editableFilename.value,
                    notes: editableNotes.value,
                    captions: editableCaptions.value,
                });
            }
        };

        // Watchers for the props to update the local editable references
        watch(() => props.filename, (newVal) => {
            editableFilename.value = newVal;
        });
        watch(() => props.notes, (newVal) => {
            editableNotes.value = newVal;
        });
        watch(() => props.captions, (newVal) => {
            editableCaptions.value = newVal;
        });

        // Methods to emit delete and move events
        const emitDelete = () => {
            emit('delete', props.filename);
        };
        const moveImage = () => {
            console.log('Move image:', props.filename);
        };
        
        const get_src = (filename: string) => {
            return `http://localhost:8000/static/${filename}`;
        };

        return {
            editableFilename,
            editableNotes,
            editableCaptions,
            imageSrc,
            emitUpdate,
            emitDelete,
            moveImage,
            get_src,
        };
    },
});
</script>
  

<style scoped>
/* Styles for ImageCard */
.tags {
    /* Styles for tags */
}

.tag {
    /* Individual tag styles */
}
</style>
