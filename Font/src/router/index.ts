import { createRouter, createWebHashHistory, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    //重定向到指定页面,首页
    {
      path: "/",
      name: "RootRedirect",
      redirect:"/home"
    },
    //登录界面
    {
      path: "/login",
      name: "Login",
      component:()=>import('@/views/Login.vue'),
      meta: { hidenMenu: true }
    },
    //首页页面
    {
      path: "/home",
      name: "Home",
      component:()=>import('@/views/Home.vue'),
      meta: { requireAuth: true },
    },
    
    //疲劳驾驶
    {
      path: "/drowsyDriving",
      name: "DrowsyDriving",
      component:()=>import('@/views/InTesting/DrowsyDriving.vue'),
      meta: { requireAuth: true },
    },
    //抛洒物检测
    {
      path: "/throws",
      name: "Throws",
      component:()=>import('@/views/OutTesting/Throws.vue'),
      meta: { requireAuth: true },
    }, 
    //车辆违停
    {
      path: "/illegalParking",
      name: "IllegalParking",
      component:()=>import('@/views/OutTesting/IllegalParking.vue'),
      meta: { requireAuth: true },
    }, 
    //车道线生成
    {
      path: "/laneMarkings",
      name: "LaneMarkings",
      component:()=>import('@/views/OutTesting/LaneMarkings.vue'),
      meta: { requireAuth: true },
    },
    //数据界面
    {
      path: "/monitor",
      name: "Monitor",
      component:()=>import('@/views/Statistics.vue'),
      meta: { requireAuth: true },
    },
    //用户界面
    {
      path: "/user",
      name: "User",
      component:()=>import('@/views/User.vue'),
      meta: { requireAuth: true },
    },

  ],
});
//路由守卫前置检查
router.beforeEach((to, from, next) => {
  // 检查目标路由的 meta 信息中是否存在 requireAuth 字段，且值为 true
  if (to.meta.requireAuth) {
    // 从本地存储中获取 token，用于判断用户是否已登录
    const token = localStorage.getItem("token");
    // 如果 token 存在，说明用户已登录
    if (token) {
      // 允许路由跳转，继续访问目标页面
      next();
    } else {
      // 如果 token 不存在，说明用户未登录
      next({
        // 跳转到名为 "Login" 的路由，通常是登录页面
        name: "Login",
      });
    }
  } 
  else {
    // 如果目标路由不需要身份验证
    // 允许路由跳转，继续访问目标页面
    next();
  }
});
export default router
