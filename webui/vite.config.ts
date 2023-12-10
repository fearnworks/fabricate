// vite.config.ts
/// <reference types="vitest" />
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import * as path from 'path';
import { quasar, transformAssetUrls } from '@quasar/vite-plugin'

console.log('Vite config loaded');

export default defineConfig({
    plugins: [
        vue({
            template: { transformAssetUrls }
        }),

        // @quasar/plugin-vite options list:
        // https://github.com/quasarframework/quasar/blob/dev/vite-plugin/index.d.ts
        quasar({
            sassVariables: 'src/quasar-variables.sass'
        })
    ],
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src'),
        },
    },
    server: {
        host: true,
        port: 28100
    },
    test: {
        // Test configuration here
        globals: true,
        environment: 'happy-dom',
        setupFiles: ['./tests/setup.ts'],
    },

});
