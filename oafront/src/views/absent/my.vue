<script setup name="myabsent">
import OAPageHeader from "@/components/OAPageHeader.vue";
import { ref, reactive, onMounted, computed, watch } from "vue";
import absentHttp from "@/api/absentHttp";
import { ElMessage } from "element-plus";
import formatTime from "@/utils/timeFormatter";
import OAMain from "@/components/OAMain.vue";
import OAPagination from "@/components/OAPagination.vue";
import OADialog from "@/components/OADialog.vue";

let dialogFormVisible = ref(false);
let absentForm = reactive({
  title: "",
  absent_type_id: null,
  date_range: "",
  request_content: "",
});
let formLabelWidth = 100;
let absent_types = ref([]);
let responder = reactive({
  email: "",
  realname: "",
});
let absentFormRef = ref();
let absents = ref([]);

let onShowDiaglog = () => {
  (absentForm.title = ""),
    (absentForm.absent_type_id = null),
    (absentForm.date_range = ""),
    (absentForm.request_content = "");
  dialogFormVisible.value = true;
};

let onCancleDiaglog = () => {
  (absentForm.title = ""),
    (absentForm.absent_type_id = null),
    (absentForm.date_range = ""),
    (absentForm.request_content = "");
  dialogFormVisible.value = false;
};
let pagination = reactive({
  total: 0,
  page: 1,
});
let rules = reactive({
  title: [{ required: true, message: "请输入标题！", trigger: "blur" }],
  absent_type_id: [
    { required: true, message: "请选择请假类型！", trigger: "change" },
  ],
  date_range: [
    { required: true, message: "请选择请假时间！", trigger: "blur" },
  ],
  request_content: [
    { required: true, message: "请输入请假理由！", trigger: "blur" },
  ],
});
const textarea = ref("");

const onSubmitAbsent = () => {
  absentFormRef.value.validate(async (valid, fields) => {
    if (valid) {
      let data = {
        title: absentForm.title,
        absent_type_id: absentForm.absent_type_id,
        start_date: absentForm.date_range[0],
        end_date: absentForm.date_range[1],
        request_content: absentForm.request_content,
      };
      try {
        let absent = await absentHttp.applyAbsent(data);
        dialogFormVisible.value = false;
        ElMessage.success("发起完成!");
        absents.value.unshift(absent)
      } catch (detail) {
        ElMessage.error(detail);
      }
    }
  });
};

watch(
  () => pagination.page,
  (value) => {
    requestAbsents(value);
  }
);

const requestAbsents = async (page) => {
  try {
    let absents_data = await absentHttp.getMyAbsents(page);
    console.log(absents_data);
    let total = absents_data.count;
    pagination.total = total;
    let results = absents_data.results;
    absents.value = results;
  } catch (detail) {
    ElMessage.error(detail);
  }
};

onMounted(async () => {
  try {
    let absent_types_data = await absentHttp.getAbsentTypes();
    absent_types.value = absent_types_data;

    let responder_data = await absentHttp.getResponder();
    Object.assign(responder, responder_data);

    requestAbsents(1);
  } catch (detail) {
    ElMessage.error(detail);
  }
});

let responder_str = computed(() => {
  if (responder.emial) {
    return "[" + responder.email + "]" + responder.realname;
  } else {
    return "无";
  }
});
</script>

<template>
  <OAMain title="个人考勤">
    <el-card style="text-align: right">
      <el-button type="primary" @click="onShowDiaglog">
        <el-icon><Plus /></el-icon>
        发起考勤
      </el-button>
    </el-card>

    <el-card>
      <el-table :data="absents" style="width: 100%">
        <el-table-column prop="title" label="标题" />
        <el-table-column prop="absent_type.name" label="类型" />
        <el-table-column prop="request_content" label="原因" />
        <el-table-column label="发起时间">
          <template #default="scope">
            {{ formatTime.stringFromDateTime(scope.row.create_time) }}
          </template>
        </el-table-column>
        <el-table-column prop="start_date" label="开始日期" />
        <el-table-column prop="end_date" label="结束日期" />
        <el-table-column label="审核领导">
          {{ responder_str }}
        </el-table-column>
        <el-table-column prop="response_content" label="反馈意见" />
        <el-table-column label="审核状态">
          <template #default="scope">
            <el-tag type="info" v-if="scope.row.status == 1">审核中</el-tag>
            <el-tag type="success" v-else-if="scope.row.status == 2"
              >已通过</el-tag
            >
            <el-tag type="danger" v-else>已拒绝</el-tag>
          </template>
        </el-table-column>
      </el-table>

      <template #footer>
        <OAPagination
          v-model="pagination.page"
          :total="pagination.total"
          :page-size="1"
        ></OAPagination>
      </template>
    </el-card>
  </OAMain>

  <OADialog title="发起考勤" v-model="dialogFormVisible" @click="onSubmitAbsent">
    <el-form :model="absentForm" :rules="rules" ref="absentFormRef">
      <el-form-item label="标题" :label-width="formLabelWidth" prop="title">
        <el-input v-model="absentForm.title" autocomplete="off" />
      </el-form-item>

      <el-form-item
        label="请假类型"
        :label-width="formLabelWidth"
        prop="absent_type_id"
      >
        <el-select
          v-model="absentForm.absent_type_id"
          placeholder="请选择请假类型"
        >
          <el-option
            v-for="item in absent_types"
            :label="item.name"
            :value="item.id"
            :key="item.name"
          />
        </el-select>
      </el-form-item>

      <el-form-item
        label="请假时间"
        :label-width="formLabelWidth"
        prop="date_range"
      >
        <el-date-picker
          v-model="absentForm.date_range"
          type="daterange"
          range-separator="到"
          start-placeholder="起始日期"
          end-placeholder="结束日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
        />
      </el-form-item>

      <el-form-item label="审批领导" :label-width="formLabelWidth">
        <el-input :value="responder_str" readonly disabled autocomplete="off" />
      </el-form-item>

      <el-form-item
        label="请假理由"
        :label-width="formLabelWidth"
        prop="request_content"
      >
        <el-input
          v-model="absentForm.request_content"
          style="width: 100%"
          type="textarea"
          placeholder="请输入请假理由"
        />
      </el-form-item>
    </el-form>
  </OADialog>
</template>

<style scoped></style>
