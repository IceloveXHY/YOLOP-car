<template>
  <div>
      <!--标题-->
      <div>
        <h2 style="margin-left: 500px;">车道线生成</h2>
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
          <!--右侧展示-->
          <div class="result-section">
              <!--视频展示-->
              <div class="video-container">
                <video controls class="preview-video">
                  <source :src="videoSrc" type="video/mp4" v-if="videoSrc" />
                  <source src="@/assets/video/video4.mp4" type="video/mp4" v-else />
                  您的浏览器不支持视频播放
                </video>
              </div>
              
          </div>
      </div>
      <!-- 加载遮罩 -->
    <el-dialog v-model="isLoading" :show-close="false" width="30%">
      <div class="progress-container">
        <el-progress 
          type="dashboard" 
          :percentage="progress"
          :color="progressColors"
        />
        <p class="progress-text">视频分析中，请稍候...</p>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import type { UploadUserFile } from 'element-plus';
import { nextTick } from 'vue';
import { useRecords } from '@/hooks/userRecord';
import { onBeforeUnmount } from 'vue';
// 调用自定义 hook
const { records } = useRecords();
// 上传文件列表
const fileList = ref<UploadUserFile[]>([]);
// 选中的文件
const selectedFile = ref<File | null>(null);
// 视频源路径
const videoSrc = ref<string>('');
const isLoading = ref(false);
// 进度条百分比
const progress = ref(0);
 // 用于存储定时器ID
let intervalId: number | null = null; 
// 进度条颜色配置
const progressColors = [
  { color: '#f56c6c', percentage: 20 },
  { color: '#e6a23c', percentage: 40 },
  { color: '#5cb87a', percentage: 60 },
  { color: '#1989fa', percentage: 80 },
  { color: '#6f7ad3', percentage: 100 }
]
// 处理文件选择变化
const handleFileChange = (file: UploadUserFile) => {
    selectedFile.value = file.raw!;
};

// 当选择的文件数量超过限制时触发
const handleExceed = (files: UploadUserFile[], uploadFiles: UploadUserFile[]) => {
  ElMessage.warning(
      `The limit is 1, you selected ${files.length} files this time, add up to ${files.length + uploadFiles.length} totally`
  );
};

// 上传文件函数
const uploadFile = async () => {
  if (!selectedFile.value) {
      ElMessage.warning('请选择要上传的文件');
      return;
  }
  isLoading.value = true;
  // 模拟进度：5秒内加载到99%
  const duration = 10000; // 5秒
  const intervalTime = 50; // 更新间隔(毫秒)
  const steps = duration / intervalTime; // 总步数
  let currentStep = 0;
  //定时器
  intervalId = setInterval(() => {
    currentStep++;
    const newProgress = (Math.min(99, (currentStep / steps) * 100)) | 0; // 限制最大99%
    progress.value = newProgress;
    if (currentStep >= steps) clearInterval(intervalId!); // 到达5秒后停止
  }, intervalTime);
  const formData = new FormData();
  formData.append('video', selectedFile.value);
  try {
      const response = await axios.post('http://localhost:8000/lane_markings/', formData, {
          headers: {
              'Content-Type': 'multipart/form-data'
          }
      });
        // 清除定时器并直接跳转到100%
      if (intervalId) clearInterval(intervalId);
      progress.value = 100;
      
      // 1秒后关闭弹窗让用户看到完成状态
      setTimeout(() => {
        isLoading.value = false;
      }, 1000);
      handleSuccess(response.data);
      fileList.value = [];
      selectedFile.value = null;
  } catch (error) {
      ElMessage.error('文件上传失败，请稍后重试');
      console.error('文件上传错误:', error);
  }
};

// 处理文件上传成功事件
const handleSuccess = (response: { message: string; output_video_path: any; }) => {
    if (response && response.message === 'Video saved successfully') {
        // 基础路径为 http://localhost:8000/ ，手动拼接完整路径
        const baseUrl = 'http://localhost:8000';
        videoSrc.value = baseUrl + response.output_video_path; 
        console.log('处理后的文件路径:', videoSrc.value);
        nextTick(() => {
            // 比如重新加载视频
            const videoElement = document.querySelector('video') as HTMLVideoElement;
            if (videoElement) {
                videoElement.load();
            }
        });
    }
};
// 组件卸载时清理定时器
onBeforeUnmount(() => {
  if (intervalId) clearInterval(intervalId);
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

.stats-summary {
  display: flex;
  gap: 30px;
  margin: 20px 0;
}

.danger-stat {
  color: #f56c6c;
}

.progress-container {
  text-align: center;
  padding: 20px;
}

.progress-text {
  margin-top: 15px;
  color: #606266;
}
</style>    