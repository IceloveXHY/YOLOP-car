<template>
    <div class="container">
        <el-card class="header">
            <el-row>
                <el-col :span="6">
                    <el-statistic title="共检测出抛洒物" :value="268500" />
                </el-col>
                <el-col :span="6">
                    <el-statistic title="检测种类" :value="138">
                        <!-- <template #title>
                            <div style="display: inline-flex; align-items: center">
                                Ratio of men to women
                                <el-icon style="margin-left: 4px" :size="12">
                                    <Male />
                                </el-icon>
                            </div>
                        </template>
<template #suffix>/100</template> -->
                    </el-statistic>
                </el-col>
                <el-col :span="6">
                    <el-statistic title="检测成功率" :value="outputValue" />
                </el-col>
                <el-col :span="6">
                    <el-statistic title="Feedback number" :value="562">
                        <template #suffix>
                            <el-icon style="vertical-align: -0.125em">
                                <ChatLineRound />
                            </el-icon>
                        </template>
                    </el-statistic>
                </el-col>
            </el-row>
        </el-card>
        <div class="charts">
            <el-card class="lineChartBox">
                <v-chart class="lineChart" :option="option_l" autoresize></v-chart>
            </el-card>
            <div class="right">
                <el-card class="pieChartBox">
                    <v-chart class="pieChart" :option="option_c" autoresize></v-chart>
                </el-card>
                <el-card class="raderChartBox">
                    <v-chart class="raderChart" :option="option_r" autoresize></v-chart>
                </el-card>
            </div>

        </div>
    </div>
</template>

<script setup>
import { ref } from "vue"
import { useTransition } from '@vueuse/core'
import { ChatLineRound } from '@element-plus/icons-vue'
const source = ref(0)
const outputValue = useTransition(source, {
    duration: 1500,
})
source.value = 90

const option_l = ref({
    tooltip: {
        trigger: "axis"
    },
    xAxis: {
        type: 'category',
        data: ['瓶子', '废纸', '石头', '钱', '鼠标', '电脑', '键盘']
    },
    yAxis: {
        type: 'value'
    },
    legend: {
        orient: 'plain',
        left: 'left'
    },
    series: [
        {
            data: [120, 200, 150, 80, 70, 110, 130],
            type: 'bar'
        }
    ]
})
const option_c = ref({
    title: {
        text: '道路抛洒物',
        left: 'left', // 调整图例，防止遮挡
    },
    tooltip: {
        trigger: 'item'
    },
    legend: {
        orient: 'vertical',
        left: 'right' // 调整图例位置，防止遮挡
    },
    series: [
        {
            name: '类别占比',
            type: 'pie',
            radius: ['40%', '70%'], // 改为环形图
            center: ['50%', '50%'], // 确保饼图居中
            data: [
                { value: 120, name: '瓶子' },
                { value: 200, name: '废纸' },
                { value: 150, name: '石头' },
                { value: 80, name: '钱' },
                { value: 70, name: '鼠标' },
                { value: 110, name: '电脑' },
                { value: 130, name: '键盘' },
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

const option_r = ref({
    title: {
        text: '雷达图分析'
    },
    legend: {
        left: 'right', // 调整图例，防止遮挡
        data: ['抛洒物'] // 必须和 series[].name 对应
    },
    radar: {
        indicator: [
            { name: '瓶子', max: 200 },
            { name: '废纸', max: 200 },
            { name: '石头', max: 200 },
            { name: '钱', max: 200 },
            { name: '鼠标', max: 200 },
            { name: '电脑', max: 200 },
            { name: '键盘', max: 200 },
        ]
    },
    series: [
        {
            name: '预算 vs 支出',
            type: 'radar',
            data: [
                {
                    value: [120, 200, 150, 80, 70, 110, 130],
                    name: '预算分配'
                },
            ]
        }
    ]
});
</script>

<style scoped>
.container {
    box-sizing: border-box;
    width: 100%;
    /* background-color: #e6e6e6; */
}

.header {
    width: 90%;
    margin: auto;
    height: 6rem;
    border-radius: 1rem;
    box-shadow: 1rem;
    /* background-color: #e6e6e6; */
    /* border: 1px solid rgba(0, 0, 0, .5); */
}

.charts {
    box-sizing: border-box;
    padding: 2rem 3rem;
    display: flex;
    justify-content: space-around;
}

.lineChartBox {
    width: 60%;
}

.right {
    display: flex;
    width: 35%;
    height: 30rem;
    flex-direction: column;
    justify-content: space-between;
}

.raderChartBox {
    width: 100%;
    height: 46%;
}

.pieChartBox {
    width: 100%;
    height: 46%;
}


.pieChart {
    width: 100%;
    height: 12.5rem;
}

.raderChart{
    width: 100%;
    height: 12.5rem;
}

.lineChart {
    width: 100%;
    height: 25rem;
}
</style>