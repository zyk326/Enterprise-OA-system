<script setup name="frame">
import { ref, computed, reactive, onMounted } from "vue";
import authHttp from "@/api/authHttp";
import { ElMessage } from "element-plus";

import {
  Check,
  Delete,
  Edit,
  Message,
  Search,
  Star,
} from "@element-plus/icons-vue";
import routes from '@/router/frame'

let defaultActive = ref('home')

let isCollapse = ref(true);
let asideWidth = computed(() => {
  if (isCollapse.value) {
    return "64px";
  } else {
    return "250px";
  }
});

let displayUser = reactive({
  department: {},
  realname: ""
})

const onCollapseAside = () => {
  isCollapse.value = !isCollapse.value;
};

import { useAuthStore } from "@/stores/auth";
let authStore = useAuthStore();

import { useRouter } from "vue-router";
let router = useRouter();
const onExit = () => {
  authStore.clearUserToken();
  router.push({ name: "login" });
};


let formTag = ref()
let dialogVisible = ref(false)
let formLabelWidth = 100
let resetPwdForm = reactive({
  oldpwd: '',
  pwd1: '',
  pwd2: ''
})

const onControlResetPwd = () => {
  resetPwdForm.oldpwd = ''
  resetPwdForm.pwd1 = ''
  resetPwdForm.pwd2 = ''
  dialogVisible.value = true
}
let rules = reactive({
  oldpwd: [
    { required: true, message: '请输入旧密码!', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度需在6~20之间!', trigger: 'blur' }
  ],
  pwd1: [
    { required: true, message: '请输入新密码!', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度需在6~20之间!', trigger: 'blur' }
  ],
  pwd2: [
    { required: true, message: '请输入确认密码!', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度需在6~20之间!', trigger: 'blur' }
  ],
})

const onSubmit = () => {
  formTag.value.validate(async (valid, fields) => {
    if (valid) {
      try {
        await authHttp.resetPwd(resetPwdForm.oldpwd, resetPwdForm.pwd1, resetPwdForm.pwd2)
        ElMessage.success("密码修改成功!")
      } catch (detail) {
        ElMessage.error(detail)
      }
    } else {
      ElMessage.info("请按要求输入字段!")
    }
    console.log(fields)
  })
}

onMounted(() => {
  defaultActive.value = router.currentRoute.value.name
  displayUser.department = authStore.user.department
  displayUser.realname = authStore.user.realname
})
</script>

<template>
  <el-container class="container">
    <el-aside class="aside" :width="asideWidth">
      <RouterLink to="/" class="brand">
        <span v-show="!isCollapse">项目</span>
        <strong>OA</strong>
        <span v-show="!isCollapse">系统</span>
      </RouterLink>

      <el-menu active-text-color="#ffd04b" background-color="#343a40" class="el-menu-vertical-demo"
        :default-active="defaultActive" text-color="#fff" :collapse="isCollapse" :collapse-transition="false"
        :router="true">


        <template v-for="route in routes[0].children">
          <template v-if="authStore.has_permission(route.meta.permissions, route.meta.opt)">

            <el-menu-item v-if="!route.children" :index="route.name" :route="{ name: route.name }">
              <el-icon>
                <component :is="route.meta.icon"></component>
              </el-icon>
              <span>{{ route.meta.text }}</span>
            </el-menu-item>

            <el-sub-menu v-else :index="route.name">

              <template #title>
                <el-icon>
                  <component :is="route.meta.icon"></component>
                </el-icon>
                <span>{{ route.meta.text }}</span>
              </template>

              <template v-for="child in route.children">
                <template v-if="authStore.has_permission(child.meta.permissions, child.meta.opt)">
                  <el-menu-item v-if="!child.meta.hidden" :index="child.name" :route="{ name: child.name }">
                    <el-icon>
                      <component :is="child.meta.icon"></component>
                    </el-icon>
                    <span>{{ child.meta.text }}</span>
                  </el-menu-item></template>

              </template>


            </el-sub-menu>

          </template>

        </template>


      </el-menu>

    </el-aside>

    <el-container>
      <el-header class="header">
        <div class="left-header">
          <el-icon v-show="isCollapse" @click="onCollapseAside">
            <Expand />
          </el-icon>
          <el-icon v-show="!isCollapse" @click="onCollapseAside">
            <Fold />
          </el-icon>
        </div>
        <div class="right-header">
          <!-- <el-button :icon="Search"></el-button> -->
          <el-dropdown>
            <span class="el-dropdown-link">
              <el-avatar :size="30" icon="UserFilled" />
              <span style="margin-left: 10px">[{{ displayUser.department.name }}]{{
                displayUser.realname
              }}</span>
              <el-icon class="el-icon--right">
                <arrow-down />
              </el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item :onclick="onControlResetPwd">修改密码</el-dropdown-item>
                <el-dropdown-item divided @click="onExit">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <el-main class="main">
        <RouterView></RouterView>
      </el-main>

    </el-container>
  </el-container>

  <el-dialog v-model="dialogVisible" title="修改密码" width="500">
    <el-form :model="resetPwdForm" :rules="rules" ref="formTag">
      <el-form-item label="旧密码" :label-width="formLabelWidth" prop="oldpwd">
        <el-input v-model="resetPwdForm.oldpwd" autocomplete="off" type="password" />
      </el-form-item>

      <el-form-item label="新密码" :label-width="formLabelWidth" prop="pwd1">
        <el-input v-model="resetPwdForm.pwd1" autocomplete="off" type="password" />
      </el-form-item>

      <el-form-item label="确认密码" :label-width="formLabelWidth" prop="pwd2">
        <el-input v-model="resetPwdForm.pwd2" autocomplete="off" type="password" />
      </el-form-item>

    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="onSubmit">
          确认
        </el-button>
      </div>
    </template>
  </el-dialog>


</template>

<style scoped>
.container {
  height: 100vh;
}

.aside {
  background-color: #343a40;
  box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22) !important;
}

.aside .brand {
  color: #fff;
  text-decoration: none;
  border-bottom: 1px solid #434a50;
  background-color: #232631;
  height: 60px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 20px;
}

.header {
  height: 60px;
  background-color: #fff;
  border-bottom: 1px solid #e6e6e6;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.main {}

.el-menu {
  border-right: none;
}

.el-dropdown-link {
  display: flex;
  align-items: center;
}
</style>
