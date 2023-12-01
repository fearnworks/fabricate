// tests/ImageCard.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, fireEvent, screen } from '@testing-library/vue';
import ImageCard from '@/components/ImageCard.vue' 

describe('ImageCard', () => {
  it('emits delete event when delete button is clicked', async () => {
    const { getByTestId, emitted } = render(ImageCard, {
      props: {
        filename: 'test-image.png',
        tags: [],
        notes: '',
        captions: '',
      },
    });

    const deleteButton = getByTestId('delete-button');
    await fireEvent.click(deleteButton);

    // Check emitted event for delete
    expect(emitted()).toHaveProperty('delete');
    expect(emitted().delete[0]).toEqual(['test-image.png']);
  });

  
});

