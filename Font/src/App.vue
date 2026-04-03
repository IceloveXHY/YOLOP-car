<template>
 
    <div style="display: flex;">
        <!-- 菜单组件 -->
      <nav>
          <Menu></Menu>
      </nav>
      <RouterView></RouterView>
    </div>
</template>
<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import Menu from './components/Menu.vue'
</script>

<style scoped>
/* #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
}
nav {
    padding: 0;
    margin: 0;
} */
</style>
