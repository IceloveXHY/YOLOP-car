<template>
    <div class="container">
        <div class="login-container">
            <div class="login-header">
                <h2>用户登录</h2>
            </div>
            <form>
                <div class="form-group">
                    <label for="username">用户名</label>
                    <input type="text" v-model="account" id="username" placeholder="默认账户:admin" required>
                </div>
                <div class="form-group">
                    <label for="password">密码</label>
                    <input type="password" v-model="password" id="password" placeholder="默认密码:123456" required>
                </div>
                <div class="remember-forgot">
                    <div class="remember-me">
                        <input type="checkbox" id="remember">
                        <label for="remember">记住我</label>
                    </div>
                    <div class="forgot-password">
                        <a>忘记密码?</a>
                    </div>
                </div>
                <button type="button" class="login-button" @click="login">登录</button>
                <div class="register-link">
                    还没有账号? <a>立即注册</a>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup lang="ts" name="Login">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ElMessage } from 'element-plus'
const route = useRoute()
const router = useRouter()
// //挂载判断
// onMounted(() => {
//     console.log(route.meta.hidenMenu)
// })

let account = ref('')
let password = ref('')
//判断是否登录
const login = () => {
    // console.log(account, password)
    if (account.value == "admin" && password.value == "123456") {
        ElMessage({
            message: '登录成功',
            type: 'success',
        })
        //修改meta状态
        route.meta.hidenMenu = false;

        // console.log("meta状态",route.meta.hidenMenu);

        //浏览器中存储用户名
        localStorage.setItem("token", "admin")
        //跳转首页
        router.push('/home')

    } else {
        ElMessage({
            message: '用户名或密码错误',
            type: 'error',
        })
    }
}
</script>

<style scoped>
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: 'Arial', sans-serif;
}

.container {
    width: 100vw;
    height: 100vh;
}

.login-container {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    padding: 30px;
    width: 25rem;
    height: 26rem;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translateX(-50%) translateY(-50%);
}

.login-header {
    text-align: center;
    margin-bottom: 25px;
}

.login-header h2 {
    color: #333;
    font-size: 24px;
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    color: #555;
    font-size: 14px;
}

.form-group input {
    width: 100%;
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 14px;
    transition: border-color 0.3s;
}

.form-group input:focus {
    border-color: #4285f4;
    outline: none;
}

.remember-forgot {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    font-size: 13px;
}

.remember-me {
    display: flex;
    align-items: center;
}

.remember-me input {
    margin-right: 5px;
}

.forgot-password a {
    color: #4285f4;
    text-decoration: none;
}

.login-button {
    width: 100%;
    padding: 12px;
    background-color: #4285f4;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.login-button:hover {
    background-color: #3367d6;
}

.register-link {
    text-align: center;
    margin-top: 20px;
    font-size: 14px;
    color: #666;
}

.register-link a {
    color: #4285f4;
    text-decoration: none;
}
</style>