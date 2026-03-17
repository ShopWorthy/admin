<template>
  <div>
    <h2 class="mb-4">Users</h2>
    <div class="table-responsive">
      <table class="table table-hover">
        <thead class="table-dark">
          <tr>
            <th>ID</th><th>Username</th><th>Email</th><th>Role</th><th>Created</th><th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.username }}</td>
            <td>{{ user.email }}</td>
            <td><span :class="user.role === 'admin' ? 'badge bg-danger' : 'badge bg-secondary'">{{ user.role }}</span></td>
            <td>{{ user.created_at }}</td>
            <td>
              <button class="btn btn-sm btn-outline-danger" @click="deleteUser(user.id)">Delete</button>
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
    return { users: [] }
  },
  async mounted() {
    try {
      const res = await axios.get('/admin/api/users')
      this.users = res.data
    } catch {}
  },
  methods: {
    async deleteUser(id) {
      if (!confirm('Delete this user?')) return
      await axios.delete(`/admin/api/users/${id}`)
      this.users = this.users.filter(u => u.id !== id)
    }
  }
}
</script>
