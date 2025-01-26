<template>
    <div class="overflow-x-auto bg-gray-900 p-6 rounded-lg">
        <table class="table-auto w-full text-left text-sm text-gray-400 bg-gray-800 rounded-lg">
            <thead class="text-gray-300 uppercase">
                <tr>
                    <th class="px-4 py-3">
                        <input type="checkbox" class="rounded border-gray-600 bg-gray-700">
                    </th>
                    <th class="px-2 py-3 items-center relative group">
                        Keyword
                        <div class="ml-2 flex flex-col float-right w-[40%] pt-[5px]">
                            <div class="cursor-pointer text-gray-400 hover:text-gray-50 text-[8px] leading-[8px]">▲</div>
                            <div class="cursor-pointer text-gray-400 hover:text-gray-50 text-[8px] leading-[8px]">▼</div>
                        </div>
                        <div class="tooltip">
                            <div class="font-medium">The keyword being </div>
                            <div class="text-gray-400">tracked for the plugin</div>
                        </div>
                    </th>
                    <th class="px-2 py-3 items-center relative group">
                        Position
                        <div class="ml-2 flex flex-col float-right w-[25%] pt-[5px]">
                            <div class="cursor-pointer text-gray-400 hover:text-gray-50 text-[8px] leading-[8px]">▲</div>
                            <div class="cursor-pointer text-gray-400 hover:text-gray-50 text-[8px] leading-[8px]">▼</div>
                        </div>
                        <div class="tooltip">
                            <div class="font-medium">Search Position</div>
                            <div class="text-gray-400">In The WordPress.org Search Results</div>
                        </div>
                    </th>
                    <th class="px-4 py-3 relative group">
                        Occurrences
                        <div class="ml-2 flex flex-col float-right w-[20%] pt-[5px]">
                            <div class="cursor-pointer text-gray-400 hover:text-gray-50 text-[8px] leading-[8px]">▲</div>
                            <div class="cursor-pointer text-gray-400 hover:text-gray-50 text-[8px] leading-[8px]">▼</div>
                        </div>
                        <div class="tooltip">
                            <div class="font-medium">Keyword Count</div>
                            <div class="text-gray-400">Number Of Times The Keyword Appears In The Readme.txt</div>
                        </div>
                    </th>
                    <th class="px-4 py-3 relative group">
                        Language
                        <div class="ml-2 flex flex-col float-right w-[25%] pt-[5px]">
                            <div class="cursor-pointer text-gray-400 hover:text-gray-50 text-[8px] leading-[8px]">▲</div>
                            <div class="cursor-pointer text-gray-400 hover:text-gray-50 text-[8px] leading-[8px]">▼</div>
                        </div>
                        <div class="tooltip">
                            <div class="font-medium">Search Language</div>
                            <div class="text-gray-400">The Language Used For Keyword Tracking</div>
                        </div>
                    </th>
                    <th class="px-4 py-3 relative group">
                        Updated
                        <div class="ml-2 flex flex-col float-right w-[50%] pt-[5px]">
                            <div class="cursor-pointer text-gray-400 hover:text-gray-50 text-[8px] leading-[8px]">▲</div>
                            <div class="cursor-pointer text-gray-400 hover:text-gray-50 text-[8px] leading-[8px]">▼</div>
                        </div>
                        <div class="tooltip">
                            <div class="font-medium">Last Updated</div>
                            <div class="text-gray-400">Most Recent Update Of The Keyword Data</div>
                        </div>
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(tag, index) in tagData" :key="index" class="border-t border-gray-700 hover:bg-gray-700">
                    <td class="px-4 py-3">
                        <input type="checkbox" class="rounded border-gray-600 bg-gray-700">
                    </td>
                    <td class="px-4 py-3">{{ tag.keyword }}</td>
                    <td class="px-4 py-3 flex items-center gap-2">
                        <span>{{ tag.position || 0 }}</span>
                        <span v-if="tag.position" :class="getChangeClass(tag.position_change)" class="text-sm">
                            {{ getChangeSymbol(tag.position_change) }} 
                            {{ Math.abs(tag.position_change) }}
                        </span>
                    </td>
                    <td class="px-4 py-3">{{ tag.occurrences }}</td>
                    <td class="px-4 py-3">{{ tag.language }}</td>
                    <td class="px-4 py-3">{{ formatDate(tag.updated_at) }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<style scoped>
.tooltip {
    @apply invisible group-hover:visible absolute z-50 p-3 mt-1 
           text-xs bg-gray-900 rounded-md shadow-lg 
           whitespace-nowrap border border-gray-700 capitalize;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
}

.tooltip div {
    @apply leading-5;
}

.tooltip div:first-child {
    @apply mb-1;
}

/* Add a small arrow to the tooltip */
.tooltip::before {
    content: '';
    @apply absolute -top-1 left-1/2 -ml-1 border-4 border-transparent 
           border-b-gray-900;
}

/* Ensure the tooltip container has proper positioning */
.relative {
    position: relative;
}

.group:hover .tooltip {
    @apply visible;
}
</style>

<script setup>
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';

const props = defineProps({
    pluginSlug: {
        type: String,
        required: true
    },
    selectedTrend: {
        type: String,
        required: true
    },
    keywords: {
        type: Array,
        required: true
    }
});

const tagData = ref([]);
const loading = ref(false);
const error = ref(null);

// Fetch tag data from backend
const fetchTagData = async () => {
    loading.value = true;
    error.value = null;
    
    try {
        const response = await axios.post(`/api/plugin-keywords`, {
            slug: props.pluginSlug,
            keywords: props.keywords,
            trend: props.selectedTrend
        });
        
        if (response.data.success) {
            tagData.value = response.data.data.map(tag => ({
                keyword: tag.keyword,
                position: tag.current_position,
                position_change: tag.position_change,
                occurrences: tag.occurrences,
                language: tag.language,
                updated_at: tag.updated_at
            }));
        } else {
            error.value = 'Failed to fetch keyword data';
        }
    } catch (err) {
        console.error('Error fetching keyword data:', err);
        error.value = 'Error loading keyword data';
    } finally {
        loading.value = false;
    }
};

// Helper functions
const getChangeClass = (change) => {
    return change >= 0 ? 'text-green-500' : 'text-red-500';
};

const getChangeSymbol = (change) => {
    return change >= 0 ? '▲' : '▼';
};

const formatDate = (date) => {
    if (!date) return 'N/A';
    try {
        return new Date(date).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    } catch (err) {
        return 'Invalid date';
    }
};

// Watch for changes in trend selection
watch(() => props.selectedTrend, () => {
    fetchTagData();
});

// Initial data fetch
onMounted(() => {
    fetchTagData();
});
</script> 