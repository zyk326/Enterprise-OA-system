<script setup name="myabsent">
import OAPageHeader from "@/components/OAPageHeader.vue";
import { ref, reactive, onMounted } from "vue";
import absentHttp from "@/api/absentHttp";
import { ElMessage } from "element-plus";
import formatTime from "@/utils/timeFormatter";
import OAPagination from "@/components/OAPagination.vue";
import OADialog from "@/components/OADialog.vue";
import OAMain from "@/components/OAMain.vue";

let absents = ref([]);

let pagination = reactive({
  total: 0,
  page: 1,
});

let dialogVisible = ref(false);
onMounted(async () => {
  try {
    let data = await absentHttp.getSubAbsents();
    pagination.total = data.count;
    absents.value = data.results;
    console.log(absents.value);
  } catch (detail) {
    ElMessage.error(detail);
  }
});
let handleIndex = null;
const onShowDialog = (index) => {
  (absentForm.status = 2),
    (absentForm.responde_content = ""),
    (dialogVisible.value = true);
  handleIndex = index;
};
let absentFormRef = ref()
let absentForm = reactive({
  status: 2,
  responde_content: "",
});
let rules = reactive({
  status: [{ required: true, message: "请选择处理结果!", trigger: "change" }],
  responde_content: [
    { required: true, message: "请输入反馈意见!", trigger: "blur" },
  ],
});

const onSubmitAbsent = () => {
  console.log("is in");
  absentFormRef.value.validate(async (valid, fields) => {
    if (valid) {
      console.log("in");
      try {
        const absent = absents.value[handleIndex];
        const data = await absentHttp.handleSubAbsent(
          absent.id,
          absentForm.status,
          absentForm.responde_content
        );
        absents.value.splice(handleIndex, 1, data);
      } catch (detail) {
        ElMessage.error(detail);
      }
    }
  });
};
</script>

<template>
  <OADialog title="处理考勤" v-model="dialogVisible" @submit="onSubmitAbsent">
    <el-form
      :model="absentForm"
      :rules="rules"
      ref="absentFormRef"
      label-width="100px"
    >
      <el-form-item label="结果" prop="status">
        <el-radio-group v-model="absentForm.status">
          <el-radio :value="2">通过</el-radio>
          <el-radio :value="3">拒绝</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="反馈意见" prop="responde_content">
        <el-input
          v-model="absentForm.responde_content"
          style="width: 100%"
          type="textarea"
          placeholder="请输入反馈意见"
        />
      </el-form-item>
    </el-form>
  </OADialog>

  <OAMain title="下属考勤">
    <el-card>
      <el-table :data="absents" style="width: 100%">
        <el-table-column prop="title" label="标题" />
        <el-table-column label="发起人">
          <template #default="scope">
            {{
              "[" +
              scope.row.requester.department.name +
              "]" +
              scope.row.requester.realname
            }}
          </template>
        </el-table-column>
        <el-table-column prop="absent_type.name" label="类型" />
        <el-table-column prop="request_content" label="原因" />
        <el-table-column label="发起时间">
          <template #default="scope">
            {{ formatTime.stringFromDateTime(scope.row.create_time) }}
          </template>
        </el-table-column>
        <el-table-column prop="start_date" label="开始日期" />
        <el-table-column prop="end_date" label="结束日期" />
        <el-table-column prop="responder.realname" label="审核领导" />
        <el-table-column prop="response_content" label="反馈意见" />
        <el-table-column label="审核状态">
          <template #default="scope">
            <el-tag type="info" v-if="scope.row.status == 1">审核中</el-tag>
            <el-tag type="success" v-else-if="scope.row.status == 2">已通过</el-tag>
            <el-tag type="danger" v-else>已拒绝</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="处理">
          <template #default="scope">
            <el-button v-if="scope.row.status == 1" type="primary" icon="EditPen" @click="onShowDialog(scope.$index)"></el-button>
            <el-button v-else disabled type="default">完成</el-button>
          </template>
        </el-table-column>
      </el-table>

      <template #footer>
        <OAPagination
          v-model="pagination.page"
          :total="pagination.total"
          :page-size="10"
        ></OAPagination>
      </template>
    </el-card>
  </OAMain>
</template>

<style scoped>
.el-pagination {
  justify-content: center;
}

.el-space :deep(.el-space__item) {
  width: 100%;
}
</style>
