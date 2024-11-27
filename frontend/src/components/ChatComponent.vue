<template>
  <div>
    <h2>Chat</h2>
    <label>
      <input type="checkbox" v-model="showDebug"> Show Debug Messages
    </label>
    <div class="message-box">
      <ChatItem
        v-for="message in messages"
        :key="message.id"
        :sender="message.sender"
        :text="message.text"
      />
    </div>
    <form @submit.prevent="sendMessage" class="message-form">
      <button @click="newConvo" class="new-thread-button">+</button>
      <textarea v-model="newMessage" placeholder="Type a message..." class="message-input form-control" rows="3"></textarea>
      <button type="submit" class="send-button btn btn-primary">Send</button>
    </form>
  </div>
</template>

<script>
import ChatItem from './ChatItem.vue';

export default {
  name: 'ChatComponent',
  components: {
    ChatItem
  },
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
  data() {
    return {
      newMessage: '',
      showDebug: false
    }
  },
  methods: {
    async sendMessage() {
      this.$nextTick(() => {
        this.scrollToBottom();
      });
      if (this.newMessage.trim() === '') return

      const userMessage = {
        text: this.newMessage,
        sender: 'user',
      }
      this.$emit('add-message', userMessage.text, userMessage.sender)

      try {
        await fetch('http://127.0.0.1:5000/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ message: userMessage.text, thread_id: this.threadId })
        });
      } catch (error) {
        console.error('Error sending message:', error)
      }
    },
    scrollToBottom() {
      const chatHistory = this.$el.querySelector('.message-box');
      chatHistory.scrollTop = chatHistory.scrollHeight;
    },
    newConvo() {
      this.$emit('new-thread')
    }
  }

};
</script>

<style scoped>
.message-box {
  height: 400px;
  overflow-y: scroll;
  background-color: darkgray;
  scrollbar-width: none; /* For Firefox */
  -ms-overflow-style: none;  /* For Internet Explorer and Edge */
}
.message-form {
  display: flex;
  align-items: center;
}

.message-input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin: 0 10px;
}

.send-button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  background-color: #007bff;
  color: #ecf0f1;
  cursor: pointer;
}

.send-button:hover {
  background-color: #0056b3;
}

.new-thread-button {
  background-color:  #007bff;
  color: #ecf0f1;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  font-size: 24px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.new-thread-button:hover {
  background-color: #0056b3;
}

form {
  margin-top: 20px;
}
</style>