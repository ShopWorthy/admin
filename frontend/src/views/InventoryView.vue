<template>
  <div>
    <h2 class="mb-4">Inventory</h2>
    <div class="table-responsive">
      <table class="table table-hover">
        <thead class="table-dark">
          <tr>
            <th>Product ID</th><th>Name</th><th>SKU</th><th>Stock</th><th>Reorder At</th><th>Location</th><th>Updated</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.id" :class="item.stock_count <= item.reorder_threshold ? 'table-warning' : ''">
            <td>{{ item.product_id }}</td>
            <td>{{ item.product_name }}</td>
            <td>{{ item.sku }}</td>
            <td><strong>{{ item.stock_count }}</strong></td>
            <td>{{ item.reorder_threshold }}</td>
            <td>{{ item.warehouse_location }}</td>
            <td>{{ item.last_updated }}</td>
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
    return { items: [] }
  },
  async mounted() {
    try {
      const res = await axios.get('/admin/api/inventory')
      this.items = res.data
    } catch {}
  }
}
</script>
