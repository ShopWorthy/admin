<template>
  <div>
    <nav v-if="isLoggedIn" class="navbar navbar-dark bg-dark">
      <div class="container-fluid">
        <span class="navbar-brand fw-bold">ShopWorthy Admin</span>
        <div class="d-flex gap-3">
          <router-link to="/dashboard" class="text-white text-decoration-none">Dashboard</router-link>
          <router-link to="/orders" class="text-white text-decoration-none">Orders</router-link>
          <router-link to="/users" class="text-white text-decoration-none">Users</router-link>
          <router-link to="/inventory" class="text-white text-decoration-none">Inventory</router-link>
          <button @click="logout" class="btn btn-sm btn-outline-light">Logout</button>
        </div>
      </div>
    </nav>
    <main class="container-fluid py-4">
      <router-view />
    </main>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  computed: {
    isLoggedIn() {
      return !!localStorage.getItem('admin_logged_in')
    }
  },
  methods: {
    async logout() {
      await axios.post('/admin/logout')
      localStorage.removeItem('admin_logged_in')
      this.$router.push('/login')
    }
  }
}
</script>
