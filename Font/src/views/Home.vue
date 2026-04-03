<template>
  <div class="home">
    <div class="content">
      <h1>欢迎来到智能驾驶实时安全监管系统</h1>
      <p>我们致力于提供最先进的交通解决方案</p>
    </div>
    <div class="container">
        <div
            v-for="(item, index) in imageList"
            :key="index"
            class="card"
            @mouseenter="handleMouseEnter(index)"
            @mouseleave="handleMouseLeave(index)"
        >
            <img :src="item.src" :class="{ 'transparent': isExpanded[index] }" :alt="item.alt">
            <div class="card-content">
                <p class="card-title">{{ item.title }}</p>
                <!-- <p class="card-desc">{{ item.desc }}</p> -->
                <!-- <button class="card-btn">{{ item.btnText }}</button> -->
            </div>
        </div>
    </div>
    <div styple="margin-top: 20px; text-align: center; width: 100%;">
      <h2>关于我们</h2>
      <p>
        本系统聚焦交通安全与管理领域，依托前沿技术构建核心能力，打造多维度智能解决方案：
        车辆违停检测功能通过实时视频分析技术精准捕捉违规停车行为并生成证据链，有效保障道路畅通；
        抛洒物检测利用多光谱传感器融合算法实时识别路面异物并触发分级预警，显著降低安全隐患；
        疲劳驾驶检测借助驾驶员面部姿态识别技术实时监测疲劳、分神等危险状态，通过声光预警与数据同步干预预防事故发生；
        车道线生成功能结合机器视觉与语义分割算法动态生成高精度车道线标识，为规范行车轨迹及智能驾驶系统提供精准路况信息。
        团队始终秉持创新理念，持续优化算法与技术，针对城市交通治理、高速公路监测等多元场景提供“检测-预警-处置”全链路智能解决方案，致力于以技术驱动交通管理数字化转型，守护每一段安全出行，助力构建高效有序的现代交通生态。 </p>
      <p>我们提供多种智能交通解决方案，欢迎咨询！</p>
    </div>
      
  </div>
 
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

// 定义图片列表数据，保持本地路径
const imageList = [
  {
      src: 'src/assets/img/car.png',
      alt: 'car',
      title: '车辆违停检测',
      desc: '提供坚实的交通安全检测能力',
      btnText: '立即咨询'
  },
  {
      src: 'src/assets/img/garbage.jpg',
      alt: 'garbage',
      title: '抛洒物检测',
      desc: '相关功能描述',
      btnText: '查看更多'
  },
  {
      src: 'src/assets/img/sleepy.jpg',
      alt:'sleepy',
      title: '疲劳驾驶检测',
      desc: '功能三的描述',
      btnText: '了解详情'
  },
  {
      src: 'src/assets/img/virtualroad.png',
      alt: 'virtualroad',
      title: '车道线生成',
      desc: '功能四的描述',
      btnText: '立即体验'
  }
];

const isExpanded = ref<boolean[]>(new Array(imageList.length).fill(false));
const handleMouseEnter = (index: number) => {
  isExpanded.value[index] = true;
};
const handleMouseLeave = (index: number) => {
  isExpanded.value[index] = false;
};

</script>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  align-items: center; /* 水平居中 */
  justify-content: center; /* 垂直居中 */
  margin-top: 50px;
  margin-left: 100px;
  /* 背景颜色 */
  /* background-color: #f0f0f0;  */
}
.content {
  text-align: center;
  /* margin-bottom: 20px; */
}
.container {
  display: flex;
  justify-content: center; /* 水平方向将子元素居中 */
  align-items: center; /* 垂直方向将子元素居中 */
  margin-top: 50px;
}

.card {
  width: 250px;
  height: 300px;
  border: 1px solid #ccc;
  border-radius: 5px;
  overflow: hidden;
  position: relative;
  transition: all 0.3s ease;
}

/* 新增包裹元素样式 */
.image-text-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
}

.card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: opacity 0.3s ease;
}

/* 鼠标悬停时图片变透明的样式 */
.transparent {
  opacity: 0.3;
}

.card-content {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: rgba(255, 255, 255, 0.8);
  padding: 10px;
  transition: all 0.3s ease;
}

.card-title {
  margin: 0;
  font-size: 16px;
}

.card-desc {
  margin: 10px 0;
  font-size: 14px;
}

.card-btn {
  width: 100%;
  padding: 5px;
  background-color: #007BFF;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

/* 新增鼠标悬停时卡片向右伸长的样式 */
.card:hover {
  width: 300px; /* 鼠标放上去后宽度变为300px，可根据需求调整 */
  transform: translateX(0); /* 初始位置不变 */
  transition: width 0.3s ease, transform 0.3s ease; /* 过渡效果 */
}
</style>