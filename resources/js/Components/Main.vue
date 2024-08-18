<script setup>
import ApplicationLogo from '@/Components/ApplicationLogo.vue';
import {Inertia as InertiaCore} from '@inertiajs/inertia';


</script>

<template>
    <div>
        <div class="p-6 lg:p-8 bg-white border-b border-gray-200">
            <h1 class="mt-8 text-2xl font-medium text-gray-900">
                Plugins
            </h1>

            <!-- Plugins Button -->
            <div class="mt-4">
                <button
                    class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                    @click="handlePluginButtonClick">
                    + Add Plugin
                </button>


            </div>
        </div>

        <div class="bg-gray-200 bg-opacity-25 grid grid-cols-1 md:grid-cols-4 gap-6 lg:gap-8 p-6 lg:p-8">
            <!-- Plugin Card -->
            <div class="bg-white rounded-lg shadow-md p-4 flex items-start">
                <!--      <img src="path_to_plugin_image.png" alt="Plugin Image" class="w-16 h-16 rounded-lg"> !-->
                <div class="ml-4">
                    <h3 class="text-lg font-semibold text-gray-800">BS Maps - Google Maps Plugin</h3>
                    <div class="flex items-center">
                        <span class="text-yellow-500 text-sm">★★★★★</span>
                        <span class="text-gray-500 text-sm ml-2">(1)</span>
                    </div>
                    <p class="text-sm text-gray-500 mt-1">60+ active installations</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>


import {router} from "@inertiajs/vue3";

export default {
    methods: {
        handlePluginButtonClick() {
            router.get(route('add-plugin'));

        }
    }

}
</script>

