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
                                <div class="w-2/3 w-2/3 bg-gray-800  p-4 rounded-lg">
                                    <h2 class="text-lg font-semibold mb-4">{{ currentChartTitle }}</h2>
                                    <canvas id="line-chart" class=""></canvas>
                                </div>

                                <!-- Buttons Section -->
                                <div class="w-1/3 pl-6 flex flex-col justify-between">
                                    <div class="mb-4">
                                        <button @click="updateChart('averagePosition')" class="flex items-center justify-between bg-gray-800 hover:bg-gray-700 text-white font-bold py-6 px-6 rounded-lg w-full">
                                            <div>
                                                <h3 class="text-sm font-semibold">Average Position</h3>
                                                <p class="text-2xl">2320.80 <span class="text-red-500 text-sm">▼ 13.20</span></p>
                                            </div>
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18" />
                                            </svg>
                                        </button>
                                    </div>
                                    <div class="mb-4">
                                        <button @click="updateChart('positionMovement')" class="flex items-center justify-between bg-gray-800 hover:bg-gray-700 text-white font-bold py-6 px-6 rounded-lg w-full">
                                            <div>
                                                <h3 class="text-sm font-semibold">Position Movement</h3>
                                                <p class="text-2xl">0 <span class="text-green-500 text-sm">▲ 5</span></p>
                                            </div>
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18" />
                                            </svg>
                                        </button>
                                    </div>
                                    <div class="mb-4">
                                        <button @click="updateChart('activeInstalls')" class="flex items-center justify-between bg-gray-800 hover:bg-gray-700 text-white font-bold py-6 px-6 rounded-lg w-full">
                                            <div>
                                                <h3 class="text-sm font-semibold">Active Installs</h3>
                                                <p class="text-2xl">12</p>
                                            </div>
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18" />
                                            </svg>
                                        </button>
                                    </div>
                                    <div>
                                        <button @click="updateChart('downloads')" class="flex items-center justify-between bg-gray-800 hover:bg-gray-700 text-white font-bold py-6 px-6 rounded-lg w-full">
                                            <div>
                                                <h3 class="text-sm font-semibold">Downloads</h3>
                                                <p class="text-2xl">4 <span class="text-red-500 text-sm">▼ 56%</span></p>
                                            </div>
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18" />
                                            </svg>
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
