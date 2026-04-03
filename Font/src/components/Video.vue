<template>
  <video controls width="150">
    <source src="@/assets/video/video1.mp4" type="video/mp4" />
  </video>
</template>

<script setup lang="ts">
import { reactive } from 'vue';
const options =reactive ({
  // src: "D:/Project/Vue/road_detection(ts)/src/assets/video/video1.mp4", // 本地视频文件路径
  // src: "@/assets/video/video1.mp4", // 本地视频文件路径
  // type: 'mp4', // 视频类型
});
</script>

<style scoped>
</style>    