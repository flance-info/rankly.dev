<template>
    <div>
        <h3 class="pt-4 text-2xl font-semibold text-gray-800 mb-4 p-6 lg:p-8 bg-white ">
            Plugins in Your Account
        </h3>
        <div v-if="loading">Loading...</div>
        <div v-else-if="error">{{ error }}</div>
        <div v-else class="bg-gray-200 bg-opacity-25 grid grid-cols-1 md:grid-cols-4 gap-6 lg:gap-8 p-6 lg:p-8">
            <div v-for="plugin in plugins" :key="plugin.id" class="bg-white rounded-lg p-4 shadow-md flex flex-col relative">
                <button
                    class="absolute top-1 right-1 w-6 h-6 flex items-center justify-center text-sm"
                    @click="removePlugin(plugin.slug)"
                    title="Remove Plugin"
                >
                    x
                </button>
                <div class="pb-2 flex items-start relative">
                    <img :src="getPluginIconUrl(plugin.slug)" alt="Plugin Image" class="w-16 h-16 rounded-lg">
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
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useToast } from 'vue-toastification';

const toast = useToast();
const plugins = ref([]);
const loading = ref(true);
const error = ref(null);

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
</script>

<style scoped>
.text-yellow-500 {
    color: #f59e0b; /* Tailwind's yellow-500 color */
}
</style>



