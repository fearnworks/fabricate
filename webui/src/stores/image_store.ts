import { defineStore } from 'pinia';
import { ref } from 'vue';
import ImageAPI from '@/api/ImageAPI';
import { DBImageData } from '@/types';

export const useImageStore = defineStore('imageStore', () => {
    const server = `http://${import.meta.env.VITE_SERVER_URL}:28100`;
    const images = ref<DBImageData[]>([]);
    // const isLoading = ref(false); // Uncomment if you want to track loading state

    const fetchImages = async () => {
        const api = new ImageAPI(server);
        // isLoading.value = true; // Start loading
        try {
            const fetchedImages = await api.fetchImages();
            images.value = fetchedImages;
            console.log('Fetched images:', fetchedImages);
        } catch (error) {
            console.error('Error fetching images:', error);
        } finally {
            // isLoading.value = false; // Stop loading
        }
    };

    const handleUpdate = async (uid: string, updateData: DBImageData) => {
        const api = new ImageAPI(server);
        try {
            console.log('updateData', updateData)
            await api.updateImage(uid, updateData);
            await fetchImages(); // Re-fetch images to update the list
        } catch (error) {
            console.error('Error updating image:', error);
        }
    };

    const handleDelete = async (uid: string) => {
        const api = new ImageAPI(server);
        try {
            await api.deleteImage(uid);
            images.value = images.value.filter((image) => image.uid !== uid);
        } catch (error) {
            console.error('Error deleting image:', error);
        }
    };

    const getImageByUid = (uid: string) => {
        return images.value.find(image => image.uid === uid);
    };
    fetchImages()
    // Return the state and actions
    return {
        images,
        // isLoading, // Uncomment if loading state is used
        fetchImages,
        handleUpdate,
        handleDelete,
        getImageByUid,
    };
});
