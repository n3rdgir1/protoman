import { createApp } from 'vue'
import App from './App.vue'
import { io } from 'socket.io-client'

const socket = io('http://127.0.0.1:5000')

socket.on('connect', () => {
  console.info('Connected to WebSocket server')
})

const app = createApp(App)
app.config.globalProperties.$socket = socket

app.mount('#app')
