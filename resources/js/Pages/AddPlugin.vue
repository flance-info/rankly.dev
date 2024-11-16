<script setup>
import AppLayout from '@/Layouts/AppLayout.vue';
import AddPluginForm from '@/Pages/AddPluginForm.vue';
import PluginList from '@/Components/PluginList.vue';
import {ref, onMounted} from 'vue';

const plugins = ref([]);

// Function to fetch plugins from local storage
const fetchLocalPlugins = () => {
    const storedPlugins = localStorage.getItem('plugins');
    plugins.value = storedPlugins ? JSON.parse(storedPlugins) : [];
};

// Save plugins to local storage
const savePluginsToLocal = () => {
    localStorage.setItem('plugins', JSON.stringify(plugins.value));
};

// Fetch plugins when the component is mounted
onMounted(fetchLocalPlugins);

const addPluginToList = (newPlugin) => {
    plugins.value.push(newPlugin);
    savePluginsToLocal(); // Update local storage with the new plugin list
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


