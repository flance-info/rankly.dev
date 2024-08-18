<script setup>
// Import necessary components
import AppLayout from '@/Layouts/AppLayout.vue';
import DeleteTeamForm from '@/Pages/Teams/Partials/DeleteTeamForm.vue';
import SectionBorder from '@/Components/SectionBorder.vue';
import TeamMemberManager from '@/Pages/Teams/Partials/TeamMemberManager.vue';
import UpdateTeamNameForm from '@/Pages/Teams/Partials/UpdateTeamNameForm.vue';

// Define the props using the defineProps macro
const props = defineProps({
    team: {
        type: Object,
        required: true,
    },
    availableRoles: {
        type: Array,
        required: true,
    },
    permissions: {
        type: Object,
        required: true,
    },
});
</script>

<template>
    <AppLayout :title="`Team Settings - ${team.name}`">



    </AppLayout>
</template>
