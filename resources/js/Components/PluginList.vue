<template>
  <div class="p-6 bg-white border border-gray-200 rounded-lg shadow-md">
    <h2 class="text-2xl font-semibold text-gray-800 mb-4">Your Plugins</h2>
    <ul>
      <li v-for="plugin in plugins" :key="plugin.id" class="mb-4">
        <div class="p-4 bg-gray-100 rounded-lg">
          <h3 class="text-lg font-bold text-gray-700">{{ plugin.name }}</h3>
          <p class="text-sm text-gray-600">{{ plugin.description }}</p>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  plugins: {
    type: Array,
    required: true
  }
});
</script>

<style scoped>
/* Add any additional styles here */
</style> 