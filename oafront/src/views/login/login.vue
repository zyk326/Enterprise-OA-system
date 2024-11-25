<script setup name="login">
import login_image from "@/assets/image/login.png";
import { reactive } from "vue";
import axios from "axios";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";
import authHttp from "@/api/authHttp";
import {ElMessage} from "element-plus"

const authStore = useAuthStore();
const router = useRouter();

let form = reactive({
  email: "",
  password: "",
});

const onSubmit = async () => {
  let pwdRgx = /^[0-9a-zA-Z_-]{6,20}/;
  let emailRgx = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9])+/;
  if (!emailRgx.test(form.email)) {
    // alert("邮箱格式不满足！");
    ElMessage.info("邮箱格式不满足！")
    return;
  }
  if (!pwdRgx.test(form.password)) {
    // alert("密码格式不满足！");
    ElMessage.info("密码格式不满足！")
    return;
  }

  // 封装axios
  //   authHttp
  //     .login(form.email, form.password)
  //     .then((res) => {
  //       let data = res.data;
  //       let token = data.token;
  //       let user = data.user;
  //       authStore.setUserToken(user, token);
  //       // 跳转到oa系统的首页
  //       router.push({ name: "frame" });
  //     })
  //     .catch((err) => {
  //       let detail = err.response.data.detail;
  //       alert(detail);
  //     });

  // 异步调用
  try {
    let data = await authHttp.login(form.email, form.password);
    // console.log(data)
    let token = data.token;
    let user = data.user;
    authStore.setUserToken(user, token);
    router.push({ name: 'frame' });
  } catch (detail) {
    // alert(detail);
    ElMessage.info(detail)
  }
};
</script>

<template>
  <div class="dowebok">
    <div class="container-login100">
      <div class="wrap-login100">
        <div class="login100-pic js-tilt" data-tilt>
          <img :src="login_image" alt="IMG" />
        </div>

        <div class="login100-form validate-form">
          <span class="login100-form-title"> 员工登陆 </span>

          <div class="wrap-input100 validate-input">
            <input
              class="input100"
              type="text"
              name="email"
              placeholder="邮箱"
              v-model="form.email"
            />
            <span class="focus-input100"></span>
            <span class="symbol-input100">
              <i class="iconfont icon-fa-envelope" aria-hidden="true"></i>
            </span>
          </div>

          <div class="wrap-input100 validate-input">
            <input
              class="input100"
              type="password"
              name="password"
              placeholder="密码"
              v-model="form.password"
            />
            <span class="focus-input100"></span>
            <span class="symbol-input100">
              <i class="iconfont icon-fa-lock" aria-hidden="true"></i>
            </span>
          </div>

          <div class="container-login100-form-btn">
            <button class="login100-form-btn" @click="onSubmit">登陆</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped src="@/assets/css/login.css"></style>
<style scoped src="@/assets/iconfont/iconfont.css"></style>
