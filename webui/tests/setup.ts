// Example of a test setup file (e.g., tests/setup.ts)

// import { createTestingPinia } from '@pinia/testing'; // If you use Pinia
import { config } from '@vue/test-utils';
import { vi } from 'vitest';

// Mock global injections or functions
config.global.provide = {
  handleUpdate: vi.fn(), // Replace with a real function if needed
  get_src: vi.fn(), // Replace with a real function if needed
};

// Setup Pinia for state management (if used)
// config.global.plugins.push(createTestingPinia());
