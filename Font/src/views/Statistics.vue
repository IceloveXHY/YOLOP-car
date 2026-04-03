<template>
    <div class="container">
        <div class="header">
            <div class="custom-style">
                <el-segmented v-model="value" :options="options" />
            </div>
            <!-- <div class="titile">
                数据统计
            </div> -->
        </div>
        <!-- <Tired></Tired> -->
        <Throw></Throw>
    </div>

</template>

<script setup lang="ts">
import { ref } from 'vue';
// import Tired from "@/components/Tired.vue"
import Throw from "@/components/Throw.vue"
const options = ['疲劳驾驶', '抛洒物检测', '道路识别', '违停检测']
const value = ref('抛洒物检测')
const option = ref({
    title: {
        text: 'Referer of a Website',
        subtext: 'Fake Data',
        left: 'center'
    },
    tooltip: {
        show: false,
        trigger: 'item'
    },
    legend: {
        show: false,
        orient: 'plain',
        left: 'left'
    },
    series: [
        {
            name: 'Access From',
            type: 'pie',
            radius: '50%',
            data: [
                { value: 1048, name: 'Search Engine' },
                { value: 735, name: 'Direct' },
                { value: 580, name: 'Email' },
                { value: 484, name: 'Union Ads' },
                { value: 300, name: 'Video Ads' }
            ],
            emphasis: {
                itemStyle: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }
    ]
});
</script>


<style scoped>

.el-col {
  text-align: center;
}
.chart {
    width: 600px;
    height: 400px;
}

.container {
    width: 100%;
    height: 100%;
    box-sizing: border-box;
    padding-top: 1rem;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
}

.header {
    display: flex;
    text-align: center;
    /* justify-content: space-around; */
    width: 100%;
    height: 4rem;
    line-height: 4rem;
    /* border: 1px solid black; */

}

.titile {
    font-size: 2rem;
    width: 100%;
    text-align: center;
}

.custom-style .el-segmented {
    --el-segmented-item-selected-color: var(--el-text-color-primary);
    --el-segmented-item-selected-bg-color: #ffd100;
    --el-border-radius-base: 16px;
    position: absolute;
    transform: translateX(4rem) translateY(1rem);
}
</style>