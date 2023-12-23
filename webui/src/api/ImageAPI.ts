import axios, { AxiosInstance } from 'axios';
import { DBImageData} from '@/types';
import getSrc from '@/composables/utils';


interface ImageAPIInterface {
  fetchImages: () => Promise<DBImageData[]>;
  deleteImage: (uid: string) => Promise<void>;
  updateImage: (uid: string, updateData: DBImageData) => Promise<void>;
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

  async deleteImage(uid: string): Promise<void> {
    await this.axiosInstance.delete(`/delete-image/${uid}`);
  }

  async updateImage(uid: string, updateData: DBImageData): Promise<void> {
    await this.axiosInstance.patch(`/update-image/${uid}`, updateData);
  }

  // Further methods can be added as needed
}

export default ImageAPI;
