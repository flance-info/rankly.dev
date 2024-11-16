<template>
    <div>
        <div class="p-6 lg:p-8 bg-white border-b border-gray-200">
            <div class="mb-4 text-gray-600">
                <!-- <h2 class="text-xl font-bold">Plugins > Add plugin</h2> -->
            </div>

            <!-- Search Input -->
            <div class="flex items-center mb-8">
                <input
                    type="text"
                    placeholder="Search plugin by name, slug or WordPress URL"
                    class="w-full p-3 border-t border-b border-l rounded-l-md border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    v-model="searchQuery"
                />
                <button
                    class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-r-md border-t border-b border-r border-blue-500"
                    @click="searchPlugin"
                >
                    Search
                </button>
            </div>

            <!-- Placeholder Content -->
            <div class="flex flex-col items-center justify-center">
                <p class="text-gray-600">Use search to find and add a plugin.</p>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import {useToast} from "vue-toastification";

export default {
    data() {
        return {
            searchQuery: '',
        };
    },
    methods: {
        searchPlugin() {
            const toast = useToast();
            if (this.searchQuery) {
                axios.post('/api/search-plugin', {slug: this.searchQuery})
                    .then(response => {
                        console.log('Plugin added:', response.data);
                        const newPlugin = response.data.plugin;
                         // Show success message
                        const message = response.data.message ? response.data.message : 'Plugin Info received successfully';
                        toast.success(message);
                        this.$emit('plugin-added', newPlugin);
                    })
                    .catch(error => {
                          console.log(error);
                        const errorMessage = error.response.data?.error || 'Could not add plugin.';
                        toast.error(`Error: ${errorMessage}`);
                    });
            } else {
                toast.warning("Please enter a search query.");
            }
        }
    }

}
</script>

<style scoped>
/* Add any custom styles here */
</style>
