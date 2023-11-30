<template>
        <div v-if="visible" class="fixed bottom-0 right-0 bg-blue-500 text-white p-4 rounded m-4">
            <p>{{ message }}</p>
        </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
    name: 'ToastComponent',
    setup() {
        const visible = ref(false);
        const message = ref('');

        const showToast = (msg: string) => {
            message.value = msg;
            visible.value = true;
            setTimeout(() => {
                visible.value = false;
            }, 3000); // Hide after 3 seconds
        };

        return {
            visible,
            message,
            showToast
        };
    },
});
</script>

<style scoped>
.toast {
    /* Style your toast */
}
</style>