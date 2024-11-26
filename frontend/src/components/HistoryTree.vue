<template>
    <div>
      <TreeNode v-for="node in rootNodes" :key="node.id" :node="node" :nodes="nodes" />
    </div>
</template>

<script>
  import TreeNode from './TreeNode.vue';

  export default {
    name: 'HistoryTree',
    components: {
      TreeNode
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
      fetch('http://127.0.0.1:5000/history/11')
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