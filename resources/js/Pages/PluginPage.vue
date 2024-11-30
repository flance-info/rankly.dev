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
                            <canvas id="line-chart" width="857" height="375" style="display: block; width: 686px; height: 300px;" class="chartjs-render-monitor"></canvas>
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
import {defineProps, onMounted} from 'vue';
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

// Function to initialize the chart
const initializeChart = () => {
    const ctx = document.getElementById('line-chart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Aug 6', 'Sep 1', 'Sep 10', 'Sep 19', 'Oct 1', 'Oct 10', 'Oct 19', 'Nov 1', 'Nov 10', 'Nov 19'], // Example labels
            datasets: [{
                label: 'Downloads Per Day',
                data: [2326, 194980, 184340, 174700, 154560, 144920, 134280, 113860, 103220, 93380], // Example data
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 2,

                backgroundColor: "#000",
                pointRadius: 3,
                fill: false,
                tension: 0.1
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return `Downloads: ${context.raw}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: true,

                    }
                },
                y: {
                    beginAtZero: true,

                }
            }
        }
    });
};

onMounted(() => {
    initializeChart();
});
</script>


<style scoped>
    .text-yellow-500 {
    color: #f59e0b; /* Tailwind's yellow-500 color */
}
</style>
