<template>
    <div class=" bg-gray-900 p-6 rounded-lg">
        <!-- Delete Button -->
        <div v-if="selectedKeywords.length > 0" class="flex justify-end mb-4">
            <button @click="confirmDelete" 
                    class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md flex items-center space-x-2 text-sm">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
                <span>Delete Selected ({{ selectedKeywords.length }})</span>
            </button>
        </div>

        <table class="table-auto w-full text-left text-sm text-gray-400 bg-gray-800 rounded-lg">
            <thead class="text-gray-300 uppercase">
                <tr>
                    <th class="px-4 py-3">
                        <input type="checkbox" 
                               class="rounded border-gray-600 bg-gray-700"
                               :checked="isAllSelected"
                               @change="toggleAllSelection"
                               :indeterminate="isIndeterminate">
                    </th>
                    <th class="px-2 py-3 items-center">
                        <div class="flex justify-between items-center">
                            <span class="relative group">
                                Keyword
                                <div class="tooltip">
                                    <div class="font-medium">Tracked Keyword</div>
                                    <div class="text-gray-400">The Search Term Being Tracked For Your Plugin</div>
                                </div>
                            </span>
                            <div class="flex flex-col w-[40%] pt-[5px]">
                                <div @click="sort('keyword', 'asc')" 
                                     :class="getSortClass('keyword', 'asc')"
                                     class="cursor-pointer text-[8px] leading-[8px]">▲</div>
                                <div @click="sort('keyword', 'desc')" 
                                     :class="getSortClass('keyword', 'desc')"
                                     class="cursor-pointer text-[8px] leading-[8px]">▼</div>
                            </div>
                        </div>
                    </th>
                    <th class="px-2 py-3 items-center">
                        <div class="flex justify-between items-center">
                            <span class="relative group">
                                Position
                                <div class="tooltip">
                                    <div class="font-medium">Search Position</div>
                                    <div class="text-gray-400">Your Plugin's Position In The WordPress.org Search Results</div>
                                </div>
                            </span>
                            <div class="flex flex-col w-[25%] pt-[5px]">
                                <div @click="sort('position', 'asc')" 
                                     :class="getSortClass('position', 'asc')"
                                     class="cursor-pointer text-[8px] leading-[8px]">▲</div>
                                <div @click="sort('position', 'desc')" 
                                     :class="getSortClass('position', 'desc')"
                                     class="cursor-pointer text-[8px] leading-[8px]">▼</div>
                            </div>
                        </div>
                    </th>
                    <th class="px-4 py-3">
                        <div class="flex justify-between items-center">
                            <span class="relative group">
                                Occurrences
                                <div class="tooltip">
                                    <div class="font-medium">Keyword Count</div>
                                    <div class="text-gray-400">Number Of Times The Keyword Appears In The Readme.txt</div>
                                </div>
                            </span>
                            <div class="flex flex-col w-[20%] pt-[5px]">
                                <div @click="sort('occurrences', 'asc')" 
                                     :class="getSortClass('occurrences', 'asc')"
                                     class="cursor-pointer text-[8px] leading-[8px]">▲</div>
                                <div @click="sort('occurrences', 'desc')" 
                                     :class="getSortClass('occurrences', 'desc')"
                                     class="cursor-pointer text-[8px] leading-[8px]">▼</div>
                            </div>
                        </div>
                    </th>
                    <th class="px-4 py-3">
                        <div class="flex justify-between items-center">
                            <span class="relative group">
                                Language
                                <div class="tooltip">
                                    <div class="font-medium">Search Language</div>
                                    <div class="text-gray-400">The Language Used For Keyword Tracking</div>
                                </div>
                            </span>
                            <div class="flex flex-col w-[25%] pt-[5px]">
                                <div @click="sort('language', 'asc')" 
                                     :class="getSortClass('language', 'asc')"
                                     class="cursor-pointer text-[8px] leading-[8px]">▲</div>
                                <div @click="sort('language', 'desc')" 
                                     :class="getSortClass('language', 'desc')"
                                     class="cursor-pointer text-[8px] leading-[8px]">▼</div>
                            </div>
                        </div>
                    </th>
                    <th class="px-4 py-3">
                        <div class="flex justify-between items-center">
                            <span class="relative group">
                                Updated
                                <div class="tooltip">
                                    <div class="font-medium">Last Updated</div>
                                    <div class="text-gray-400">Most Recent Update Of The Keyword Data</div>
                                </div>
                            </span>
                            <div class="flex flex-col w-[50%] pt-[5px]">
                                <div @click="sort('updated_date', 'asc')" 
                                     :class="getSortClass('updated_date', 'asc')"
                                     class="cursor-pointer text-[8px] leading-[8px]">▲</div>
                                <div @click="sort('updated_date', 'desc')" 
                                     :class="getSortClass('updated_date', 'desc')"
                                     class="cursor-pointer text-[8px] leading-[8px]">▼</div>
                            </div>
                        </div>
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(tag, index) in sortedData" 
                    :key="index" 
                    class="border-t border-gray-700 hover:bg-gray-700">
                    <td class="px-4 py-3">
                        <input type="checkbox" 
                               class="rounded border-gray-600 bg-gray-700"
                               v-model="selectedKeywords"
                               :value="tag.keyword">
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

        <!-- Delete Confirmation Modal -->
        <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div class="bg-gray-800 p-6 rounded-lg shadow-xl max-w-md w-full mx-4">
                <h3 class="text-lg font-medium text-gray-200 mb-4">Confirm Deletion</h3>
                <p class="text-gray-400 mb-6">
                    Are you sure you want to delete {{ selectedKeywords.length }} selected keyword{{ selectedKeywords.length > 1 ? 's' : '' }}?
                    This action cannot be undone.
                </p>
                <div class="flex justify-end space-x-4">
                    <button @click="showDeleteModal = false" 
                            class="px-4 py-2 text-gray-400 hover:text-gray-200">
                        Cancel
                    </button>
                    <button @click="deleteKeywords" 
                            class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md">
                        Delete
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue';
import axios from 'axios';
import { defineEmits } from 'vue';

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
    },
    onUpdate: {
        type: Function,
        default: () => {}
    }
});

const tagData = ref([]);
const loading = ref(false);
const error = ref(null);

const sortColumn = ref('');
const sortDirection = ref('');

const selectedKeywords = ref([]);
const showDeleteModal = ref(false);

const emit = defineEmits(['keywords-updated']);

const sortedData = computed(() => {
    if (!sortColumn.value) return tagData.value;

    return [...tagData.value].sort((a, b) => {
        let aValue = a[sortColumn.value];
        let bValue = b[sortColumn.value];

        // Handle special cases
        if (sortColumn.value === 'position') {
            aValue = a.position || 0;
            bValue = b.position || 0;
        } else if (sortColumn.value === 'updated_date') {
            aValue = new Date(a.updated_date);
            bValue = new Date(b.updated_date);
        }

        if (sortDirection.value === 'asc') {
            return aValue > bValue ? 1 : -1;
        } else {
            return aValue < bValue ? 1 : -1;
        }
    });
});

const sort = (column, direction) => {
    if (sortColumn.value === column && sortDirection.value === direction) {
        // Clear sort if clicking the same column and direction
        sortColumn.value = '';
        sortDirection.value = '';
    } else {
        sortColumn.value = column;
        sortDirection.value = direction;
    }
};

const getSortClass = (column, direction) => {
    const isActive = sortColumn.value === column && sortDirection.value === direction;
    return {
        'text-gray-400 hover:text-gray-50': !isActive,
        'text-blue-500 hover:text-blue-400': isActive
    };
};

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
            emit('keyword-data', tagData.value);
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

const isAllSelected = computed(() => {
    return tagData.value.length > 0 && selectedKeywords.value.length === tagData.value.length;
});

const isIndeterminate = computed(() => {
    return selectedKeywords.value.length > 0 && !isAllSelected.value;
});

const toggleAllSelection = () => {
    if (isAllSelected.value) {
        selectedKeywords.value = [];
    } else {
        selectedKeywords.value = tagData.value.map(tag => tag.keyword);
    }
};

const confirmDelete = () => {
    showDeleteModal.value = true;
};

const deleteKeywords = async () => {
    try {
        await axios.delete('/api/keywords', {
            data: {
                slug: props.pluginSlug,
                keywords: selectedKeywords.value
            }
        });
        
        // Emit event to parent to update keywords list and average position
        emit('keywords-updated');
        
        // Clear selection
        selectedKeywords.value = [];
        showDeleteModal.value = false;
        
        // Refresh the table data
        await fetchTagData();
        
    } catch (error) {
        console.error('Error removing keywords:', error);
    }
};
</script>

<style scoped>
.tooltip {
    @apply invisible group-hover:visible absolute z-50 p-3 mt-1 
           text-xs bg-gray-900 rounded-md shadow-lg 
           border border-gray-700 capitalize;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    width: 170px;
    white-space: normal; /* Allow text to wrap */
}

.tooltip div {
    @apply leading-5;
}

.tooltip div:first-child {
    @apply mb-1;
}

.tooltip::before {
    content: '';
    @apply absolute -top-1 left-1/2 -ml-1 border-4 border-transparent 
           border-b-gray-900;
}

.group:hover .tooltip {
    @apply visible;
}

/* Add styles for checkbox indeterminate state */
input[type="checkbox"]:indeterminate {
    @apply bg-gray-500;
}
</style> 