<template>
    <!-- 文件上传 -->
    <el-upload v-model:file-list="fileList" class="upload-demo"
        action="http://localhost:8000/process_video/"
        multiple 
        :on-preview="handlePreview"
        :on-remove="handleRemove" 
        :before-remove="beforeRemove" 
        :limit="1" 
        :on-exceed="handleExceed" 
        :on-success="handleSuccess"
        accept="image/*,video/*"
        >
        <el-button type="primary">上传检测样本</el-button>
        <template #tip>
            <div class="el-upload__tip">
                <!-- image/video files with a size less than 500KB. -->
                 限制 image/video 文件
            </div>
        </template>
    </el-upload>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { UploadProps, UploadUserFile } from 'element-plus'
import axios from 'axios';

// 上传文件列表
const fileList = ref<UploadUserFile[]>([]);

// 绑定移除文件时触发的事件处理函数
const handleRemove: UploadProps['onRemove'] = (file, uploadFiles) => {
    console.log(file, uploadFiles);
};

// 绑定预览文件时触发的事件处理函数
const handlePreview: UploadProps['onPreview'] = (uploadFile) => {
    console.log(uploadFile);
};

// 当选择的文件数量超过限制时，触发
const handleExceed: UploadProps['onExceed'] = (files, uploadFiles) => {
    ElMessage.warning(
        `The limit is 1, you selected ${files.length} files this time, add up to ${files.length + uploadFiles.length} totally`
    );
};

// 绑定在移除文件之前触发的事件处理函数 beforeRemove，可用于进行确认操作。
const beforeRemove: UploadProps['beforeRemove'] = (uploadFile, uploadFiles) => {
    return ElMessageBox.confirm(
        `Cancel the transfer of ${uploadFile.name} ?`
    ).then(
        () => true,
        () => false
    );
};

// 处理文件上传成功事件
const handleSuccess = (response: { message: string; processed_file_path: any; }, file: any, fileList: any) => {
    if (response && response.message === 'Video processed successfully') {
        // 这里可以根据后端返回的处理后文件路径，进行展示等操作
        console.log('处理后的文件路径:', response.processed_file_path);
    }
};
</script>

<style scoped>

</style>    