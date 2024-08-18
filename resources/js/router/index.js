import { createRouter, createWebHistory } from 'vue-router';
import AddPlugin from '../components/AddPlugin.vue';

const routes = [
    {
        path: '/add-plugin',
        name: 'AddPlugin',
        component: AddPlugin,
    },
    // Other routes...
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
