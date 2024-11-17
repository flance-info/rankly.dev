<template>
    <div>
        <h3 class="pt-4 text-2xl font-semibold text-gray-800 mb-4 p-6 lg:p-8 bg-white ">
            Plugins You Can Add to Your Account
        </h3>
        <div class="bg-gray-200 bg-opacity-25 grid grid-cols-1 md:grid-cols-4 gap-6 lg:gap-8 p-6 lg:p-8">
            <div v-for="plugin in plugins" :key="plugin.id" class="bg-white rounded-lg p-4 shadow-md flex flex-col relative">
                <!-- Remove Button -->
                <button
                    class="absolute top-1 right-1 w-6 h-6 pb-6 pl-6 pt-2.5 pr-4 flex items-center justify-center text-sm z-10"
                    @click="removePlugin(plugin.slug)"
                    title="Remove Plugin"
                >
                    x
                </button>
                <div class="pb-2 flex items-start relative">
                    <!-- Plugin Icon -->
                     <img :src="getPluginIconUrl(plugin.slug)"   @error="handleIconError"
                          :data-slug="plugin.slug"
                         alt="Plugin Image" class="w-16 h-16 rounded-lg">
                    <!-- Plugin Info -->
                    <div class="ml-4">
                        <h3 class="text-lg font-semibold text-gray-800" v-html="plugin.name"></h3>
                        <div class="flex items-center">
                        <span class="text-yellow-500 text-sm">
                            <ul class="rating-score" :data-rating="roundToNearestHalf(plugin.rating)">
                                <li class="rating-score-item"></li>
                                <li class="rating-score-item"></li>
                                <li class="rating-score-item"></li>
                                <li class="rating-score-item"></li>
                                <li class="rating-score-item"></li>
                            </ul>
                        </span>
                            <span class="text-gray-500 text-sm ml-2">({{ totalRatings(plugin.ratings) }})</span>
                        </div>
                        <p class="text-sm text-gray-500 mt-1"> {{ plugin.active_installs }}+ active installations</p>
                    </div>

                </div>
                <!-- Add to Account Button -->
                <div class="mt-auto flex justify-center">
                    <button
                        class="bg-blue-500 text-white px-4 py-2 rounded-lg shadow hover:bg-blue-600"
                        @click="addPluginsToAccount(plugin.slug)"
                    >
                        Add to Account
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>


<script setup>
import {defineProps, defineEmits} from 'vue';
import axios from 'axios';
import {useToast} from 'vue-toastification';

const toast = useToast();
const emit = defineEmits(['plugin-added']);

const props = defineProps({
    plugins: {
        type: Object,
        required: true,
    },
});
const handleIconError = (event) => {
    const fallbackJpgUrl = `https://ps.w.org/${event.target.dataset.slug}/assets/icon-128x128.jpg`;

console.log('te',event.target.dataset.slug);
    if (event.target.src === fallbackJpgUrl) {

        event.target.src = 'https://ps.w.org/amp/assets/icon-128x128.png';
        event.target.onerror = null; // Prevent further loop
    } else {

        event.target.src = fallbackJpgUrl;
    }
};
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

// Function to remove a plugin by its slug
const removePlugin = (slug) => {
    delete props.plugins[slug]; // Remove the plugin from the object
    savePluginsToLocal(); // Save updated plugins to local storage
};

// Function to save plugins to local storage
const savePluginsToLocal = () => {
    localStorage.setItem('plugins', JSON.stringify(props.plugins));
};

// Function to add a plugin to the user account
const addPluginsToAccount = async (slug) => {
    try {
        const plugin = props.plugins[slug];

        if (!plugin) {
            toast.error('Plugin not found!');
            return;
        }

        const response = await axios.post('/api/user/plugin', {
            plugin,
        });
        const message = response.data.message ? response.data.message : 'Plugin successfully added to your account!';
        toast.success(message);

        // Emit event to notify parent component
        emit('plugin-added', plugin);

        console.log('Response:', response.data);
    } catch (error) {
        console.error('Error adding plugin:', error);
        toast.error('Failed to add plugin to your account.');
    }
};


</script>


<style scoped>

</style>
