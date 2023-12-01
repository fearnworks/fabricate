// tests/ImageReader.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, fireEvent, screen } from '@testing-library/vue';
import ImageReader from '@/components/ImageReader.vue';
import { renderWithProps } from './test-utils';
import { WebSocket } from 'mock-socket';

global.WebSocket = WebSocket;
beforeEach(() => {
    vi.useFakeTimers()
})
vi.mock('@/api/ImageAPI', async () => {
        // Import the actual module
        const actual = await vi.importActual('@/api/ImageAPI') as any;
    
        // Create a partial mock, with the default export being a mock class
        // and keeping the rest of the exports as they are
        return {
            ...actual,
            default: class MockImageAPI {
                async fetchImages() {
                    // Mock implementation or vi.fn() if you want to track calls
                    return [{ filename: 'test-image.png' }];
                }
                async deleteImage() {
                    // Mock implementation or vi.fn()
                }
                async updateImage() {
                    // Mock implementation or vi.fn()
                }
            }
        };
    });

describe('ImageReader', () => {
    beforeEach(() => {
        vi.resetAllMocks();
    });

    it('renders loading state initially', () => {
        renderWithProps(ImageReader, {});
        expect(screen.getByText('Loading images...')).to.exist
    });
});