// tests/ImageReader.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, fireEvent, screen } from '@testing-library/vue';
import ImageReader from '@/components/ImageReader.vue';
import { renderWithProps } from './test-utils';
import { WebSocket } from 'mock-socket';
import './mock'; // This will automatically use the mocked API due to hoisting

global.WebSocket = WebSocket;

describe('ImageReader', () => {
    beforeEach(() => {
        vi.resetAllMocks();
        vi.useFakeTimers();
    });

    it('renders loading state initially', () => {
        renderWithProps(ImageReader, {});
        expect(screen.getByText('Loading images...')).to.exist
    });
});