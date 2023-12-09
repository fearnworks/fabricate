// ImageGrid.spec.ts
import { render } from '@testing-library/vue'
import ImageGrid from '@/components/ImageGrid.vue'
import { describe, it, expect, vi, beforeEach } from 'vitest';

describe('ImageGrid', () => {
  it('renders correct image URL', async () => {
    const image = { filename: 'test-image.png', id: '1', url: '' }
    const { getByAltText } = render(ImageGrid, {
      props: { images: [image] }
    })

    const renderedImage = getByAltText(image.filename)
    expect(renderedImage.getAttribute('src')).to.equal('http://server:28100/static/test-image.png')
  })
})