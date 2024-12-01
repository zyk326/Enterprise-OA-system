<script setup name="staff_add">
import { ref, reactive } from "vue";
import staffHttp from "@/api/staffHttp";
import { useRouter } from "vue-router";
import OAMain from "@/components/OAMain.vue";
import { useAuthStore } from "@/stores/auth";
import { ElMessage } from "element-plus";

const router = useRouter();
const authStore = useAuthStore();
let staffForm = reactive({
  email: "",
  password: "",
  realname: "",
});
let formLabelWidth = '60px'
const formRef = ref();
let rules = reactive({
  email: [{ required: true, message: "请输入邮箱！", trigger: "blur" }],
  password: [{ required: true, message: "请输入密码！", trigger: "blur" }],
  realname: [{ required: true, message: "请输入真实姓名！", trigger: "blur" }],
});

const onSubmit = () => {
  formRef.value.validate(async (valid, field) => {
    if (valid) {
      try {
        await staffHttp.addStaff(staffForm.realname, staffForm.email, staffForm.password)
        ElMessage.success('员工添加成功!')
        router.push({ name: 'staff_list' })
      } catch (detail) {
        ElMessage.error(detail)
      }
    }
  })
};
</script>

<template>
  <OAMain title="新增员工">
    <el-card shadow="always">
      <el-form :model="staffForm" :rules="rules" ref="formRef">
        <el-form-item label="姓名" prop="realname" :label-width="formLabelWidth">
          <el-input v-model="staffForm.realname" placeholder="请输入姓名" />
        </el-form-item>

        <el-form-item label="邮箱" prop="email" :label-width="formLabelWidth">
          <el-input v-model="staffForm.email" placeholder="请输入邮箱" />
        </el-form-item>

        <el-form-item label="密码" prop="password" :label-width="formLabelWidth">
          <el-input v-model="staffForm.password" placeholder="请输入密码" />
        </el-form-item>

        <el-form-item label="部门" :label-width="formLabelWidth">
          <el-input readonly disabled :value="authStore.user.department.name" placeholder="请输入部门" />
        </el-form-item>

        <el-form-item label="领导" :label-width="formLabelWidth">
          <el-input readonly disabled :placeholder="'[' + authStore.user.email + ']' + authStore.user.realname
            " />
        </el-form-item>

        <el-form-item>
          <div style="text-align: right; flex: 1">
            <el-button type="primary" @click="onSubmit">提交</el-button>
          </div>
        </el-form-item>
      </el-form>
    </el-card>
  </OAMain>
</template>

<style scoped>
.el-form-item ::v-deep(label) {
  margin-right: 10px;
}
</style>
