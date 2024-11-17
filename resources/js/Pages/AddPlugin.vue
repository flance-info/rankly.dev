<script setup>
import AppLayout from '@/Layouts/AppLayout.vue';
import AddPluginForm from '@/Pages/AddPluginForm.vue';
import PluginList from '@/Components/PluginList.vue';
import {ref, onMounted} from 'vue';
import {useToast} from "vue-toastification";

const plugins = ref({}); // Store plugins as an object with slugs as keys
const toast = useToast();
// Fetch plugins from local storage
const fetchLocalPlugins = () => {
    const storedPlugins = localStorage.getItem('plugins');
    plugins.value = storedPlugins ? JSON.parse(storedPlugins) : {};
};

// Save plugins to local storage
const savePluginsToLocal = () => {
    localStorage.setItem('plugins', JSON.stringify(plugins.value));
};

// Fetch plugins when the component is mounted
onMounted(fetchLocalPlugins);
const decodeHTML = (html) => {
    const txt = document.createElement('textarea');
    txt.innerHTML = html;
    return txt.value;
};
const clearPlugins = () => {
    plugins.value = {};
    savePluginsToLocal();
};
// Add or update a plugin by its slug
const addPluginToList = (newPlugin) => {
    if (newPlugin.slug) {
        const decodedName = decodeHTML(newPlugin.name);
        if (plugins.value[newPlugin.slug]) {
            clearPlugins();
            plugins.value[newPlugin.slug] = newPlugin;
            toast.success(
                `Plugin "${decodedName}" information updated.`,
                {
                    dangerouslyHTML: true,
                }
            );
        } else {
            clearPlugins();
            plugins.value[newPlugin.slug] = newPlugin;
            toast.info(`Plugin "${decodedName}" added successfully.`);
        }
        savePluginsToLocal();
    } else {
        console.error('Plugin does not have a slug:', newPlugin);
    }
};
</script>


<template>
    <AppLayout title="Plugins">
        <template #header>
            <h1 class="font-semibold text-xl text-gray-800 leading-tight">
                Plugins > Add plugin
            </h1>
        </template>

        <div class="py-12">
            <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
                <div class="bg-white overflow-hidden shadow-xl sm:rounded-lg">
                    <AddPluginForm @plugin-added="addPluginToList"/>
                </div>
            </div>
        </div>

        <!-- Plugin List Component -->
        <div class="py-4">
            <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
                <div class="bg-white overflow-hidden shadow-xl sm:rounded-lg">
                    <PluginList :plugins="plugins"/>
                </div>
            </div>
        </div>
    </AppLayout>
</template>


