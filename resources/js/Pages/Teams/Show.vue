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
        <template #header>
            <h2 class="font-semibold text-xl text-gray-800 leading-tight">
                Team Settings for {{ team.name }} (ID: {{ team.id }})
            </h2>
        </template>

        <div>
            <div class="max-w-7xl mx-auto py-10 sm:px-6 lg:px-8">
                <UpdateTeamNameForm :team="team.id" :permissions="permissions" />

                <TeamMemberManager
                    class="mt-10 sm:mt-0"
                    :team="team.id"
                    :available-roles="availableRoles"
                    :user-permissions="permissions"
                />

                <template v-if="permissions.canDeleteTeam && !team.personal_team">
                    <SectionBorder />

                    <DeleteTeamForm class="mt-10 sm:mt-0" :team="team.id" />
                </template>
            </div>
        </div>
    </AppLayout>
</template>
