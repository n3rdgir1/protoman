<template>
  <div id="app">
    <div>
      <button @click="tab = 0">Chat</button>
      <button @click="tab = 1">History</button>
    </div>
    <div v-if="tab === 0">
      <ChatComponent messages="messages" threadId="threadId"/>
    </div>
    <div v-else>
      <HistoryTree threadId="threadId"/>
    </div>
  </div>
</template>

<script>
import ChatComponent from './components/ChatComponent.vue';
import HistoryTree from './components/HistoryTree.vue';
import { v4 as uuidv4 } from 'uuid'
import { marked } from 'marked'

export default {
  name: 'App',
  components: {
    ChatComponent,
    HistoryTree
  },
  data() {
    return {
      terminalOutput: '',
      threadId: '',
      tab: 0,
      messages: [],
    };
  },
  methods: {
    updateTerminalOutput(newOutput) {
      this.terminalOutput += newOutput + '\n';
    },
    newThread() {
      this.threadId = uuidv4()
      localStorage.setItem('threadId', this.threadId)
      console.log('New thread ID:', this.threadId)
      this.terminalOutput = ''
    },
    addMessage(message, sender, id) {
      const messageToAdd = {
        id: id || Date.now() + 1,
        text: message,
        sender: sender,
        html: marked(message)
      }
      this.messages.push(messageToAdd)
      this.$nextTick(() => {
        this.scrollToBottom()
      })
    },
  },
  mounted() {
    const storedThreadId = localStorage.getItem('threadId')
    if (storedThreadId) {
      this.threadId = storedThreadId
      console.log('Restored thread ID from localStorage:', this.threadId)
    }

    this.$socket.on('chat', (message) => {
      this.addMessage.addMessage(message, 'bot')
    })

    this.$socket.on('debug', (message) => {
      this.addMessage.addMessage(message, 'debug')
    })

    this.$socket.on('terminal', (message) => {
      this.updateTerminalOutput(message)
    })
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>