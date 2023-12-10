import { defineStore } from 'pinia';
import { ref } from 'vue';
import  ImageAPI  from '@/api/ImageAPI';
import { DBImageData } from '@/types';

export const useImageStore = defineStore('imageStore', () => {
  const images = ref<DBImageData[]>([]);
  // const isLoading = ref(false); // Uncomment if you want to track loading state

  const fetchImages = async () => {
    const api = new ImageAPI('http://localhost:28100');
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

  const handleUpdate = async (filename: string, updateData: DBImageData) => {
    const api = new ImageAPI('http://localhost:28100');
    try {
      await api.updateImage(filename, updateData);
      await fetchImages(); // Re-fetch images to update the list
    } catch (error) {
      console.error('Error updating image:', error);
    }
  };

  const handleDelete = async (filename: string) => {
    const api = new ImageAPI('http://localhost:28100');
    try {
      await api.deleteImage(filename);
      images.value = images.value.filter((image) => image.filename !== filename);
    } catch (error) {
      console.error('Error deleting image:', error);
    }
  };

  const getImageByUid = (uid: string) => {
    return images.value.find(image => image.uid === uid);
  };

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
