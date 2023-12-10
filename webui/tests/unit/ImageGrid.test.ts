// ImageGrid.spec.ts
import { mount } from '@vue/test-utils';
import ImageGrid from '@/components/ImageGrid.vue';
import { describe, it, expect } from 'vitest';
describe('ImageGrid', () => {
  it('renders correct image URL', async () => {
    const image = {
      filename: 'test-image.png',
      tags: [],
      notes: '',
      captions: '',
      path: 'http://localhost:28100/static/test-image.png'
    };

    // Mount the component with props
    const wrapper = mount(ImageGrid, {
      props: {
        images: [image]
      }
    });

    // Wait for Vue to perform updates if needed
    await wrapper.vm.$nextTick();

    // Find the image by using the `find` method and the alt text
    const imageElement = wrapper.find(`[alt="${image.path}"]`);

    // Check if the image element was found before calling attributes
    if (imageElement.exists()) {
      // Assert that the `src` of the image matches the expected path
      expect(imageElement.attributes('src')).toBe(image.path);
    } else {
      // If the image element wasn't found, fail the test with a message
      expect(imageElement.exists()).toBe(true);
    }
  })
})