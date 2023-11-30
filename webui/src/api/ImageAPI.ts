import axios, { AxiosInstance } from 'axios';

interface ImageData {
  filename: string;
  tags?: string[];
  notes?: string;
  captions?: string;
}

class ImageAPI {
  private axiosInstance: AxiosInstance;

  constructor(baseURL: string) {
    this.axiosInstance = axios.create({ baseURL });
  }

  async fetchImages(): Promise<any> {
    try {
      const response = await this.axiosInstance.get('/images');
      console.log(response)
      return response.data;
    } catch (error) {
      console.error(error);
      throw error;
    }
  }

  async deleteImage(filename: string): Promise<any> {
    try {
      const response = await this.axiosInstance.delete(`/delete-image/${filename}`);
      return response.data;
    } catch (error) {
      console.error(error);
      throw error;
    }
  }

  async updateImage(filename: string, updateData: ImageData): Promise<any> {
    try {
      const response = await this.axiosInstance.patch(`/update-image/${filename}`, updateData);
      return response.data;
    } catch (error) {
      console.error(error);
      throw error;
    }
  }

  // Further methods can be added as needed
}

export default ImageAPI;
