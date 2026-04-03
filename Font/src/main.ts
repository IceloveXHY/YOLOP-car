import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Element from "element-plus"
import 'element-plus/dist/index.css'
import './assets/iconfont/iconfont.css'
import * as Icons from '@element-plus/icons-vue' // 引入所有图标
import * as echarts from 'echarts';
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import {  BarChart} from "echarts/charts"
// import { BarChart, Piechart, RaderChart } from "echarts/charts";
import { GridComponent, TooltipComponent } from "echarts/components";
import VChart from "vue-echarts";
import vue3videoPlay from 'vue3-video-play'; // 引入视频流

import 'vue3-video-play/dist/style.css'; // 引入样式

use([CanvasRenderer, BarChart, GridComponent, TooltipComponent]);

const app = createApp(App)
for (const [key, component] of Object.entries(Icons)) {
    app.component(key, component)
  }
  app.component("v-chart", VChart); // 全局注册 ECharts 组件
app.use(router)
app.use(Element)
app.use(vue3videoPlay)
app.mount('#app')
