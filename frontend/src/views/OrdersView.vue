<template>
  <div>
    <h2 class="mb-4">Orders</h2>
    <div class="table-responsive">
      <table class="table table-hover">
        <thead class="table-dark">
          <tr>
            <th>ID</th><th>User ID</th><th>Status</th><th>Total</th><th>Notes</th><th>Created</th><th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="order in orders" :key="order.id">
            <td>{{ order.id }}</td>
            <td>{{ order.user_id }}</td>
            <td>
              <select v-model="order.status" @change="updateStatus(order)" class="form-select form-select-sm w-auto">
                <option v-for="s in statuses" :key="s" :value="s">{{ s }}</option>
              </select>
            </td>
            <td>${{ Number(order.total).toFixed(2) }}</td>
            <!-- Renders HTML from order notes — stored XSS vector -->
            <td v-html="order.notes"></td>
            <td>{{ order.created_at }}</td>
            <td>
              <button class="btn btn-sm btn-outline-primary" @click="updateStatus(order)">Save</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return { orders: [], statuses: ['pending','paid','shipped','delivered','cancelled'] }
  },
  async mounted() {
    try {
      const res = await axios.get('/admin/api/orders')
      this.orders = res.data
    } catch {}
  },
  methods: {
    async updateStatus(order) {
      await axios.put(`/admin/api/orders/${order.id}/status`, { status: order.status })
    }
  }
}
</script>
