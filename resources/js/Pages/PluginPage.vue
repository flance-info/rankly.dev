<template>
  <div v-if="plugin">
    <h1 class="text-2xl font-bold">{{ plugin.name }}</h1>
    <img :src="plugin.iconUrl" alt="Plugin Icon" class="w-32 h-32 my-4">
    <p class="text-gray-700">{{ plugin.description }}</p>
    <div class="mt-4">
      <span class="text-yellow-500">Rating: {{ plugin.rating }}</span>
      <span class="ml-4 text-gray-500">Active Installs: {{ plugin.activeInstalls }}</span>
    </div>
  </div>
  <div v-else>
    <p>Loading plugin information...</p>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  plugin: Object
});
</script>

<style scoped>
.text-yellow-500 {
  color: #f59e0b; /* Tailwind's yellow-500 color */
}
</style>
