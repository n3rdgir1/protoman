<template>
    <h2>History</h2>
    <div>
      <TreeNode v-for="node in rootNodes" :key="node.id" :node="node" :nodes="nodes" />
      <div v-if="rootNodes.length === 0">No history available</div>
    </div>
</template>

<script>
  import TreeNode from './TreeNode.vue';

  export default {
    name: 'HistoryTree',
    components: {
      TreeNode
    },
    props: {
      threadId: {
        type: String,
        required: true
      }
    },
    data() {
      return {
        nodes: []
      };
    },
    computed: {
      rootNodes() {
        return this.nodes.filter(node => node.parent_checkpoint_id === null);
      }
    },
    created() {
      fetch(`http://127.0.0.1:5000/history/${this.threadId}`)//, { mode: 'no-cors' })
        .then(response => response.json())
        .then(data => {
          this.nodes = data;
        })
        .catch(error => {
          console.error('Error fetching nodes:', error);
        });
    }
  }
</script>

<style scoped>
</style>