<template>
    <div class="node">
      <template v-if="parent">
        <details :class="['details', currentClass]">
          <summary>{{ parent?.next[0] || "root" }}</summary>
          <div class="chat">
            <ChatItem v-for="chat in node.chat" :key="chat.id" :sender="chat.sender" :text="chat.text" />
          </div>
          <div class="rewind">
            <button @click="rewind">Rewind</button>
          </div>
        </details>
      </template>
      <template v-else>
        <div class="details root">root</div>
      </template>
      <div v-if="children.length" class="children-container">
        <TreeNode v-for="child in children" :key="child.id" :node="child" :nodes="nodes" />
      </div>
    </div>
</template>

<script>
import ChatItem from './ChatItem.vue';

  export default {
    name: 'TreeNode',
    components: {
      ChatItem
    },
    props: {
      node: {
        type: Object,
        required: true
      },
      nodes: {
        type: Array,
        required: true
      }
    },
    computed: {
      children() {
        const kids = this.nodes.filter(n => n.parent_checkpoint_id === this.node.checkpoint_id);
        return kids
      },
      parent() {
        return this.nodes.find(n => n.checkpoint_id === this.node.parent_checkpoint_id);
      },
      currentClass() {
        return this.node.current ? 'current' : '';
      }
    },
    methods: {
      async rewind() {
        try {
          const response = await fetch('http://127.0.0.1:5000/history/chat', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              threadId: this.node.thread_id,
              checkpointId: this.node.checkpoint_id
            })
          });
          if (!response.ok) {
            console.error('Failed to rewind');
          }
        } catch (error) {
          console.error('Error:', error);
        }
      }
    }
  }
</script>

<style scoped>

.node {
  margin: 20px;

}

.details {
  background-color: #f0f0f0;
  padding: 20px 10px;
  border: 1px solid #ccc;
  margin: 0 auto;
  text-align: center;
}

details, .root {
  width: 200px;
}

details[open] {
  width: 500px;
}

.rewind {
  text-align: center;
  margin-top: 10px;
}

.rewind button::before {
  content: '';
  position: absolute;
  top: 50%;
  left: -200px;
  height: 1px;
  width: 200px;
  background-color: #000;
}

.rewind button::after {
  content: '';
  position: absolute;
  top: 50%;
  right: -200px;
  height: 1px;
  width: 200px;
  background-color: #000;
}

.rewind button {
  position: relative;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  background-color: #007bff;
  color: #ecf0f1;
  cursor: pointer;
}

.chat {
  margin: 0 auto;
  width: 500px;
}

.children-container {
  display: flex;
  justify-content: center;
}

.chat-item-debug{
  display: none;
}

.current {
  background-color: #06ad0b;
}
</style>