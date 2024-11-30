<template>
    <AppLayout title="PluginPage">
        <template #header>
            <div class="font-semibold  text-sm text-gray-800 leading-tight pb-2">
                Plugins > {{ plugin.slug }}
            </div>

        </template>

        <div class="py-12 max-w-7xl mx-auto sm:px-6 lg:px-8 flex flex-row items-center gap-4">
            <img :src="getPluginIconUrl(plugin.slug)" @error="handleIconError"
                 :data-slug="plugin.slug"
                 alt="Plugin Image" class="w-16 h-16">
            <h1 v-if="plugin" class="font-semibold text-lg text-gray-800 leading-tight">
                {{ decodeHTML(plugin.name) }}
            </h1>
        </div>

        <!-- Plugin List Component -->
        <div class="py-4">
            <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
                <div class="bg-blue-50 overflow-hidden shadow-xl sm:rounded-lg">
                    <div v-if="plugin">


                        <p class="text-gray-700">{{ decodeHTML(plugin.description) }}</p>
                        <div class="mt-4">
                            <span class="text-yellow-500">Rating: {{ pluginData.rating }}</span>
                            <span class="ml-4 text-gray-500">Active Installs: {{ pluginData.activeInstalls }}</span>
                        </div>

                        <!-- Download Stats Graph -->
                        <div class="mt-6">
                            <div class="flex flex-row bg-gray-900 text-white p-6 rounded-lg shadow-lg">
                                <!-- Chart Section -->
                                <div class="w-2/3">
                                    <h2 class="text-lg font-semibold mb-4">{{ currentChartTitle }}</h2>
                                    <canvas id="line-chart" class="bg-gray-800 p-4 rounded-lg"></canvas>
                                </div>

                                <!-- Buttons Section -->
                                <div class="w-1/3 pl-6">
                                    <div class="mb-4">
                                        <h3 class="text-sm font-semibold">Average Position</h3>
                                        <button @click="updateChart('averagePosition')" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-2">
                                            View
                                        </button>
                                    </div>
                                    <div class="mb-4">
                                        <h3 class="text-sm font-semibold">Position Movement</h3>
                                        <button @click="updateChart('positionMovement')" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-2">
                                            View
                                        </button>
                                    </div>
                                    <div class="mb-4">
                                        <h3 class="text-sm font-semibold">Active Installs</h3>
                                        <button @click="updateChart('activeInstalls')" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-2">
                                            View
                                        </button>
                                    </div>
                                    <div>
                                        <h3 class="text-sm font-semibold">Downloads</h3>
                                        <button @click="updateChart('downloads')" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-2">
                                            View
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div v-else>
                        <p>Loading plugin information...</p>
                    </div>
                 
                </div>
            </div>
        </div>
        <div class="py-6">
            <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
                <div class="bg-white overflow-hidden shadow-xl sm:rounded-lg">


                </div>
            </div>
        </div>
    </AppLayout>
</template>


<script setup>
import AppLayout from '@/Layouts/AppLayout.vue';
import {defineProps, onMounted, ref} from 'vue';
import {Chart, registerables} from 'chart.js';

// Register all necessary components
Chart.register(...registerables);

const props = defineProps({
    plugin: Object
});

const getPluginIconUrl = (slug) => {
    return `https://ps.w.org/${slug}/assets/icon-128x128.png`;
};

const pluginData = props.plugin.plugin_data;

const handleIconError = (event) => {
    const fallbackJpgUrl = `https://ps.w.org/${event.target.dataset.slug}/assets/icon-128x128.jpg`;
    if (event.target.src === fallbackJpgUrl) {
        event.target.src = 'https://ps.w.org/amp/assets/icon-128x128.png';
        event.target.onerror = null; // Prevent further loop
    } else {
        event.target.src = fallbackJpgUrl;
    }
};

const decodeHTML = (html) => {
    const txt = document.createElement('textarea');
    txt.innerHTML = html;
    return txt.value;
};

const currentChartTitle = ref('Downloads Per Day');
let chartInstance;

const chartData = {
    averagePosition: {
        title: 'Average Position',
        data: [10, 12, 8, 9, 7, 6, 5, 4]
    },
    positionMovement: {
        title: 'Position Movement',
        data: [0, 1, -1, 2, -2, 3, -3, 4]
    },
    activeInstalls: {
        title: 'Active Installs',
        data: [100, 150, 130, 170, 160, 180, 190, 200]
    },
    downloads: {
        title: 'Downloads Per Day',
        data: [0, 1, 0, 0, 0, 2, 0, 0]
    }
};

const initializeChart = (data) => {
    const ctx = document.getElementById('line-chart').getContext('2d');
    chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Nov 22', 'Nov 23', 'Nov 24', 'Nov 25', 'Nov 26', 'Nov 27', 'Nov 28', 'Nov 29'],
            datasets: [{
                label: currentChartTitle.value,
                data: data,
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 2,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                pointRadius: 3,
                fill: true,
                tension: 0.1
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    grid: {
                        display: true
                    }
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });
};

const updateChart = (type) => {
    currentChartTitle.value = chartData[type].title;
    chartInstance.data.datasets[0].data = chartData[type].data;
    chartInstance.update();
};

onMounted(() => {
    initializeChart(chartData.downloads.data);
});
</script>


<style scoped>
    .text-yellow-500 {
    color: #f59e0b; /* Tailwind's yellow-500 color */
}
</style>
