<!-- <script>
export default {
    methods: {
        toLogin: function() {
            this.$router.push("/login")
        }
    }
}
</script> -->

<template>
    <button @click="this.$router.push('/login')" class="btn bt-success-subtle btns">
        login
    </button>

    <button class="btn bg-primary-subtle btns">
        Signup
    </button>
</template>