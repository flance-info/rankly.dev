<template>
    <div>
        <h3 class="pt-4 text-2xl font-semibold text-gray-800 mb-4 p-6 lg:p-8 bg-white ">
            Plugins You Can Add to Your Account
        </h3>
        <div class="bg-gray-200 bg-opacity-25 grid grid-cols-1 md:grid-cols-4 gap-6 lg:gap-8 p-6 lg:p-8">
            <div v-for="plugin in plugins" :key="plugin.id" class="bg-white rounded-lg shadow-md p-4 flex items-start relative">

                <!-- Remove Button -->
                 <button
                    class="absolute top-1 right-1  w-6 h-6 flex items-center justify-center text-sm"
                    @click="removePlugin(plugin.slug)"
                    title="Remove Plugin"
                >
                    x
                </button>

                <!-- Plugin Icon -->
                <img :src="getPluginIconUrl(plugin.slug)" alt="Plugin Image" class="w-16 h-16 rounded-lg">

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
        </div>
    </div>
</template>


<script setup>
import {defineProps} from 'vue';


const props = defineProps({
    plugins: {
        type: Object,
        required: true
    }
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

const calculateStars = (rating) => {
    const fullStars = Math.floor((rating / 100) * 5); // Full stars based on rating
    const hasHalfStar = (rating % 20) >= 10; // Check if there's a half star
    return {fullStars, hasHalfStar};
};

function roundToNearestHalf(value) {
    value = (value * 5) / 100;
    console.log(value);
    const floorValue = Math.floor(value);
    const decimalPart = value - floorValue;
    console.log(floorValue, decimalPart);
    if (decimalPart < 0.25) {
        return floorValue;
    } else if (decimalPart < 0.75) {
        return floorValue + 0.5;
    } else {
        return floorValue + 1;
    }
}

function getPluginIconUrl(slug) {
    return `https://ps.w.org/${slug}/assets/icon-128x128.png`;
}
</script>

<style scoped>

</style>
