// mock.ts
import { vi } from 'vitest';

export const mockImageList = [{
  filename: 'test-image.png',
  tags: [],
  notes: '',
  captions: '',
  path: ''
}];

vi.mock('@/api/ImageAPI', async (importOriginal) => {
  const actual = await importOriginal<typeof import('@/api/ImageAPI')>();
  return {
    ...actual,
    default: class MockImageAPI {
      async fetchImages() {
        return mockImageList;
      }
      // other methods
      async deleteImage() {
        // Mock implementation
      }
      async updateImage() {
        // Mock implementation
      }
    }
  };
});