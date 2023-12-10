export interface ToastMethods {
  /**
   * This method is used to display a toast message.
   * @param message The message to be displayed in the toast.
   */
  showToast: (message: string) => void;
}

export interface DBImageData {
  filename: string;
  tags: string[];
  notes: string;
  captions: string;
  path: string;
}
