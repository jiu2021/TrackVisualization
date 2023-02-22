<template>
  <div class="login-wrapper">
    <el-card class="login-form">
      <h2>TrackVisualization系统</h2>
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
import { ref } from "vue";
import { loginM } from "@/model";
import { reqLogin } from "@/api";
import { ElMessage } from "element-plus";
import router from "@/router";
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
          message: '登陆成功',
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
  height: 320px;
  margin-top: 200px;
  padding: 0 20px;
}

.account-input {
  margin-bottom: 20px;
}

.btn {
  margin-top: 30px;
}
</style>