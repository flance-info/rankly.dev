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
                        Priority
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
                <tr v-for="(tag, index) in tags" :key="index" class="border-t border-gray-700 hover:bg-gray-700">
                    <td class="px-4 py-3">
                        <input type="checkbox" class="rounded border-gray-600 bg-gray-700">
                    </td>
                    <td class="px-4 py-3">{{ tag }}</td>
                    <td class="px-4 py-3 flex items-center gap-2">
                        <span>{{ getPositionForTag(tag) }}</span>
                        <span :class="getPositionChangeClass(tag)" class="text-sm">{{ getPositionChangeSymbol(tag) }} {{ getPositionChange(tag) }}</span>
                    </td>
                    <td class="px-4 py-3">{{ getPriorityForTag(tag) }}</td>
                    <td class="px-4 py-3">{{ getOccurrencesForTag(tag) }}</td>
                    <td class="px-4 py-3">{{ getLanguageForTag(tag) }}</td>
                    <td class="px-4 py-3">{{ getTrackedForTag(tag) }}</td>
                    <td class="px-4 py-3">{{ getUpdatedForTag(tag) }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup>
import { defineProps } from 'vue';

// Define props to receive tags
const props = defineProps({
    tags: Array
});

// Define methods to get data for each tag
const getPositionForTag = (tag) => {
    // Logic to get position for the tag
    return 'Position Data';
};

const getPositionChangeClass = (tag) => {
    // Logic to determine class based on position change
    return 'text-green-500'; // or 'text-red-500'
};

const getPositionChangeSymbol = (tag) => {
    // Logic to determine symbol based on position change
    return '▲'; // or '▼'
};

const getPositionChange = (tag) => {
    // Logic to get position change for the tag
    return 'Change Data';
};

const getPriorityForTag = (tag) => {
    // Logic to get priority for the tag
    return 'Priority Data';
};

const getOccurrencesForTag = (tag) => {
    // Logic to get occurrences for the tag
    return 'Occurrences Data';
};

const getLanguageForTag = (tag) => {
    // Logic to get language for the tag
    return 'Language Data';
};

const getTrackedForTag = (tag) => {
    // Logic to get tracked status for the tag
    return 'Tracked Data';
};

const getUpdatedForTag = (tag) => {
    // Logic to get updated date for the tag
    return 'Updated Data';
};
</script> 