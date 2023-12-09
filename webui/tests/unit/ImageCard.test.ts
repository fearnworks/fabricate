// ImageCard.spec.ts
import { describe, it, expect, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import ImageCard from '@/components/ImageCard.vue';

describe('ImageCard', () => {
  it('emits delete event when delete button is clicked', async () => {
    // Create a mock for the handleUpdate method if it's used in the component
    const handleUpdate = vi.fn();

    // Mount the component with props
    const wrapper = mount(ImageCard, {
      props: {
        filename: 'test-image.png',
        tags: [],
        notes: '',
        captions: '',
        path: 'http://server:28100/static/test-image.png'
      },
      // Provide mocks for any injected dependencies or global properties
      global: {
        mocks: {
          handleUpdate
        }
      }
    });

    // Find the delete button by using the `find` method and the test id
    const deleteButton = wrapper.find('[data-testid="delete-button"]');

    // Trigger a click event on the delete button
    await deleteButton.trigger('click');

    // Assert that the delete event has been emitted with the correct payload
    expect(wrapper.emitted()).toHaveProperty('delete');
    expect(wrapper.emitted().delete[0]).toEqual(['test-image.png']);
  });
});