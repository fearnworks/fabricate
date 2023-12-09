import axios, { AxiosInstance } from 'axios';
import { DBImageData} from '@/types';
import getSrc from '@/composables/utils';


interface ImageAPIInterface {
  fetchImages: () => Promise<DBImageData[]>;
  deleteImage: (filename: string) => Promise<void>;
  updateImage: (filename: string, updateData: DBImageData) => Promise<void>;
}

class ImageAPI implements ImageAPIInterface {
  private axiosInstance: AxiosInstance;

  constructor(baseURL: string, axiosInstance?: AxiosInstance) {
    this.axiosInstance = axiosInstance || axios.create({ baseURL });
  }

  async fetchImages(): Promise<DBImageData[]> {
    console.log('fetchImages', this.axiosInstance.defaults.baseURL)
    const response = await this.axiosInstance.get<{images: DBImageData[]}>('/images');
    console.log(response)
    const imageList: DBImageData[] = response.data.images.map(image => {
      image.path = getSrc(image.filename);
      console.log(image.path)
      return image;
    });
    return imageList;
  }

  async deleteImage(filename: string): Promise<void> {
    await this.axiosInstance.delete(`/delete-image/${filename}`);
  }

  async updateImage(filename: string, updateData: DBImageData): Promise<void> {
    await this.axiosInstance.patch(`/update-image/${filename}`, updateData);
  }

  // Further methods can be added as needed
}

export default ImageAPI;
