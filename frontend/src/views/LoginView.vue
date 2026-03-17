<template>
  <div class="row justify-content-center mt-5">
    <div class="col-md-4">
      <div class="card shadow">
        <div class="card-body p-4">
          <h4 class="card-title text-center mb-4">ShopWorthy Admin</h4>
          <form @submit.prevent="login">
            <div class="mb-3">
              <label class="form-label">Username</label>
              <input v-model="form.username" type="text" class="form-control" required />
            </div>
            <div class="mb-3">
              <label class="form-label">Password</label>
              <input v-model="form.password" type="password" class="form-control" required />
            </div>
            <div v-if="error" class="alert alert-danger py-2">{{ error }}</div>
            <button type="submit" class="btn btn-dark w-100" :disabled="loading">
              {{ loading ? 'Signing in...' : 'Sign In' }}
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return { form: { username: '', password: '' }, error: '', loading: false }
  },
  methods: {
    async login() {
      this.loading = true
      this.error = ''
      try {
        await axios.post('/admin/login', this.form)
        localStorage.setItem('admin_logged_in', '1')
        this.$router.push('/dashboard')
      } catch {
        this.error = 'Invalid credentials'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
