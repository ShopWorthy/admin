import { createRouter, createWebHashHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import OrdersView from '../views/OrdersView.vue'
import UsersView from '../views/UsersView.vue'
import InventoryView from '../views/InventoryView.vue'

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/login', component: LoginView },
  { path: '/dashboard', component: DashboardView },
  { path: '/orders', component: OrdersView },
  { path: '/users', component: UsersView },
  { path: '/inventory', component: InventoryView },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

function isLoggedIn() {
  return !!localStorage.getItem('admin_logged_in')
}

router.beforeEach((to, _from, next) => {
  if (to.path === '/login') {
    if (isLoggedIn()) next({ path: '/dashboard' })
    else next()
    return
  }
  if (!isLoggedIn()) {
    next({ path: '/login' })
    return
  }
  next()
})

export default router
