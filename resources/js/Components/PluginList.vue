<template>
  <div>
    <h3 class="pt-4 text-2xl font-semibold text-gray-800 mb-4 p-6 lg:p-8 bg-white ">
        Plugins You Can Add to Your Account
    </h3>
    <div class="bg-gray-200 bg-opacity-25 grid grid-cols-1 md:grid-cols-4 gap-6 lg:gap-8 p-6 lg:p-8">
      <div v-for="plugin in plugins" :key="plugin.id" class="bg-white rounded-lg shadow-md p-4 flex items-start">
        <!-- Uncomment and replace with actual image path if available -->
        <!-- <img :src="plugin.image" alt="Plugin Image" class="w-16 h-16 rounded-lg"> -->
        <div class="ml-4">
          <h3 class="text-lg font-semibold text-gray-800" v-html="plugin.name"></h3>
          <div class="flex items-center">
            <span class="text-yellow-500 text-sm">★★★★★</span>
            <span class="text-gray-500 text-sm ml-2">(1)</span>
          </div>
          <p class="text-sm text-gray-500 mt-1">{{ plugin.activeInstallations }} active installations</p>
        </div>
      </div>
    </div>
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
