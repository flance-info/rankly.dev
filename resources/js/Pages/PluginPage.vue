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
                       
                        <!-- Download Stats Graph -->
                        <div class="mt-6">
                            <div class="flex flex-row bg-gray-900 text-white p-6 rounded-lg shadow-lg">
                                <!-- Chart Section -->
                                <div class="w-2/3 bg-gray-800 p-4 rounded-lg">
                                    <div class="flex justify-between items-center mb-4">
                                        <h2 class="text-lg font-semibold">{{ currentChartTitle }}</h2>
                                        <select
                                            v-model="selectedTrend"
                                           
                                            class="bg-gray-700 text-white rounded-lg px-4 py-1 focus:outline-none appearance-none pr-8"
                                            style="background-image: url('data:image/svg+xml;utf8,<svg xmlns=%27http://www.w3.org/2000/svg%27 width=%2710%27 height=%275%27 viewBox=%270 0 10 5%27><path d=%27M0 0l5 5 5-5H0z%27 fill=%27%23ffffff%27/></svg>'); background-repeat: no-repeat; background-position: right 0.75rem center; background-size: 10px 5px;"
                                        >
                                            <option value="7">Last 7 Days</option>
                                            <option value="30">Last 30 Days</option>
                                            <option value="90" selected>Last 90 Days</option>
                                            <option value="365">Last Year</option>
                                        </select>

                                    </div>
                                    <canvas 
                                        v-show="activeChart === 'positionMovement'"
                                        ref="keywordChartCanvas" 
                                        id="line-chart-keyword" 
                                        class="chart-container"
                                    ></canvas>
                                    <canvas 
                                        v-show="activeChart !== 'positionMovement'"
                                        ref="lineChartCanvas" 
                                        id="line-chart" 
                                        class="chart-container"
                                    ></canvas>
                                </div>


                                <!-- Buttons Section -->
                                <div class="w-1/3 pl-6 flex flex-col justify-between">
                                    <div class="mb-4">
                                        <button @click="handleMetricClick('downloads')"
                                                :class="{
                                          'bg-gray-800 hover:bg-gray-700': activeChart !== 'downloads',
                                          'bg-gray-700 hover:bg-gray-700 shadow-lg transform scale-[1.02]': activeChart === 'downloads'
                                        }"


                                                class="flex items-center justify-between text-white font-bold py-6 px-6 rounded-lg w-full transition-all duration-200">
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
                                    <div class="mb-4">
                                        <button @click="handleMetricClick('activeInstalls')"
                                                :class="{
                                          'bg-gray-800 hover:bg-gray-700': activeChart !== 'activeInstalls',
                                          'bg-gray-700 hover:bg-gray-700 shadow-lg transform scale-[1.02]': activeChart === 'activeInstalls'
                                        }"

                                                class="flex items-center justify-between text-white font-bold py-6 px-6 rounded-lg w-full transition-all duration-200">
                                            <div>
                                                <h3 class="text-sm font-semibold text-left">Active Installs</h3>
                                                <p class="text-2xl text-left">{{ summary2.total_active_installs }}
                                             <span :class="{'text-red-500': summary2.percentage_change < 0, 'text-green-500': summary2.percentage_change >= 0}" class="text-sm">
                                                        {{ summary2.percentage_change < 0 ? '▼' : '▲' }} {{ Math.abs(summary2.percentage_change) }}%
                                                    </span>                                         
                                          
                                                    </p>
                                              
                                           
                                            </div>
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"/>
                                            </svg>
                                        </button>
                                    </div>
                                    <div class="mb-4">
                                        <button @click="handleMetricClick('averagePosition')"
                                                :class="{
                                          'bg-gray-800 hover:bg-gray-700': activeChart !== 'averagePosition',
                                          'bg-gray-700 hover:bg-gray-700 shadow-lg transform scale-[1.02]': activeChart === 'averagePosition'
                                        }"


                                                class="flex items-center justify-between text-white font-bold py-6 px-6 rounded-lg w-full transition-all duration-200">
                                            <div>
                                                <h3 class="text-sm font-semibold text-left">Average Position</h3>
                                                <p class="text-2xl text-left">
                                                    {{ summary3?.current_position ? summary3.current_position.toFixed(2) : '0.00' }}
                                                    <span :class="{'text-red-500': summary3?.percentage_change < 0, 'text-green-500': summary3?.percentage_change >= 0}" 
                                                          class="text-sm">
                                                        {{ summary3?.percentage_change < 0 ? '▼' : '▲' }} {{ Math.abs(summary3?.percentage_change || 0) }}%
                                                    </span>
                                                </p>
                                            </div>
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"/>
                                            </svg>
                                        </button>
                                    </div>
                                    <div>
                                        <button @click="handleMetricClick('positionMovement')"
                                                :class="{
                                          'bg-gray-800 hover:bg-gray-700': activeChart !== 'positionMovement',
                                          'bg-gray-700 hover:bg-gray-700 shadow-lg transform scale-[1.02]': activeChart === 'positionMovement'
                                        }"


                                                class="flex items-center justify-between text-white font-bold py-6 px-6 rounded-lg w-full transition-all duration-200">
                                            <div>
                                                <h3 class="text-sm font-semibold text-left">Plugin Position by Keywords</h3>
                                                <p class="text-2xl text-left">0 <span class="text-green-500 text-sm">▲ 5</span></p>
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
                                    <span class="text-2xl font-bold">
                                        {{ plugin.plugin_data.support_threads > 0 
                                            ? Math.round((plugin.plugin_data.support_threads_resolved / plugin.plugin_data.support_threads) * 100) 
                                            : 0 }}%
                                    </span>
                                    <svg xmlns="http://www.w3.org/2000/svg" 
                                         :class="[plugin.plugin_data.support_threads_resolved > 0 ? 'text-green-500' : 'text-red-500']"
                                         class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                        <path d="..."/>
                                    </svg>
                                </div>
                            </div>

                            <!-- Rating -->
                            <div class="flex-1 bg-gray-800 rounded-lg p-4 flex flex-col items-center justify-between text-center text-white">
                                <p class="text-sm text-gray-400">RATING</p>
                                <div class="flex items-center gap-2">
                                    <span class="text-2xl font-bold">
                                        {{ Math.round((plugin.plugin_data.rating || 0)) }}%
                                    </span>
                                    <svg xmlns="http://www.w3.org/2000/svg" 
                                         :class="[plugin.plugin_data.rating >= 80 ? 'text-green-500' : 'text-red-500']"
                                         class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                        <path d="..."/>
                                    </svg>
                                </div>
                            </div>

                            <!-- Tested Up To -->
                            <div class="flex-1 bg-gray-800 rounded-lg p-4 flex flex-col items-center justify-between text-center text-white">
                                <p class="text-sm text-gray-400">TESTED UP TO</p>
                                <div class="flex items-center gap-2">
                                    <span class="text-2xl font-bold">{{ plugin.plugin_data.tested }}</span>
                                    <svg xmlns="http://www.w3.org/2000/svg" 
                                         :class="[isTestedVersionRecent ? 'text-green-500' : 'text-red-500']"
                                         class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                        <path d="..."/>
                                    </svg>
                                </div>
                            </div>

                            <!-- Last Updated -->
                            <div class="flex-1 bg-gray-800 rounded-lg p-4 flex flex-col items-center justify-between text-center text-white">
                                <p class="text-sm text-gray-400">LAST UPDATED</p>
                                <div class="flex items-center gap-2">
                                    <span class="text-2xl font-bold">
                                      
                                        {{ formatLastUpdated(plugin.plugin_data.last_updated) }}
                                    </span>
                                    <svg xmlns="http://www.w3.org/2000/svg" 
                                         :class="[isRecentlyUpdated ? 'text-green-500' : 'text-red-500']"
                                         class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                        <path d="..."/>
                                    </svg>
                                </div>
                            </div>
                        </div>

                        <KeywordTable 
                            :plugin-slug="plugin.plugin_data.slug"
                            :selected-trend="selectedTrend"
                             :keywords="keywords"
                            @keywords-updated="handleKeywordsUpdated"                          
                        />

                        <canvas id="line-chart" class=""></canvas>
                        <canvas id="line-chart-keyword" class=""></canvas>

                        
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
import {defineProps, onMounted, ref, watch, computed, onBeforeUnmount} from 'vue';
import {Chart, registerables} from 'chart.js';
import axios from 'axios';
import KeywordTable from '@/Components/KeywordTable.vue';

const activeChart = ref('downloads');
Chart.register(...registerables);
const currentChartTitle = ref('Downloads Per Day');
const keywords = ref([]);
const summary = ref({
    total_downloads: 0,
    percentage_change: 0,
    chartData: {
        total_active_installs: 0,
        percentage_change: 0
    }
});

const summary2 = ref({
        total_active_installs: 0,
        percentage_change: 0
});

// Add summary3 for average position
const summary3 = ref({
    current_position: 0,
    percentage_change: 0
});

const props = defineProps({
    plugin: Object,
});
let pluginKeywordsData = ref(null);
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

const selectedTrend = ref('30'); // Default trend value
let chartInstance = null;
let chartInstanceSecond = null;

const chartData = {
    averagePosition: {
        title: 'Average Position',
        labels: [],
        data: [],
    },
    positionMovement: {
        title: 'Search Position by Keyword',
        labels: [],
        data: [],
    },
    activeInstalls: {
        title: 'Active Installs',
        labels: [],
        data: [],
    },
    downloads: {
        title: 'Downloads Per Day',
        labels: [],
        data: [],
    },
};

const initializeChart = (labels, data) => {
    const ctx = document.getElementById('line-chart').getContext('2d');
    
    // Convert data to numbers and find actual max value
    const numericData = data.map(Number);
    const maxValue = Math.max(...numericData);
    console.log('init Data array:', numericData);
    console.log('init Max value:', maxValue);
    
    const chartOptions = {
        activeInstalls: {
            label: 'Active Installs',
            reverse: false,
            tooltipLabel: (context) => `Active Installs: ${context.parsed.y.toFixed(0)}`
        },
        downloads: {
            label: 'Downloads',
            reverse: false,
            tooltipLabel: (context) => `Downloads: ${context.parsed.y.toFixed(0)}`
        },
        
        averagePosition: {
            label: 'Average Position',
            reverse: true,
            tooltipLabel: (context) => `Average Position: ${context.parsed.y.toFixed(2)}`,
            scales: {
                y: {
                    beginAtZero: false,
                    suggestedMin: maxValue * 2,  // Make bottom value twice the highest value
                    suggestedMax: 0,  // Start from 0 at top
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.7)'
                    },
                    reverse: true
                }
            }
        },
        positionMovement: {
            label: 'Position Movementee',
            reverse: false,
            tooltipLabel: (context) => `Movement: ${context.parsed.y.toFixed(2)}`,
            scales: {
                y: {
                    beginAtZero: false,
                    suggestedMin: maxValue * 2,  // Make bottom value twice the highest value
                    suggestedMax: 0,  // Start from 0 at top
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.7)'
                    },
                    reverse: true
                }
            }
        }
    };

    const currentOptions = chartOptions[activeChart.value] || chartOptions.downloads;

    chartInstance = new Chart(ctx, {
        type: 'line', 
        data: {
            labels,
            datasets: [
                {
                    label: currentOptions.label,
                    data,
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 2,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',  // Very transparent blue
                    pointRadius: 3,
                    fill: {
                        target: 'start',  // Fill to the origin (bottom)
                        above: 'rgba(54, 162, 235, 0.2)'  // Fill color above the line
                    },
                    tension: 0.1,
                },
            ],
        },
        options: {
            plugins: {
                legend: {
                    display: false,
                },
                tooltip: {
                    callbacks: {
                        label: currentOptions.tooltipLabel
                    }
                }
            },
            
            scales: {
                x: {
                    grid: {
                        display: true,
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.7)'
                    }
                },
                y: {
                    suggestedMin: 0,
                    suggestedMax: maxValue,  // Ensure suggestedMax is set here
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.7)'
                    },
                    reverse: currentOptions.reverse
                }
            },
        },
    });
};

const updateChart = (type) => {
    activeChart.value = type;
    currentChartTitle.value = chartData[type].title;
    
    if (chartInstance) {
        const data = chartData[type].data;
        const numericData = data.map(Number);
        const maxValue = Math.max(...numericData);
   
        
        const chartOptions = {
            averagePosition: {
                label: 'Average Position',
                reverse: true,
                tooltipLabel: (context) => `Average Position: ${context.parsed.y.toFixed(2)}`,
                scales: {
                    y: {
                        beginAtZero: false,
                        suggestedMin: maxValue * 2,
                        suggestedMax: 0,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: 'rgba(255, 255, 255, 0.7)'
                        },
                        reverse: true
                    }
                }
            },
            positionMovement: {
                label: 'Position Movement',
                reverse: true,
                tooltipLabel: (context) => `Movement: ${context.parsed.y.toFixed(2)}`,
                 scales: {
                    y: {
                        beginAtZero: false,
                        suggestedMin: maxValue * 2,  // Make bottom value twice the highest value
                        suggestedMax: 0,  // Start from 0 at top
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: 'rgba(255, 255, 255, 0.7)'
                        },
                        reverse: true
                    }
                }
            
            },
            activeInstalls: {
                label: 'Active Installs',
                reverse: false,
                tooltipLabel: (context) => `Active Installs: ${context.parsed.y.toFixed(0)}`,
                scales: {
                    y: {
                        beginAtZero: true,
                        suggestedMin: 0,
                        reverse: false
                    }
                }
            },
            downloads: {
                label: 'Downloads',
                reverse: false,
                tooltipLabel: (context) => `Downloads: ${context.parsed.y.toFixed(0)}`,
                scales: {
                    y: {
                        beginAtZero: true,
                        suggestedMin: 0,
                        reverse: false

                    }
                }
            }
        };

        const currentOptions = chartOptions[type];
        
        chartInstance.data.labels = chartData[type].labels;
        chartInstance.data.datasets[0].data = data;
        chartInstance.data.datasets[0].label = currentOptions.label;
        
        // Update the scales configuration
        chartInstance.options.scales.y = {
            ...chartInstance.options.scales.y,
            ...currentOptions.scales.y,
            suggestedMax: type === 'averagePosition' || type === 'positionMovement' ?  maxValue * 2: maxValue * 0.5,
            suggestedMin: 0
        };
        
        chartInstance.options.plugins.tooltip.callbacks.label = currentOptions.tooltipLabel;
        
        chartInstance.update();
    }
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

            // Only initialize or update chart after data is available
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

const fetchActiveInstallsData = async (slug) => {
    try {
        const response = await axios.get(`/api/plugin-active-installs/${slug}`, {
            params: {
                trend: selectedTrend.value
            },
            withCredentials: true
        });
        
        if (response.data.success) {
            const activeInstalls = response.data.data;
            const labels = Object.keys(activeInstalls);
            const data = Object.values(activeInstalls);

            chartData.activeInstalls.labels = labels;
            chartData.activeInstalls.data = data;
            summary2.value = response.data.summary;
    
            // Only update chart if it's the active type
            if (chartInstance && activeChart.value === 'activeInstalls') {
                updateChart('activeInstalls');
            }
        } else {
            console.error('Failed to fetch active installs:', response.data.message);
        }
    } catch (error) {
        console.error('An error occurred while fetching active installs:', error);
    }
};

const fetchPositionMovementData = async (slug) => {
    try {
        // First get user keywords
        const userKeywordsResponse = await axios.get(`/api/user-keywords/${slug}`);
        if (!userKeywordsResponse.data.success) {
            throw new Error('Failed to fetch user keywords');
        }

        // Then use those keywords for position movement data
        const response = await axios.post(`/api/plugin-position-movement`, {
            slug,
            keywords: userKeywordsResponse.data.keywords, // Use user keywords instead of plugin tags
            trend: selectedTrend.value
        });
        
        if (response.data.success) {
            const positionData = response.data.data;
            pluginKeywordsData = response.data.data;
            const labels = positionData.map(item => {
                return new Date(item.stat_date).toLocaleDateString('en-US', {
                    month: 'short',
                    day: 'numeric'
                });
            });
            const data = positionData.map(item => item.rank_order);
            keywordData.value = positionData;
            // Calculate summary for average position
            const currentPosition = data[data.length - 1];
            const previousPosition = data[data.length - 2] || currentPosition;
            const change = previousPosition - currentPosition;
            const percentageChange = previousPosition !== 0 
                ? ((change) / previousPosition) * 100 
                : 0;
            
            // Update summary3
            summary3.value = {
                current_position: currentPosition,
                percentage_change: Number(percentageChange.toFixed(2))
            };
            
            // Update chart data
            chartData.positionMovement.labels = labels;
            chartData.positionMovement.data = data;
            chartData.averagePosition.labels = labels;
            chartData.averagePosition.data = data;
        }
    } catch (error) {
        console.error('An error occurred while fetching position movement data:', error);
    }
};

// Add a flag to track if data has been loaded
const dataLoaded = ref({
    downloads: false,
    activeInstalls: false,
    positionMovement: false
});

// Add this ref to store keyword data
let keywordData = ref(null);

// Add this method to receive keyword data from KeywordTable
const handleKeywordData = (data) => {
    console.log('handleKeywordData', data);
    keywordData.value = dat;
    if (activeChart.value === 'positionMovement') {
      //  updateKeywordPositionChart(data);
    }
};

// Modify the existing handleMetricClick function
const handleMetricClick = (metricType) => {
    // Destroy existing charts before switching
    if (metricType !== 'positionMovement' && keywordChartInstance.value) {
        keywordChartInstance.value.destroy();
        keywordChartInstance.value = null;
    } 
    activeChart.value = metricType;
    
    // Update chart title based on metric type
    switch (metricType) {
        case 'downloads':
            currentChartTitle.value = 'Downloads Per Day';
            updateChart(metricType);
            break;
        case 'activeInstalls':
            currentChartTitle.value = 'Active Installs';
            updateChart(metricType);
            break;
        case 'averagePosition':
            currentChartTitle.value = 'Average Position';
            updateChart(metricType);
            break;
        case 'positionMovement':
            currentChartTitle.value = 'Search Position by Keyword';
            console.log('keywordData', keywordData.value);
            // Use the new keyword position chart
            if (keywordData.value.length > 0) {
                updateKeywordPositionChart(keywordData.value);
            }
            break;
    }
};

// Add ref for user keywords
const userKeywords = ref([]);

// Function to fetch user keywords
const fetchUserKeywords = async (slug) => {
    try {
        const response = await axios.get(`/api/user-keywords/${slug}`);
        if (response.data.success) {
            userKeywords.value = response.data.keywords;
        }
    } catch (error) {
        console.error('Error fetching user keywords:', error);
    }
};

// Modify onMounted to set the dataLoaded flags
onMounted(async () => {
    if (props.plugin && props.plugin.plugin_data) {
        console.log('Loading initial data for plugin:', props.plugin.plugin_data.slug);
        
        try {
            // Fetch downloads data first and initialize chart
            await fetchDownloadData(props.plugin.plugin_data.slug);
            dataLoaded.value.downloads = true;
            
            // Then fetch other data in parallel
            await Promise.all([
                fetchPositionMovementData(props.plugin.plugin_data.slug).then(() => {
                    dataLoaded.value.positionMovement = true;
                }),
                fetchActiveInstallsData(props.plugin.plugin_data.slug).then(() => {
                    dataLoaded.value.activeInstalls = true;
                })
            ]);

            // Fetch user keywords
            await fetchUserKeywords(props.plugin.plugin_data.slug);
        } catch (error) {
            console.error('Error loading initial data:', error);
        }
    } else {
        console.error('Plugin data not available');
    }
});

// Modify the trend watcher and data fetching logic
watch(selectedTrend, async () => {
    console.log('selectedTrend changed:', selectedTrend.value);
    if (props.plugin && props.plugin.plugin_data) {
        try {
            // Store current active chart type
            const currentActiveChart = activeChart.value;
            
            // Reset data loaded flags
            Object.keys(dataLoaded.value).forEach(key => {
                dataLoaded.value[key] = false;
            });
            
            // Determine which data to fetch first based on current chart type
            let firstFetch;
            switch (currentActiveChart) {
                case 'downloads':
                    firstFetch = fetchDownloadData(props.plugin.plugin_data.slug);
                    break;
                case 'activeInstalls':
                    firstFetch = fetchActiveInstallsData(props.plugin.plugin_data.slug);
                    break;
                case 'averagePosition':
                case 'positionMovement':
                    firstFetch = fetchPositionMovementData(props.plugin.plugin_data.slug);
                    break;
            }
            
            // Fetch current chart data first
            await firstFetch.then(() => {
                dataLoaded.value[currentActiveChart === 'averagePosition' ? 'positionMovement' : currentActiveChart] = true;
            });
            
            // Then fetch remaining data in parallel
            const remainingFetches = [];
            if (currentActiveChart !== 'downloads') {
                remainingFetches.push(fetchDownloadData(props.plugin.plugin_data.slug)
                    .then(() => dataLoaded.value.downloads = true));
            }
            if (currentActiveChart !== 'activeInstalls') {
                remainingFetches.push(fetchActiveInstallsData(props.plugin.plugin_data.slug)
                    .then(() => dataLoaded.value.activeInstalls = true));
            }
            if (currentActiveChart !== 'averagePosition' && currentActiveChart !== 'positionMovement') {
                remainingFetches.push(fetchPositionMovementData(props.plugin.plugin_data.slug)
                    .then(() => dataLoaded.value.positionMovement = true));
            }
            
            // Update chart immediately with current type's data
            updateChart(currentActiveChart);
            
            // Fetch remaining data in background
            await Promise.all(remainingFetches);
            
        } catch (error) {
            console.error('Error updating data with new trend:', error);
        }
    }
});

const isTestedVersionRecent = computed(() => {
    const testedVersion = pluginData.tested;
    // Compare with current WordPress version (you might want to store this in your backend)
    const currentWPVersion = '6.4'; // Update this as needed
    return testedVersion >= currentWPVersion;
});

const isRecentlyUpdated = computed(() => {
    const [datePart] = pluginData.last_updated.split(' ');
    const [year, month, day] = datePart.split('-');
    const lastUpdated = new Date(year, month - 1, day);
    
    const threeMonthsAgo = new Date();
    threeMonthsAgo.setMonth(threeMonthsAgo.getMonth() - 3);
    
    return lastUpdated >= threeMonthsAgo;
});

const formatLastUpdated = (dateString) => {
    // Handle WordPress date format (YYYY-MM-DD H:MMpm GMT)
    const [datePart] = dateString.split(' ');
    const [year, month, day] = datePart.split('-');
    
    // Create date object using parts
    const date = new Date(year, month - 1, day); // month is 0-based in JS
    
    return date.toLocaleDateString('en-GB', {
        day: 'numeric',
        month: 'short',
        year: 'numeric'
    }); // British English format puts day before month
};

const fetchPluginData = async (slug) => {
    try {
        const response = await axios.get(`/api/plugin-data/${slug}`);
        if (response.data.success) {
            console.log('Plugin Data:', response.data.data);
            // Process the plugin data as needed
        } else {
            console.error('Failed to fetch plugin data:', response.data.message);
        }
    } catch (error) {
        console.error('An error occurred while fetching plugin data:', error);
    }
};

// Update handleKeywordsUpdated
const handleKeywordsUpdated = async () => {
    await fetchUserKeywords(props.plugin.plugin_data.slug);
    await fetchPositionMovementData(props.plugin.plugin_data.slug);
    
    // Update the chart if it's showing position data
    if (activeChart.value === 'averagePosition' || activeChart.value === 'positionMovement') {
        updateChart(activeChart.value);
    }
};

// Add these new refs and methods
const keywordChartInstance = ref(null);

const updateKeywordPositionChart = (keywordData) => {
    if (keywordChartInstance.value) {
        keywordChartInstance.value.destroy();
        keywordChartInstance.value = null;
    }
    const ctx = document.getElementById('line-chart-keyword').getContext('2d');
    const keywords = keywordData.map(tag => tag.keyword);
    const positions = keywordData.map(tag => tag.position || 0);

    // Destroy both chart instances before creating a new one
   
  
    let dummyDatas = {
        dates: ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05'],
        keywords: {
            'wordpress': [5, 3, 4, 2, 1],
            'plugin': [3, 4, 2, 3, 2],
            'elementor': [1, 2, 3, 2, 1],
            'page builder': [4, 3, 2, 1, 2]
        }
    };
   let dummyData = transformKeywordData(pluginKeywordsData);
    console.log('  dummyData ',  dummyData );
   let labels = dummyData.dates.map(date => new Date(date).toLocaleDateString('en-US', {
                month: 'short',
                day: 'numeric'
            }));
          let  dataPoints = Object.entries(dummyData.keywords).map(([keyword, positions]) => ({
                label: keyword,
                data: positions,
                borderColor: `hsl(${Math.random() * 360}, 70%, 50%)`, // Random color for each line
                backgroundColor: 'transparent',
                borderWidth: 2,
                tension: 0.1,
                fill: false,
                pointRadius: 4,
            }));

    // Update or create chart
    if (chartInstanceSecond) {
        // Update existing chart
      chartInstanceSecond.data.labels = labels;
      chartInstanceSecond.data.datasets[0].data = dataPoints;
        
      chartInstanceSecond.update();
    } else {
        chartInstanceSecond = new Chart(ctx, {
        type: 'line', 
        data: {
            labels: dummyData.dates.map(date => new Date(date).toLocaleDateString('en-US', {
                month: 'short',
                day: 'numeric'
            })),
            datasets: Object.entries(dummyData.keywords).map(([keyword, positions]) => ({
                label: keyword,
                data: positions,
                borderColor: `hsl(${Math.random() * 360}, 70%, 50%)`, // Random color for each line
                backgroundColor: 'transparent',
                borderWidth: 2,
                tension: 0.1,
                fill: false,
                pointRadius: 4,
            })),
        },
        options: {
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom',
                    align: 'start',
                    labels: {
                        color: 'rgba(255, 255, 255, 0.7)',
                        padding: 20,
                        usePointStyle: true, // Uses points instead of boxes in legend
                        pointStyle: 'circle',
                        font: {
                            size: 11
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.dataset.label || '';
                            const value = context.formattedValue;
                            return `${label}: ${value}`;
                        }
                    }
                }
            },
           
            scales: {
                x: {
                    grid: {
                        display: true,
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.7)'
                    }
                },
                y: {                 
                   
                   
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.7)',
                        stepSize: 1, // Force step size to be 1
                        callback: function(value) {
                            if (Number.isInteger(value)) {
                                return value;
                            }
                        }
                    },
                    reverse: true
                }
            },
        },
    });
    }
};

// Watch for keyword changes if necessary
watch(keywordData, (newData) => {
    if (activeChart.value === 'positionMovement') {
        updateKeywordPositionChart(newData);
    }
});

// Destroy chart instance when component unmounts to prevent memory leaks
onBeforeUnmount(() => {
    if (keywordChartInstance.value) {
        keywordChartInstance.value.destroy();
    }
});

// Clean up Chart instance on component unmount

function transformKeywordData(pluginKeywordsData) {
    // Sort entries by date
    const sortedEntries = [...pluginKeywordsData].sort((a, b) => 
        new Date(a.stat_date) - new Date(b.stat_date)
    );

    // Extract and format dates
    const dates = sortedEntries.map(entry => 
        new Date(entry.stat_date).toLocaleDateString('en-US', { 
            month: 'short', 
            day: 'numeric' 
        })
    );

    // Collect all unique keywords
    const keywords = {};
    sortedEntries.forEach(entry => {
        entry.raw_data.forEach(keyword => {
            const slug = keyword.keyword_slug;
            if (!keywords[slug]) {
                keywords[slug] = [];
            }
        });
    });

    // Initialize arrays for each keyword
    Object.keys(keywords).forEach(keyword => {
        keywords[keyword] = new Array(dates.length).fill(null);
    });

    // Populate keyword rankings
    sortedEntries.forEach((entry, dateIndex) => {
        entry.raw_data.forEach(keyword => {
            const slug = keyword.keyword_slug;
            keywords[slug][dateIndex] = keyword.rank_order;
        });
    });

    return {
        dates: dates,
        keywords: keywords
    };
}

// Usage


</script>


<style scoped>
.text-yellow-500 {
    color: #f59e0b; /* Tailwind's yellow-500 color */
}

/* Add these styles if needed */
.chart-container {
    display: block;
    position: relative;
    height: 400px;
    width: 100%;
}
</style>
