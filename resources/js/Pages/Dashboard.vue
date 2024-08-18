<script setup>
import AppLayout from '@/Layouts/AppLayout.vue';
import Main from '@/Components/Main.vue';
</script>

<template>
    <AppLayout title="Plugins">
        <template #header>
            <h1 class="font-semibold text-xl text-gray-800 leading-tight">
                Plugins
            </h1>
        </template>

        <div class="py-12">
            <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
                <div class="bg-white overflow-hidden shadow-xl sm:rounded-lg">
                    <Main />
                </div>
            </div>
        </div>
    </AppLayout>
</template>
