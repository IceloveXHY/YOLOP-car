<template>
  <div>
    <!-- 标题 -->
    <div>
      <h2 style="margin-left: 500px;">车辆违停检测</h2>
    </div>
    <!-- 内容展示区 -->
    <div class="content-container">
      <!-- 左侧上传区 -->
      <div class="upload-section">
        <el-upload
          v-model:file-list="fileList"
          class="upload-demo"
          :auto-upload="false"
          :limit="1"
          :on-change="handleFileChange"
          :on-exceed="handleExceed"
          accept="video/*"
        >
          <template #trigger>
            <el-button type="primary">选择检测视频</el-button>
          </template>
          <el-button class="ml-3" type="success" @click="uploadFile" :disabled="!selectedFile" style="margin-left: 10px;">
            开始分析
          </el-button>
          <template #tip>
            <div class="el-upload__tip">支持格式：MP4</div>
          </template>
        </el-upload>
      </div>
      <!-- 右侧展示（视频渲染） -->
      <div class="result-section">
        <div class="video-container">
          <canvas id="videoCanvas" class="preview-video"></canvas>
        </div>
        <div class="analysis-results">
          <h3>分析报告</h3>
          <div class="stats-summary">
            <el-statistic title="违停车辆" :value="analysisSummary" />
          </div>
        </div> <!-- 补全analysis-results的闭合标签 -->
      </div> <!-- 补全result-section的闭合标签 -->
    </div> <!-- 补全content-container的闭合标签 -->
  </div>
</template>

<script setup lang="ts">
import { ref, onUnmounted } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import type { UploadUserFile } from 'element-plus';

// 上传相关
const fileList = ref<UploadUserFile[]>([]);
const selectedFile = ref<File | null>(null);
let taskId = ''; // 存储任务 ID
let ws: WebSocket | null = null; // WebSocket 连接
const analysisSummary = ref(0);
// 文件选择处理
const handleFileChange = (file: UploadUserFile) => {
  selectedFile.value = file.raw as File;
  fileList.value = [file];
};

// 超出文件限制处理
const handleExceed = () => {
  ElMessage.warning('最多上传 1 个视频文件');
};

// 上传视频
const uploadFile = async () => {
  if (!selectedFile.value) {
    ElMessage.warning('请选择要上传的视频文件');
    return;
  }

  const formData = new FormData();
  formData.append('video', selectedFile.value);

  try {
    // 上传文件获取任务 ID
    const response = await axios.post('http://localhost:8000/api/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    taskId = response.data.task_id;

    // 建立 WebSocket 连接
    ws = new WebSocket(`ws://localhost:8000/ws/process/${taskId}/`);
    ws.onmessage = (event) => {
      console.log('收到后端数据', event.data); // 确认是否收到数据
      const base64Frame = event.data;
      renderFrame(base64Frame); // 渲染视频帧
    };

    ws.onerror = () => {
      ElMessage.error('实时通信失败，请重试');
      ws?.close();
    };

  } catch (error) {
    ElMessage.error('文件上传失败，请稍后重试');
    console.error('文件上传错误:', error);
  }
};

// 渲染视频帧到 Canvas
const renderFrame = (base64Frame: string) => {
  const canvas = document.getElementById('videoCanvas') as HTMLCanvasElement;
  console.log('检查 canvas 元素', canvas); // 检查 canvas 是否存在
  if (!canvas) {
    console.error('未获取到 canvas 元素');
    return;
  }
  const ctx = canvas.getContext('2d');
  console.log('检查 ctx', ctx); // 检查 ctx 是否获取成功
  if (!ctx) {
    console.error('未获取到 canvas 的 2D 上下文');
    return;
  }

  const img = new Image();
  img.src = base64Frame;
  img.onerror = () => {
    console.error('图片加载错误，base64 数据可能无效', base64Frame); // 检查图片加载错误
  };
  img.onload = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
  };
};

// 组件卸载时关闭 WebSocket
onUnmounted(() => {
  ws?.close();
});
</script>

<style scoped>
.header {
  text-align: center;
  margin: 20px 0;
}

.content-container {
  display: flex;
  gap: 40px;
  padding: 0 40px;
}

.upload-section {
  width: 300px;
  
}

.result-section {
  flex: 1;
}

.video-container {
  margin-bottom: 20px;
}

.preview-video {
  width: 400px;
  max-height: 400px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}

</style>