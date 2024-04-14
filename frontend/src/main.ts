import '@/assets/main.css'
import 'vue3-toastify/dist/index.css'
import 'vue-pdf-embed/dist/style/index.css'
import 'vue-pdf-embed/dist/style/annotationLayer.css'
import 'vue-pdf-embed/dist/style/textLayer.css'

import { createApp } from 'vue'
import App from '@/App.vue'
import router from '@/router'
import { store, key } from '@/store'
import Vue3Toastify, { type ToastContainerOptions } from 'vue3-toastify'

const app = createApp(App)

app.use(router)
app.use(store, key)

app.use(Vue3Toastify, {
  autoClose: 3000,
  position: 'bottom-right'
} as ToastContainerOptions)

app.mount('#app')
