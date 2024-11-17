<script setup>
import ApplicationLogo from '@/Components/ApplicationLogo.vue';
import {router} from "@inertiajs/vue3";

</script>

<template>
    <div>
        <div class="p-6 lg:p-8 bg-white border-b border-gray-200">
         <!--   <h2 class="mt-8 text-2xl font-medium text-gray-900">
                Plugins
            </h2>
            !-->

            <!-- Plugins Button -->
            <div class="mt-4">
                <button
                    class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                    @click="handlePluginButtonClick">
                    + Add Plugin
                </button>


            </div>
        </div>
    </div>

</template>

<script>

export default {
    methods: {
        handlePluginButtonClick() {
            router.get(route('add-plugin'));

        }
    }

}
</script>

