// ImageGrid.spec.ts
import { mount } from '@vue/test-utils';
import { Quasar } from 'quasar';
import ImageGrid from '@/components/ImageGrid.vue';
import { describe, it, expect } from 'vitest';

describe('ImageGrid', () => {
  it('renders correct image URL', async () => {
    const image = {
      uid: '1',
      filename: 'test-image.png',
      tags: [],
      notes: '',
      captions: '',
      path: 'http://192.168.1.75:28100/static/test-image.png'
    };

    // Mount the component with props
    const wrapper = mount(ImageGrid, {
      props: {
        images: [image]
      },
      global: {
        plugins: [Quasar], // Ensure Quasar components are available
      }
    });

    // Wait for Vue and Quasar to perform updates
    await wrapper.vm.$nextTick();

    // Find the image using the `data-testid` attribute
    const imageElement = wrapper.find(`[data-testid="image-0"] img`);

    // Check if the image element was found before calling attributes
    if (imageElement.exists()) {
      // Assert that the `src` of the image matches the expected path
      expect(imageElement.attributes('src')).toBe(image.path);
    } else {
      // If the image element wasn't found, fail the test with a message
      expect(imageElement.exists()).toBe(true);
    }
  });
});
