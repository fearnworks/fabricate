// vite.config.ts
/// <reference types="vitest" />
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import * as path from 'path';
console.log('Vite config loaded');

export default defineConfig({
    plugins: [vue()],
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src'),
        },
    },
    test: {
        // Test configuration here
        globals: true,
        environment: 'happy-dom',
        setupFiles: ['./tests/setup.ts'], 
    },
    
});
