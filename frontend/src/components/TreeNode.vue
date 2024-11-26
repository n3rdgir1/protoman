<template>
    <div class="node">
      <div class="details">Node: {{ parent?.next }}</div>
      <div class="chat">
        <ChatItem v-for="chat in node.chat" :key="chat.id" :sender="chat.sender" :text="chat.text" />
      </div>
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
  width: 500px;
  margin: 0 auto;
  text-align: center;
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
</style>