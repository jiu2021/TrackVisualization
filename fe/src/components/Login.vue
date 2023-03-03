<template>
  <div class="login-wrapper" v-title="name">
    <el-card class="login-form">
      <img class="logo" src="@/assets/logo-m.png" alt="">
      <el-input v-model.trim="account" placeholder="请输入管理员账号" size="large" clearable class="account-input">
        <template #prepend>
          <span>账号</span>
        </template>
      </el-input>
      <el-input v-model.trim="pwd" type="password" placeholder="请输入管理员密码" size="large" clearable>
        <template #prepend>
          <span>密码</span>
        </template>
      </el-input>
      <el-button type="primary" bg size="large" class="btn" @click="goLogin(account, pwd)">登录</el-button>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue";
import { loginM } from "@/model";
import { reqLogin, reqUserData } from "@/api";
import { ElMessage } from "element-plus";
import router from "@/router";
const name = "登录";
const account = ref('');
const pwd = ref('');
const goLogin = (account: string, pwd: string) => {
  if (account && pwd) {
    const data: loginM = { account, pwd };
    reqLogin(data).then(function (response) {
      if (response.data.code == 200) {
        localStorage.setItem('token', response.data.data.token);
        localStorage.setItem('username', response.data.data.username)
        ElMessage({
          showClose: true,
          message: '登录成功',
          type: 'success',
        });
        router.push({ name: 'home' });
      } else {
        ElMessage({
          showClose: true,
          message: '帐号或密码错误',
          type: 'error',
        });
      }
    })
  }
}

onMounted(() => {
  reqUserData().then(function (res) {
    if (res.data.code == 200) {
      router.push({ name: 'home' });
      ElMessage({
        showClose: true,
        message: '自动登录成功',
        type: 'success',
      });
    }
  })
})
</script>

<style scoped>
.login-wrapper {
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
}

.login-form {
  width: 450px;
  height: 380px;
  margin-top: 200px;
  padding: 0 20px;
}

.account-input {
  margin-bottom: 20px;
}

.btn {
  margin-top: 30px;
}

.logo {
  height: 120px;
  margin-bottom: 20px;
}
</style>