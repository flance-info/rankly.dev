// router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import AddPlugin from '@/Components/AddPlugin.vue';

const routes = [
    {
        path: '/add-plugin',
        name: 'AddPlugin',
        component: AddPlugin,
    },
    // Add other routes here if necessary
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
