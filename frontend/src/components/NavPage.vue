<script>
export default {
    data() {
        return {
            loggedIn: false
        };
    },

    mounted() {
        this.loggedIn = !!localStorage.getItem("token");
    },

    methods: {
        logoutUser() {
            localStorage.clear();
            this.loggedIn = false;
            this.$router.push("/login");   // redirect to login page
        }
    }
};
</script>

<template>
    <nav class="navbar bg-primary-subtle">
        <div class="container-fluid">
            <RouterLink class="navbar-brand" to="/dashboard">
                E-card App
            </RouterLink>

            <button
                v-if="loggedIn"
                @click="logoutUser"
                class="btn btn-danger"
            >
                Logout
            </button>
        </div>
    </nav>
</template>

<style></style>
