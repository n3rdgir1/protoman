<template>
  <div id="app">
    <div>
      <button @click="tab = 0">Chat</button>
      <button @click="tab = 1">History</button>
    </div>
    <div v-if="tab === 0">
      <ChatComponent />
    </div>
    <div v-else>
      <HistoryTree />
    </div>
  </div>
</template>

<script>
import ChatComponent from './components/ChatComponent.vue';
import HistoryTree from './components/HistoryTree.vue';

export default {
  name: 'App',
  components: {
    ChatComponent,
    HistoryTree
  },
  data() {
    return {
      tab: 0
    };
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