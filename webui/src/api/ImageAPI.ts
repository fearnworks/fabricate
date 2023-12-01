import axios, { AxiosInstance } from 'axios';

interface ImageData {
  filename: string;
  tags?: string[];
  notes?: string;
  captions?: string;
}

interface ImageAPIInterface {
  fetchImages: () => Promise<ImageData[]>;
  deleteImage: (filename: string) => Promise<void>;
  updateImage: (filename: string, updateData: ImageData) => Promise<void>;
}

class ImageAPI implements ImageAPIInterface {
  private axiosInstance: AxiosInstance;

  constructor(baseURL: string, axiosInstance?: AxiosInstance) {
    this.axiosInstance = axiosInstance || axios.create({ baseURL });
  }

  async fetchImages(): Promise<ImageData[]> {
    const response = await this.axiosInstance.get<ImageData[]>('/images');
    return response.data;
  }

  async deleteImage(filename: string): Promise<void> {
    await this.axiosInstance.delete(`/delete-image/${filename}`);
  }

  async updateImage(filename: string, updateData: ImageData): Promise<void> {
    await this.axiosInstance.patch(`/update-image/${filename}`, updateData);
  }

  // Further methods can be added as needed
}

export default ImageAPI;
