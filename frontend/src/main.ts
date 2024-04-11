import '@/assets/main.css'
import 'vue3-toastify/dist/index.css'

import { createApp } from 'vue'
import App from '@/App.vue'
import router from '@/router'
import { store, key } from '@/store'
import Vue3Toastify, { type ToastContainerOptions } from 'vue3-toastify'

const app = createApp(App)

app.use(router)
app.use(store, key)

app.use(Vue3Toastify, {
  autoClose: 3000
} as ToastContainerOptions)

app.mount('#app')
