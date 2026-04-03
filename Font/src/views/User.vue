<template>
    <div class="user-profile-container">
        <!-- 用户信息卡片 -->
        <el-card class="user-card">
            <div class="user-header">
                <!--用户头像框-->
                <div class="avatar-container">
                    <el-avatar :size="60" :icon="UserFilled"/>
                </div>
                <div class="user-info">
                    <h2 class="user-name">{{ userInfo.name }}</h2>
                    <p class="user-meta">
                        <!-- <el-tag type="info" size="small">{{ userInfo.level }}</el-tag> -->
                        <span class="join-date">加入于 {{ userInfo.joinDate }}</span>
                    </p>
                </div>
                <div class="action-buttons">
                    <el-button type="danger" @click="handleLogout" plain>
                        <el-icon>
                            <SwitchButton />
                        </el-icon>
                        退出登录
                    </el-button>
                </div>
            </div>
        </el-card>

        <!-- 用户记录卡片 -->
        <el-card class="records-card">
            <template #header>
                <div class="card-header">
                    <el-icon>
                        <Clock />
                    </el-icon>
                    <span>最近记录</span>
                </div>
            </template>

            <el-empty v-if="records.length === 0" description="暂无记录" />

            <div v-else class="record-list">
                <div v-for="(record, index) in records" :key="index" class="record-item">
                    <div class="record-content">
                        <h4>{{ record.title }}</h4>
                        <p class="record-desc">{{ record.description }}</p>
                    </div>
                    <div class="record-time">
                        <el-icon>
                            <Timer />
                        </el-icon>
                        <span>{{ record.time }}</span>
                    </div>
                </div>
            </div>
        </el-card>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessageBox, ElMessage } from 'element-plus'
import { SwitchButton, Clock, Timer } from '@element-plus/icons-vue'
import { UserFilled } from '@element-plus/icons-vue'
import { useRoute, useRouter } from 'vue-router';
import {useRecords} from '@/hooks/userRecord';
import { use } from 'echarts/types/src/extension.js';
const route = useRoute()
// 用户信息数据
const userInfo = ref({
    name: '.s',
    avatar: "",
    // level: '黄金会员',
    joinDate: '2024年5月20日'
})

// // 用户记录数据
const {records}=useRecords()


// 退出登录处理
const handleLogout = () => {
    //清空本地缓存
    localStorage.setItem("token", '')
    //修改meta状态
    route.meta.hidenMenu = true;
    //重新加载页面
    location.reload()
}
</script>

<style scoped>
.user-profile-container {
    width: 100%;
    padding: 2rem;
   
}

.user-card {
    margin-bottom: 20px;
}

.user-header {
    display: flex;
    align-items: center;
    padding: 10px 0;
}

.avatar-container {
    margin-right: 20px;
}

.user-info h2 {
    margin: 0 0 8px 0;
    font-size: 20px;
    color: #333;
}

.user-meta {
    display: flex;
    align-items: center;
    margin: 0;
    color: #666;
}

.join-date {
    margin-left: 10px;
    font-size: 13px;
}

.action-buttons {
    margin-left: auto;
}

.records-card {
    margin-top: 20px;
}

.card-header {
    display: flex;
    align-items: center;
}

.card-header .el-icon {
    margin-right: 8px;
    color: var(--el-color-primary);
}

.record-list {
    padding: 0;
}

.record-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid var(--el-border-color-light);
}

.record-item:last-child {
    border-bottom: none;
}

.record-content h4 {
    text-align: left;
    margin: 0 0 6px 0;
    font-size: 15px;
    color: #333;
}

.record-desc {
    margin: 0;
    font-size: 13px;
    color: #888;
}

.record-time {
    display: flex;
    align-items: center;
    color: #666;
    font-size: 13px;
}

.record-time .el-icon {
    margin-right: 5px;
}

.user-name{
    margin-left: 0;
    box-sizing: border-box;
    padding: 0 .5rem;
    text-align: left;
}

@media (max-width: 600px) {
    .user-header {
        flex-direction: column;
        text-align: center;
    }

    .avatar-container {
        margin-right: 0;
        margin-bottom: 15px;
    }

    .action-buttons {
        margin: 15px 0 0 0;
        width: 100%;
    }

    .record-item {
        flex-direction: column;
        align-items: flex-start;
    }

    .record-time {
        margin-top: 8px;
    }
}
</style>