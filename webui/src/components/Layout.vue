<template>
    <q-layout view="hhh LpR lFf">
        <q-header reveal bordered class="bg-primary text-white" height-hint="98">
            <q-toolbar>
                <q-btn dense flat round icon="menu" @click="toggleLeftDrawer"> Left </q-btn>
                <q-toolbar-title>
                    Fabricate
                </q-toolbar-title>
                <router-link to="/">Go to Home</router-link>
                <router-link to="/about">Go to About</router-link>
            </q-toolbar>
        </q-header>

        <q-drawer show-if-above v-model="leftDrawerOpen" side="left" bordered>
            <ImageReader class="bg-slate-600" />
        </q-drawer>
        <q-page-container>
            <router-view></router-view>
        </q-page-container>

        <q-footer reveal elevated class="bg-grey-8 text-white">
            <q-toolbar>
                <q-toolbar-title>
                    <div>Title</div>
                </q-toolbar-title>
            </q-toolbar>
        </q-footer>
    </q-layout>
</template>
  
<script setup lang="ts">
import { ref } from 'vue';
import ImageReader from '@/components/ImageReader.vue';

const leftDrawerOpen = ref(false);

const toggleLeftDrawer = () => {
    leftDrawerOpen.value = !leftDrawerOpen.value;
};
</script>