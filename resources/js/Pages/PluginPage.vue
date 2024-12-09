<template>
    <AppLayout title="PluginPage">
        <template #header>
            <div class="font-semibold  text-sm text-white leading-tight pb-2">
                Plugins > {{ plugin.slug }}
            </div>

        </template>

        <div class="py-12 max-w-7xl mx-auto sm:px-6 lg:px-8 flex flex-row items-center gap-4">
            <img :src="getPluginIconUrl(plugin.slug)" @error="handleIconError"
                 :data-slug="plugin.slug"
                 alt="Plugin Image" class="w-16 h-16">
            <h1 v-if="plugin" class="font-semibold text-lg text-white leading-tight">
                {{ decodeHTML(plugin.name) }}
            </h1>
        </div>

        <!-- Plugin List Component -->
        <div class="py-4">
            <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
                <div class="bg-gray-900 overflow-hidden shadow-xl sm:rounded-lg">
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
                                <div class="w-2/3 bg-gray-800 p-4 rounded-lg">
                                    <div class="flex justify-between items-center mb-4">
                                        <h2 class="text-lg font-semibold">{{ currentChartTitle }}</h2>
                                        <select
                                            v-model="selectedTrend"
                                            @change="fetchDownloadData(pluginData.slug)"
                                            class="bg-gray-700 text-white rounded-lg px-4 py-1 focus:outline-none appearance-none pr-8"
                                            style="background-image: url('data:image/svg+xml;utf8,<svg xmlns=%27http://www.w3.org/2000/svg%27 width=%2710%27 height=%275%27 viewBox=%270 0 10 5%27><path d=%27M0 0l5 5 5-5H0z%27 fill=%27%23ffffff%27/></svg>'); background-repeat: no-repeat; background-position: right 0.75rem center; background-size: 10px 5px;"
                                        >
                                            <option value="7">Last 7 Days</option>
                                            <option value="30">Last 30 Days</option>
                                            <option value="90" selected>Last 90 Days</option>
                                            <option value="365">Last Year</option>
                                        </select>

                                    </div>
                                    <canvas id="line-chart" class=""></canvas>
                                </div>


                                <!-- Buttons Section -->
                                <div class="w-1/3 pl-6 flex flex-col justify-between">
                                    <div class="mb-4">
                                        <button @click="updateChart('averagePosition')"
                                                :class="{
                                          'bg-gray-700': activeChart === 'averagePosition',
                                          'bg-gray-800': activeChart !== 'averagePosition',
                                        }"


                                                class="flex items-center justify-between bg-gray-800 hover:bg-gray-700 text-white font-bold py-6 px-6 rounded-lg w-full">
                                            <div>
                                                <h3 class="text-sm font-semibold text-left">Average Position</h3>
                                                <p class="text-2xl text-left">2320.80 <span class="text-red-500 text-sm">▼ 13.20</span></p>
                                            </div>
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"/>
                                            </svg>
                                        </button>
                                    </div>
                                    <div class="mb-4">
                                        <button @click="updateChart('positionMovement')"
                                                :class="{
                                          'bg-gray-700': activeChart === 'positionMovement',
                                          'bg-gray-800': activeChart !== 'positionMovement',
                                        }"


                                                class="flex items-center justify-between bg-gray-800 hover:bg-gray-700 text-white font-bold py-6 px-6 rounded-lg w-full">
                                            <div>
                                                <h3 class="text-sm font-semibold text-left">Position Movement</h3>
                                                <p class="text-2xl text-left">0 <span class="text-green-500 text-sm">▲ 5</span></p>
                                            </div>
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"/>
                                            </svg>
                                        </button>
                                    </div>
                                    <div class="mb-4">
                                        <button @click="updateChart('activeInstalls')"
                                                :class="{
                                          'bg-gray-700': activeChart === 'activeInstalls',
                                          'bg-gray-800': activeChart !== 'activeInstalls',
                                        }"

                                                class="flex items-center justify-between bg-gray-800 hover:bg-gray-700 text-white font-bold py-6 px-6 rounded-lg w-full">
                                            <div>
                                                <h3 class="text-sm font-semibold text-left">Active Installs</h3>
                                                <p class="text-2xl text-left">12</p>
                                            </div>
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"/>
                                            </svg>
                                        </button>
                                    </div>
                                    <div>
                                        <button
                                            :class="{
                                          'bg-gray-700': activeChart === 'downloads',
                                          'bg-gray-800': activeChart !== 'downloads',
                                        }"


                                            @click="updateChart('downloads')" class="flex items-center justify-between bg-gray-800 hover:bg-gray-700 text-white font-bold py-6 px-6 rounded-lg w-full">
                                            <div>
                                                <h3 class="text-sm font-semibold text-left">Downloads</h3>
                                                <p class="text-2xl text-left">
                                                    {{ summary.total_downloads }}
                                                    <span :class="{'text-red-500': summary.percentage_change < 0, 'text-green-500': summary.percentage_change >= 0}" class="text-sm">
                                                        {{ summary.percentage_change < 0 ? '▼' : '▲' }} {{ Math.abs(summary.percentage_change) }}%
                                                    </span>
                                                </p>

                                            </div>
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"/>
                                            </svg>
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="flex gap-4 bg-gray-900 p-6 pt-1 pb-1">
                            <!-- Support Resolved -->
                            <div class="flex-1 bg-gray-800 rounded-lg p-4 flex flex-col items-center justify-between text-center text-white">
                                <p class="text-sm text-gray-400">SUPPORT RESOLVED</p>
                                <div class="flex items-center gap-2">
                                    <span class="text-2xl font-bold">0%</span>
                                    <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                                        <path d="..."/>
                                    </svg>
                                </div>
                            </div>

                            <!-- Rating -->
                            <div class="flex-1 bg-gray-800 rounded-lg p-4 flex flex-col items-center justify-between text-center text-white">
                                <p class="text-sm text-gray-400">RATING</p>
                                <div class="flex items-center gap-2">
                                    <span class="text-2xl font-bold">100%</span>
                                    <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                                        <path d="..."/>
                                    </svg>
                                </div>
                            </div>

                            <!-- Tested Up To -->
                            <div class="flex-1 bg-gray-800 rounded-lg p-4 flex flex-col items-center justify-between text-center text-white">
                                <p class="text-sm text-gray-400">TESTED UP TO</p>
                                <div class="flex items-center gap-2">
                                    <span class="text-2xl font-bold">6.4.5</span>
                                    <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                                        <path d="..."/>
                                    </svg>
                                </div>
                            </div>

                            <!-- Last Updated -->
                            <div class="flex-1 bg-gray-800 rounded-lg p-4 flex flex-col items-center justify-between text-center text-white">
                                <p class="text-sm text-gray-400">LAST UPDATED</p>
                                <div class="flex items-center gap-2">
                                    <span class="text-2xl font-bold">13 Dec 2023</span>
                                    <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                                        <path d="..."/>
                                    </svg>
                                </div>
                            </div>
                        </div>

                        <div class="overflow-x-auto bg-gray-900 p-6 rounded-lg">
                            <table class="table-auto w-full text-left text-sm text-gray-400  bg-gray-800 rounded-lg">
                                <thead class=" text-gray-300 uppercase">
                                <tr>
                                    <th class="px-4 py-3">
                                        <input type="checkbox" class="rounded border-gray-600 bg-gray-700">
                                    </th>
                                    <th class="px-2 py-3  items-center">
                                        Keyword
                                        <div class="ml-2 flex flex-col float-right w-[40%] pt-[5px]">
                                            <div class="cursor-pointer text-gray-400 hover:text-gray-50 text-[8px] leading-[8px]">
                                                ▲

                                            </div>
                                            <div class="cursor-pointer text-gray-400 hover:text-gray-50 text-[8px] leading-[8px]">
                                                ▼
                                            </div>
                                        </div>

                                    </th>
                                    <th class="px-2 py-3 items-center">
                                        Position
                                        <div class="ml-2 flex flex-col float-right w-[25%] pt-[5px]">
                                            <div class="cursor-pointer text-gray-400 hover:text-gray-50 text-[8px] leading-[8px]">
                                                ▲

                                            </div>
                                            <div class="cursor-pointer text-gray-400 hover:text-gray-50 text-[8px] leading-[8px]">
                                                ▼
                                            </div>
                                        </div>

                                    </th>
                                    <th class="px-4 py-3">
                                        Priority
                                        <div class="ml-2 flex flex-col float-right w-[25%] pt-[5px]">
                                            <div class="cursor-pointer text-gray-400 hover:text-gray-50 text-[8px] leading-[8px]">
                                                ▲

                                            </div>
                                            <div class="cursor-pointer text-gray-400 hover:text-gray-50 text-[8px] leading-[8px]">
                                                ▼
                                            </div>
                                        </div>


                                    </th>
                                    <th class="px-4 py-3">
                                        Occurrences
                                        <div class="ml-2 flex flex-col float-right w-[20%] pt-[5px]">
                                            <div class="cursor-pointer text-gray-400 hover:text-gray-50 text-[8px] leading-[8px]">
                                                ▲

                                            </div>
                                            <div class="cursor-pointer text-gray-400 hover:text-gray-50 text-[8px] leading-[8px]">
                                                ▼
                                            </div>
                                        </div>

                                    </th>
                                    <th class="px-4 py-3">
                                        Language
                                        <div class="ml-2 flex flex-col float-right w-[25%] pt-[5px]">
                                            <div class="cursor-pointer text-gray-400 hover:text-gray-50 text-[8px] leading-[8px]">
                                                ▲

                                            </div>
                                            <div class="cursor-pointer text-gray-400 hover:text-gray-50 text-[8px] leading-[8px]">
                                                ▼
                                            </div>
                                        </div>


                                    </th>
                                    <th class="px-4 py-3">
                                        Tracked
                                        <div class="ml-2 flex flex-col float-right w-[50%] pt-[5px]">
                                            <div class="cursor-pointer text-gray-400 hover:text-gray-50 text-[8px] leading-[8px]">
                                                ▲

                                            </div>
                                            <div class="cursor-pointer text-gray-400 hover:text-gray-50 text-[8px] leading-[8px]">
                                                ▼
                                            </div>
                                        </div>

                                    </th>
                                    <th class="px-4 py-3">
                                        Updated
                                        <div class="ml-2 flex flex-col float-right w-[50%] pt-[5px]">
                                            <div class="cursor-pointer text-gray-400 hover:text-gray-50 text-[8px] leading-[8px]">
                                                ▲

                                            </div>
                                            <div class="cursor-pointer text-gray-400 hover:text-gray-50 text-[8px] leading-[8px]">
                                                ▼
                                            </div>
                                        </div>


                                    </th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr class=" border-t border-gray-700 hover:bg-gray-700">
                                    <td class="px-4 py-3">
                                        <input type="checkbox" class="rounded border-gray-600 bg-gray-700">
                                    </td>
                                    <td class="px-4 py-3">woocommerce</td>
                                    <td class="px-4 py-3 flex items-center gap-2">
                                        <span>9915</span>


                                        <span class="text-green-500 text-sm">▲ 38</span>
                                    </td>
                                    <td class="px-4 py-3">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-gray-300" viewBox="0 0 20 20" fill="currentColor">
                                            <path d="M10 15a1 1 0 011-1h4a1 1 0 110 2h-4a1 1 0 01-1-1zM10 5a1 1 0 011-1h4a1 1 0 110 2h-4a1 1 0 01-1-1zM7 12a1 1 0 100-2 1 1 0 000 2z"/>
                                        </svg>
                                    </td>
                                    <td class="px-4 py-3">3</td>
                                    <td class="px-4 py-3">English</td>
                                    <td class="px-4 py-3">November 25, 2024</td>
                                    <td class="px-4 py-3">November 30, 2024</td>
                                </tr>
                                <tr class=" border-t border-gray-700 hover:bg-gray-700">
                                    <td class="px-4 py-3">
                                        <input type="checkbox" class="rounded border-gray-600 bg-gray-700">
                                    </td>
                                    <td class="px-4 py-3">add to cart</td>
                                    <td class="px-4 py-3 flex items-center gap-2">
                                        <span>419</span>
                                        <span class="text-red-500 text-sm">▼ 8</span>
                                    </td>
                                    <td class="px-4 py-3">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-gray-300" viewBox="0 0 20 20" fill="currentColor">
                                            <path d="M10 15a1 1 0 011-1h4a1 1 0 110 2h-4a1 1 0 01-1-1zM10 5a1 1 0 011-1h4a1 1 0 110 2h-4a1 1 0 01-1-1zM7 12a1 1 0 100-2 1 1 0 000 2z"/>
                                        </svg>
                                    </td>
                                    <td class="px-4 py-3">3</td>
                                    <td class="px-4 py-3">English</td>
                                    <td class="px-4 py-3">November 25, 2024</td>
                                    <td class="px-4 py-3">November 30, 2024</td>
                                </tr>
                                <!-- Repeat more rows as necessary -->
                                </tbody>
                            </table>
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
import axios from 'axios';

const activeChart = ref(null);
// Register all necessary components
Chart.register(...registerables);
const summary = ref({
    total_downloads: 0,
    percentage_change: 0,
});

const props = defineProps({
    plugin: Object,
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

const selectedTrend = ref('7'); // Default trend value
const currentChartTitle = ref('Downloads Per Day');
let chartInstance;

const chartData = {
    averagePosition: {
        title: 'Average Position',
        labels: ['Nov 22', 'Nov 23', 'Nov 24', 'Nov 25', 'Nov 26', 'Nov 27', 'Nov 28', 'Nov 29'],
        data: [10, 12, 8, 9, 7, 6, 5, 4],
    },
    positionMovement: {
        title: 'Position Movement',
        labels: ['Nov 22', 'Nov 23', 'Nov 24', 'Nov 25', 'Nov 26', 'Nov 27', 'Nov 28', 'Nov 29'],
        data: [0, 1, -1, 2, -2, 3, -3, 4],
    },
    activeInstalls: {
        title: 'Active Installs',
        labels: ['Nov 22', 'Nov 23', 'Nov 24', 'Nov 25', 'Nov 26', 'Nov 27', 'Nov 28', 'Nov 29'],
        data: [100, 150, 130, 170, 160, 180, 190, 200],
    },
    downloads: {
        title: 'Downloads Per Day',
        labels: [],
        data: [],
    },
};

const initializeChart = (labels, data) => {
    const ctx = document.getElementById('line-chart').getContext('2d');
    chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels,
            datasets: [
                {
                    label: currentChartTitle.value,
                    data,
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 2,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    pointRadius: 3,
                    fill: true,
                    tension: 0.1,
                },
            ],
        },
        options: {
            plugins: {
                legend: {
                    display: false,
                },
            },
            scales: {
                x: {
                    grid: {
                        display: true,
                    },
                },
                y: {
                    beginAtZero: true,
                },
            },
        },
    });
};

const updateChart = (type) => {
    activeChart.value = type;
    currentChartTitle.value = chartData[type].title;
    chartInstance.data.labels = chartData[type].labels;
    chartInstance.data.datasets[0].data = chartData[type].data;
    chartInstance.update();
};

const fetchDownloadData = async (slug) => {
    try {
        const response = await axios.get(`/api/plugin-stats/${slug}`, {
            params: {
                trend: selectedTrend.value,
            },
        });
        if (response.data.success) {
            const downloads = response.data.data;
            const labels = Object.keys(downloads);
            const data = Object.values(downloads);

            chartData.downloads.labels = labels;
            chartData.downloads.data = data;

           summary.value = response.data.summary;

            if (!chartInstance) {
                initializeChart(labels, data);
            } else if (activeChart.value === 'downloads') {
                updateChart('downloads');
            }
        } else {
            console.error('Failed to fetch plugin stats:', response.data.message);
        }
    } catch (error) {
        console.error('An error occurred while fetching plugin stats:', error);
    }
};

onMounted(() => {
    initializeChart(chartData.averagePosition.labels, chartData.averagePosition.data);
    fetchDownloadData(pluginData.slug);
});
</script>


<style scoped>
.text-yellow-500 {
    color: #f59e0b; /* Tailwind's yellow-500 color */
}
</style>
