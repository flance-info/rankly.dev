<script setup>
import AppLayout from '@/Layouts/AppLayout.vue';
import AddPluginForm from '@/Pages/AddPluginForm.vue';
import PluginList from '@/Components/PluginList.vue';
import { ref, onMounted } from 'vue';
import axios from 'axios';

const plugins = ref([]);

// Fetch plugins from the session
const fetchSessionPlugins = async () => {
  try {
    const response = await axios.get('/api/session-plugins');
    plugins.value = response.data;
  } catch (error) {
    console.error('Error fetching session plugins:', error);
  }
};

// Fetch session plugins when the component is mounted
onMounted(fetchSessionPlugins);

const addPluginToList = (newPlugin) => {
  plugins.value.push(newPlugin);
  // Update the session with the new plugin list
  axios.post('/api/update-session-plugins', { plugins: plugins.value })
    .then(response => {
      console.log('Session updated successfully:', response.data.plugin_data);
    })
    .catch(error => {
      console.error('Error updating session plugins:', error);
    });
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
                    <AddPluginForm @plugin-added="addPluginToList" />
                </div>
            </div>
        </div>

        <!-- Plugin List Component -->
        <div class="py-4">
            <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
                <div class="bg-white overflow-hidden shadow-xl sm:rounded-lg">
            <PluginList :plugins="plugins" />
          </div>
            </div>
        </div>
    </AppLayout>
</template>


