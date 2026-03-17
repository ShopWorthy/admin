<template>
  <div>
    <h2 class="mb-4">Dashboard</h2>
    <div class="row g-4">
      <div class="col-md-4">
        <div class="card border-0 shadow-sm">
          <div class="card-body text-center">
            <h5 class="text-muted">Total Orders</h5>
            <h2 class="display-4">{{ stats.orders }}</h2>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card border-0 shadow-sm">
          <div class="card-body text-center">
            <h5 class="text-muted">Users</h5>
            <h2 class="display-4">{{ stats.users }}</h2>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card border-0 shadow-sm">
          <div class="card-body text-center">
            <h5 class="text-muted">Inventory Items</h5>
            <h2 class="display-4">{{ stats.inventory_items }}</h2>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return { stats: { orders: 0, users: 0, inventory_items: 0 } }
  },
  async mounted() {
    try {
      const res = await axios.get('/admin/api/stats')
      this.stats = res.data
    } catch {}
  }
}
</script>
