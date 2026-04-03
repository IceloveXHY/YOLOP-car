<template>
    <div>
        <!--标题-->
        <div>
          <h2 style="margin-left: 500px;">抛洒物检测</h2>
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
                 <!-- 视频展示 -->
                <div class="video-container">
                  <video controls class="preview-video">
                    <source :src="videoSrc" type="video/mp4" v-if="videoSrc" />
                    <source src="@/assets/video/video2.mp4" type="video/mp4" v-else />
                    您的浏览器不支持视频播放
                  </video>
                </div>
                  <el-table :data="analysisDetails" height="200" style="width: 100%">
                    <el-table-column prop="time" label="时间" width="120" />
                    <el-table-column prop="type" label="类型" width="120">
                      <template #default="{ row }">
                        <el-tag :type="getTagType(row.type)">
                          {{ row.type }}
                        </el-tag>
                      </template>
                    </el-table-column>
                    <el-table-column prop="confidence" label="置信度" width="100" />
                    <el-table-column prop="position" label="位置" />
                  </el-table>
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
   const intervalId = ref<number>()
  // 类型定义
  interface DetectionItem {
  time_sec: number;
  class: string;
  confidence: number;
  bbox: [number, number, number, number];
}

// interface DetailItem {
//   detections: detectionItem[];
// }

interface ApiResponse {
  status: string;
  output_url: string;
  analysis: {
    total_events: number;
    dangerous_actions: number;
    details: DetectionItem[];  // 修改数据结构定义
  };
}
interface AnalysisDetail {
  time: string;
  type: string;
  confidence: string;
  position: string;
}
const analysisDetails = ref<AnalysisDetail[]>([]);  // 表格数据

// 类型标签样式映射
const getTagType = (type: string) => {
  const typeMap: { [key: string]: string } = {
    'Bottle': 'primary',
    'Scattered debris': 'danger',
    'Soft_plastics': 'warning',
    'cardboard_boxes': 'success',
    'rock': 'info',
    'small items': ''
  };
  return typeMap[type] || 'info';
};
// 辅助方法
const mapDetectionType = (type: string) => {
  const typeMap: Record<string, string> = {
    'Bottle': '瓶子',
    'Scattered debris': '碎片',
    'Soft_plastics': '塑料袋',
    'cardboard_boxes': '纸箱',
    'rock': '石头',
    'small items': '小物品'
  };
  return typeMap[type] || '未知类型'; // 保持原始大小写匹配
}
  // 进度条颜色配置
const progressColors = [
  { color: '#f56c6c', percentage: 20 },
  { color: '#e6a23c', percentage: 40 },
  { color: '#5cb87a', percentage: 60 },
  { color: '#1989fa', percentage: 80 },
  { color: '#6f7ad3', percentage: 100 }
]

  // 文件处理
const handleFileChange = (file: UploadUserFile) => {
  if (file.raw?.type.startsWith('video/')) {
    selectedFile.value = file.raw
  } else {
    ElMessage.error('请选择有效的视频文件')
    fileList.value = []
  }
}

const handleExceed = () => {
  ElMessage.warning('每次只能上传一个视频文件')
}
  
  // 上传处理
const uploadFile = async () => {
  if (!selectedFile.value) return

  isLoading.value = true
  progress.value = 0

  // 模拟进度
  intervalId.value = window.setInterval(() => {
    if (progress.value < 90) {
      progress.value += Math.floor(Math.random() * 5) + 1
    }
  }, 500)

  try {
    const formData = new FormData()
    formData.append('video', selectedFile.value)

    const { data } = await axios.post('http://localhost:8000/throws/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    handleSuccess(data)
  } catch (error) {
    ElMessage.error('分析失败：' + (error as Error).message)
  } finally {
    clearInterval(intervalId.value)
    progress.value = 100
    setTimeout(() => {
      isLoading.value = false
      progress.value = 0
    }, 500)
  }
}

  // 处理成功响应
  const handleSuccess = (response: ApiResponse) => {
  if (response.status === 'success') {
    console.log('原始响应数据:', response)  // 调试输出完整数据

    // 处理视频地址
    videoSrc.value = `http://localhost:8000${response.output_url}`

    // 处理分析数据（关键修改）
    analysisDetails.value = (response.analysis?.details || [])
      .filter(item => item && item.class)  // 过滤无效数据
      .map(detectionItem => ({
        time: `${detectionItem.time_sec.toFixed(1)}秒`,  // 直接使用秒数
        type: mapDetectionType(detectionItem.class), 
        confidence: `${(detectionItem.confidence * 100).toFixed(1)}%`,
        position: `(${detectionItem.bbox[0]},${detectionItem.bbox[1]}) - (${detectionItem.bbox[2]},${detectionItem.bbox[3]})`
      }));

    console.log('处理后的表格数据:', analysisDetails.value)
    
    // 强制刷新视频组件
    nextTick(() => {
      const videoElement = document.querySelector('.preview-video')
      if (videoElement) {
        (videoElement as HTMLVideoElement).load()
      }
      analysisDetails.value = [...analysisDetails.value]  // 触发响应式更新
    })

    ElMessage.success('分析完成')
  }
}
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