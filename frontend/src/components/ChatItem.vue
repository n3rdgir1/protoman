<template>
  <div :class="['chat-item', senderClass]">
    {{ text }}
  </div>
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
}
.chat-item-bot {
  background-color: #e0e0e0;
  text-align: left;
}
.chat-item-user {
  background-color: #0084ff;
  color: white;
  text-align: right;
}

.chat-item-debug {
  background-color: #ffa200;
  text-align: right;
}
/* Add more sender-specific styles as needed */
</style>
