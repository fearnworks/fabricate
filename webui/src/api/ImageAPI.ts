import axios, { AxiosInstance } from 'axios';
import { Image, ImageList} from '@/types';


interface ImageAPIInterface {
  fetchImages: () => Promise<Image[]>;
  deleteImage: (filename: string) => Promise<void>;
  updateImage: (filename: string, updateData: Image) => Promise<void>;
}

class ImageAPI implements ImageAPIInterface {
  private axiosInstance: AxiosInstance;

  constructor(baseURL: string, axiosInstance?: AxiosInstance) {
    this.axiosInstance = axiosInstance || axios.create({ baseURL });
  }

  async fetchImages(): Promise<ImageList> {
    const response = await this.axiosInstance.get<Image[]>('/images');
    const imageList: ImageList = response.data;
    return imageList;
  }

  async deleteImage(filename: string): Promise<void> {
    await this.axiosInstance.delete(`/delete-image/${filename}`);
  }

  async updateImage(filename: string, updateData: Image): Promise<void> {
    await this.axiosInstance.patch(`/update-image/${filename}`, updateData);
  }

  // Further methods can be added as needed
}

export default ImageAPI;
