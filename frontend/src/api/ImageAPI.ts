import axios, { AxiosInstance } from 'axios';

class ImageAPI {
  private axiosInstance: AxiosInstance;

  constructor(baseURL: string) {
    this.axiosInstance = axios.create({
      baseURL: baseURL,
    });
  }

  async fetchImages(): Promise<any> { // Specify the return type if known
    try {
      const response = await this.axiosInstance.get('/images');
      return response.data;
    } catch (error) {
      // Handle or rethrow the error appropriately
      console.log(error);
      throw error;
    }
  }

  async deleteImage(filename: string): Promise<any> { // Specify the return type if known
    try {
      const response = await this.axiosInstance.delete(`/delete-image/${filename}`);
      return response.data;
    } catch (error) {
      console.log(error);
      // Handle or rethrow the error appropriately
      throw error;
    }
  }

  // Additional methods for other CRUD operations can be added here
}

export default ImageAPI;