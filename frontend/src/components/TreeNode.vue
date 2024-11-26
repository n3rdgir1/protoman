<template>
    <div class="node">
      <div class="details">Next: {{ node.next }}</div>
      <div v-if="children.length" class="children-container">
        <TreeNode v-for="child in children" :key="child.id" :node="child" :nodes="nodes" />
      </div>
    </div>
</template>

<script>
  export default {
    name: 'TreeNode',
    props: {
      node: Object,
      nodes: Array
    },
    computed: {
      children() {
        const kids = this.nodes.filter(n => n.parent_checkpoint_id === this.node.checkpoint_id);
        return kids
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

.children-container {
  display: flex;
  justify-content: center;
}
</style>