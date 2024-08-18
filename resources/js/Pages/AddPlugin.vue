<template>
    <div class="p-6 lg:p-8 bg-gray-100 min-h-screen">
        <!-- Breadcrumb or Title -->
        <div class="mb-4 text-gray-600">
            <h1 class="text-xl font-bold">Plugins > Add plugin</h1>
        </div>

        <!-- Search Input -->
        <div class="flex items-center mb-8">
            <input
                type="text"
                placeholder="Search plugin by name, slug or WordPress URL"
                class="w-full p-3 border rounded-l-md border-gray-300 focus:outline-none"
                v-model="searchQuery"
            />
            <button
                class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-r-md"
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
</template>

<script>
export default {
    data() {
        return {
            searchQuery: ''
        };
    },
    methods: {
        searchPlugin() {
            // Logic to handle the search functionality
            if (this.searchQuery) {
                console.log(`Searching for: ${this.searchQuery}`);
                // You can add your search logic here, or navigate to another page, etc.
            } else {
                alert("Please enter a search query.");
            }
        }
    }
}
</script>

<style scoped>
/* Add any custom styles here */
</style>
