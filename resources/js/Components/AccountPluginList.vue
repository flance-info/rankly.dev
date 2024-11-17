<template>
    <div>
        <h3 class="pt-4 text-2xl font-semibold text-gray-800 mb-4 p-6 lg:p-8 bg-white">
            Plugins in Your Account
        </h3>
        <div v-if="!plugins || plugins.length === 0">
            <p>No plugins found in your account.</p>
        </div>
        <div v-else class="bg-gray-200 bg-opacity-25 grid grid-cols-1 md:grid-cols-4 gap-6 lg:gap-8 p-6 lg:p-8">
            <div v-for="plugin in plugins" :key="plugin.id" class="bg-white rounded-lg p-4 shadow-md flex flex-col relative">
                <button
                    class="absolute top-1 right-1 w-6 h-6 pb-6 pl-6 pt-2.5 pr-4 flex items-center justify-center text-sm z-10"
                    @click="confirmRemove(plugin)"
                    title="Remove Plugin"
                >
                    x
                </button>
                <div class="pb-2 flex items-start relative">


                    <img :src="getPluginIconUrl(plugin.slug)"   @error="handleIconError"
                          :data-slug="plugin.slug"
                         alt="Plugin Image" class="w-16 h-16 rounded-lg">
                    <div class="ml-4">
                        <h3 class="text-lg font-semibold text-gray-800" v-html="plugin.name"></h3>
                        <div class="flex items-center">
                            <span class="text-yellow-500 text-sm">
                                <ul class="rating-score" :data-rating="roundToNearestHalf(plugin.plugin_data.rating)">
                                    <li class="rating-score-item"></li>
                                    <li class="rating-score-item"></li>
                                    <li class="rating-score-item"></li>
                                    <li class="rating-score-item"></li>
                                    <li class="rating-score-item"></li>
                                </ul>
                            </span>
                            <span class="text-gray-500 text-sm ml-2">({{ totalRatings(plugin.plugin_data.ratings) }})</span>
                        </div>
                        <p class="text-sm text-gray-500 mt-1"> {{ plugin.plugin_data.active_installs }}+ active installations</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Confirmation Modal -->
        <div v-if="showModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center">
            <div class="bg-white p-6 rounded shadow-lg">
                <h2 class="text-lg font-semibold mb-4">Confirm Removal</h2>
                <p>Are you sure you want to remove this plugin?</p>
                <div class="mt-4 flex justify-end">
                    <button class="bg-red-500 text-white px-4 py-2 rounded mr-2" @click="removePluginNew">Yes</button>
                    <button class="bg-gray-300 text-gray-800 px-4 py-2 rounded" @click="cancelRemove">No</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import {ref, onMounted, watch} from 'vue';
import {defineProps, defineEmits, defineExpose} from 'vue';
import axios from 'axios';
import { useToast } from 'vue-toastification';

const toast = useToast();
const plugins = ref([]);
const loading = ref(true);
const error = ref(null);
const props = defineProps({
  pluginsd: {
    type: Array,
    default: () => [],
  },
});
const handleIconError = (event) => {
    const fallbackJpgUrl = `https://ps.w.org/${event.target.dataset.slug}/assets/icon-128x128.jpg`;


    if (event.target.src === fallbackJpgUrl) {

        event.target.src = 'https://ps.w.org/amp/assets/icon-128x128.png';
        event.target.onerror = null; // Prevent further loop
    } else {

        event.target.src = fallbackJpgUrl;
    }
};
const fetchUserPlugins = async () => {
    try {
        const response = await axios.get('/api/user/plugins');
        plugins.value = response.data;
    } catch (err) {
        error.value = 'Failed to load plugins.';
        console.error(err);
    } finally {
        loading.value = false;
    }
};

onMounted(() => {
    fetchUserPlugins();
});

const totalRatings = (ratings) => {
    let total = 0;
    for (const key in ratings) {
        if (Object.prototype.hasOwnProperty.call(ratings, key)) {
            total += ratings[key];
        }
    }
    return total;
};

const roundToNearestHalf = (value) => {
    value = (value * 5) / 100;
    const floorValue = Math.floor(value);
    const decimalPart = value - floorValue;
    if (decimalPart < 0.25) {
        return floorValue;
    } else if (decimalPart < 0.75) {
        return floorValue + 0.5;
    } else {
        return floorValue + 1;
    }
};

const getPluginIconUrl = (slug) => {
    return `https://ps.w.org/${slug}/assets/icon-128x128.png`;
};

const showModal = ref(false);
const pluginToRemove = ref(null);
const confirmRemove = (plugin) => {
    pluginToRemove.value = plugin;
    showModal.value = true;
};
const cancelRemove = () => {
    showModal.value = false;
    pluginToRemove.value = null;
};
const removePlugin = async (slug) => {
    try {
        await axios.delete(`/api/user/plugins/${slug}`);
        plugins.value = plugins.value.filter(plugin => plugin.slug !== slug);
        toast.success('Plugin removed successfully');
    } catch (err) {
        console.error(err);
        toast.error('Failed to remove plugin');
    }
};
const removePluginNew = async () => {
    if (pluginToRemove.value) {
        try {
            // Call the backend API to remove the plugin
            await axios.delete(`/api/user/plugins/${pluginToRemove.value.slug}`);
            // Remove the plugin from the local list
            plugins.value = plugins.value.filter(p => p.id !== pluginToRemove.value.id);
          toast.success('Plugin removed successfully');
        } catch (error) {
            console.error('Failed to remove plugin:', error);
             toast.error('Failed to remove plugin');
        }
    }
    showModal.value = false;
    pluginToRemove.value = null;
};


const refreshData = () => {
     fetchUserPlugins();
};

// Expose the refreshData method
defineExpose({
    refreshData,
});
</script>

<style scoped>
.text-yellow-500 {
    color: #f59e0b; /* Tailwind's yellow-500 color */
}
</style>



