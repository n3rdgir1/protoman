<template>
  <pre :class="['chat-item', senderClass]">{{ text }}</pre>
</template>

<script>
export default {
  name: 'ChatItem',
  props: {
    sender: {
      type: String,
      required: true
    },
    text: {
      type: String,
      required: true
    }
  },
  computed: {
    senderClass() {
      return `chat-item-${this.sender}`;
    }
  }
}
</script>

<style scoped>
.chat-item {
  padding: 10px;
  margin: 5px 0;
  border-radius: 5px;
  max-width: calc(100% - 80px);
  word-break: break-word;
  text-wrap: wrap;
}
.chat-item-bot {
  background-color: #e0e0e0;
  text-align: left;
}
.chat-item-user {
  background-color: #0084ff;
  color: white;
  text-align: right;
  margin-left: auto;
}
.chat-item-debug {
  background-color: #ffa200;
  text-align: left;
}
</style>
