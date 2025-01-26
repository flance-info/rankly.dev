<template>
    <div class="overflow-x-auto bg-gray-900 p-6 rounded-lg">
        <table class="table-auto w-full text-left text-sm text-gray-400 bg-gray-800 rounded-lg">
            <thead class="text-gray-300 uppercase">
                <tr>
                    <th class="px-4 py-3">
                        <input type="checkbox" class="rounded border-gray-600 bg-gray-700">
                    </th>
                    <th class="px-2 py-3 items-center">
                        Keyword
                        <div class="ml-2 flex flex-col float-right w-[40%] pt-[5px]">
                            <div class="cursor-pointer text-gray-400 hover:text-gray-50 text-[8px] leading-[8px]">▲</div>
                            <div class="cursor-pointer text-gray-400 hover:text-gray-50 text-[8px] leading-[8px]">▼</div>
                        </div>
                    </th>
                    <th class="px-2 py-3 items-center">
                        Position
                        <div class="ml-2 flex flex-col float-right w-[25%] pt-[5px]">
                            <div class="cursor-pointer text-gray-400 hover:text-gray-50 text-[8px] leading-[8px]">▲</div>
                            <div class="cursor-pointer text-gray-400 hover:text-gray-50 text-[8px] leading-[8px]">▼</div>
                        </div>
                    </th>
                    <th class="px-4 py-3">
                        Occurrences
                        <div class="ml-2 flex flex-col float-right w-[20%] pt-[5px]">
                            <div class="cursor-pointer text-gray-400 hover:text-gray-50 text-[8px] leading-[8px]">▲</div>
                            <div class="cursor-pointer text-gray-400 hover:text-gray-50 text-[8px] leading-[8px]">▼</div>
                        </div>
                    </th>
                    <th class="px-4 py-3">
                        Language
                        <div class="ml-2 flex flex-col float-right w-[25%] pt-[5px]">
                            <div class="cursor-pointer text-gray-400 hover:text-gray-50 text-[8px] leading-[8px]">▲</div>
                            <div class="cursor-pointer text-gray-400 hover:text-gray-50 text-[8px] leading-[8px]">▼</div>
                        </div>
                    </th>
                    <th class="px-4 py-3">
                        Tracked
                        <div class="ml-2 flex flex-col float-right w-[50%] pt-[5px]">
                            <div class="cursor-pointer text-gray-400 hover:text-gray-50 text-[8px] leading-[8px]">▲</div>
                            <div class="cursor-pointer text-gray-400 hover:text-gray-50 text-[8px] leading-[8px]">▼</div>
                        </div>
                    </th>
                    <th class="px-4 py-3">
                        Updated
                        <div class="ml-2 flex flex-col float-right w-[50%] pt-[5px]">
                            <div class="cursor-pointer text-gray-400 hover:text-gray-50 text-[8px] leading-[8px]">▲</div>
                            <div class="cursor-pointer text-gray-400 hover:text-gray-50 text-[8px] leading-[8px]">▼</div>
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
                        <span>{{ tag.position }}</span>
                        <span :class="getChangeClass(tag.position_change)" class="text-sm">
                            {{ getChangeSymbol(tag.position_change) }} 
                            {{ Math.abs(tag.position_change) }}
                        </span>
                    </td>
                    <td class="px-4 py-3">{{ tag.occurrences }}</td>
                    <td class="px-4 py-3">{{ tag.language }}</td>
                    <td class="px-4 py-3">{{ formatDate(tag.tracked_date) }}</td>
                    <td class="px-4 py-3">{{ formatDate(tag.updated_date) }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

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
                tracked_date: tag.tracked_at,
                updated_date: tag.updated_at
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
        const dateObj = new Date(date);
        const now = new Date();
        const diffTime = Math.abs(now - dateObj);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        
        if (diffDays === 0) return 'Today';
        if (diffDays === 1) return 'Yesterday';
        if (diffDays < 7) return `${diffDays} days ago`;
        if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
        if (diffDays < 365) return `${Math.floor(diffDays / 30)} months ago`;
        return `${Math.floor(diffDays / 365)} years ago`;
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