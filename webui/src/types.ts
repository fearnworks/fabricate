import { defineProps, withDefaults, PropType } from 'vue';

export interface ToastMethods {
  /**
   * This method is used to display a toast message.
   * @param message The message to be displayed in the toast.
   */
  showToast: (message: string) => void;
}
  
export interface Image {
    filename: string;
    tags: string[];
    notes: string;
    captions: string;
}

export const createImageProps = () =>
  withDefaults(defineProps<Image>(), {
    filename: '',
    tags: () => [],
    notes: '',
    captions: '',
  });

export interface ImageList extends Array<Image> {}

export const createImageListProps = () => {
  return defineProps({
    images: {
      type: Array as PropType<ImageList>,
      required: true,
    },
  });
};