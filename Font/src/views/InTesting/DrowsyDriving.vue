<template>
  <div>
    <!-- 标题 -->
    <div class="header">
      <h2>基于改进的MA—YOLOv8的疲劳驾驶检测系统</h2>
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
      <!-- 右侧展示区 -->
      <div class="result-section">
        <!-- 视频展示 -->
        <div class="video-container">
          <video controls class="preview-video">
            <source :src="videoSrc" type="video/mp4" v-if="videoSrc" />
            <source src="@/assets/video/video1.mp4" type="video/mp4" v-else />
            您的浏览器不支持视频播放
          </video>
        </div>
        <!-- 分析结果 -->
        <div class="analysis-results">
          <h3>安全分析报告</h3>
          <div class="stats-summary">
            <el-statistic title="总异常事件" :value="analysisSummary.total" />
            <el-statistic 
              title="危险动作" 
              :value="analysisSummary.dangerous" 
              class="danger-stat"
            />
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
import { ref, reactive, nextTick } from 'vue'
import axios from 'axios'
import { ElMessage, ElLoading } from 'element-plus'
import type { UploadUserFile } from 'element-plus'

// 类型定义
interface DetectionItem {
  time_sec: number;
  class: string;
  confidence: number;
  bbox: [number, number, number, number];
}

interface DetailItem {
  frame_number: number;
  detections: DetectionItem[];
}

interface ApiResponse {
  status: string;
  output_url: string;
  analysis: {
    total_events: number;
    dangerous_actions: number;
    details: DetailItem[];
  };
}

// 响应式数据
const fileList = ref<UploadUserFile[]>([])
const selectedFile = ref<File | null>(null)
const videoSrc = ref('')
const isLoading = ref(false)
const progress = ref(0)
const intervalId = ref<number>()
const analysisSummary = reactive({
  total: 0,
  dangerous: 0
})
interface AnalysisDetail {
  time: string;
  type: string;
  confidence: string;
  position: string;
}

const analysisDetails = ref<AnalysisDetail[]>([])

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

    const { data } = await axios.post('http://localhost:8000/drowsy_driving/', formData, {
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
    console.log('分析结果:', response.output_url)
    videoSrc.value = `http://localhost:8000${response.output_url}`
    console.log('视频地址:', videoSrc.value)
    nextTick(() => {
      const videoElement = document.querySelector('.preview-video') as HTMLVideoElement
      if (videoElement) {
        videoElement.load()
        videoElement.play().catch((error) => {
          console.log('自动播放被阻止:', error)
        })
      }
    })
    // 更新统计数据
    analysisSummary.total = response.analysis.total_events || 0;
    analysisSummary.dangerous = response.analysis.dangerous_actions || 0;

    // 处理详细数据
    analysisDetails.value = (response.analysis.details || []).flatMap(item => item.detections).map(detectionItem => ({
      time: `${(detectionItem.time_sec / 5).toFixed(1)}秒`,
      type: mapDetectionType(detectionItem.class.toLowerCase() || 'unknown'),
      confidence: `${(detectionItem.confidence * 100).toFixed(1)}%`,
      position: `X:${detectionItem.bbox[0]}, Y:${detectionItem.bbox[1]}`
    }));

    console.log('前端处理后的数据:', analysisDetails.value)
    // 强制表格刷新
    nextTick(() => {
      analysisDetails.value = [...analysisDetails.value];
    });

    ElMessage.success('分析完成');
  }
}

// 辅助方法
const mapDetectionType = (type: string) => {
  const typeMap: Record<string, string> = {
    'close_eyes': '闭眼',
    'open_mouth': '打哈欠',
    'looking_away': '视线偏离',
    'unknown': '未分类'
  };
  return typeMap[type] || '未知类型';
}

const getTagType = (type: string) => {
  return type === '闭眼' ? 'danger' : type === '打哈欠' ? 'warning' : 'info';
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