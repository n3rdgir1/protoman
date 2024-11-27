<!-- filepath: /Users/conversh/workspace/protoman/frontend/src/components/ChatComponent.vue -->
<template>
  <div>
    <h2>Chat</h2>
    <!-- Chat UI goes here -->
  </div>
</template>

<script>
export default {
  name: 'ChatComponent',
  props: {
    threadId: {
      type: String,
      required: true
    },
    messages: {
      type: Array,
      required: true
    }
  },
};
</script>

<style scoped>
/* Add styles for ChatComponent here */
</style>