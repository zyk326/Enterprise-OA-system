<script setup name="listinform">
import { ref, reactive, onMounted } from "vue";
import OAMain from "@/components/OAMain.vue";
import OADialog from "@/components/OADialog.vue";
import OAPagination from "@/components/OAPagination.vue";
import timeFormatter from "@/utils/timeFormatter";
import { useAuthStore } from "@/stores/auth";
import informHttp from "@/api/informHttp";
import { ElMessage } from "element-plus";

let informs = ref([]);
let usAuth = useAuthStore();

let dialogVisible = ref(false);
let handleIndex = 0;
const onShowDialog = (index) => {
  (handleIndex = index), (dialogVisible.value = true);
};

const onDeleteInform = async () => {
  try {
    let inform = informs.value[handleIndex];
    await informHttp.deleteInform(inform.id);
    informs.value.splice(handleIndex, 1);
    ElMessage.success("通知删除成功!");
  } catch (detail) {
    ElMessage.error(detail);
  }
};

const pagination = reactive({
  page: 1,
  total: 0,
});

onMounted(async () => {
  try {
    let data = await informHttp.getInformList(1);
    pagination.total = data.count;
    informs.value = data.results;
  } catch (detail) {
    ElMessage.error(detail);
  }
});
</script>

<template>
  <OADialog v-model="dialogVisible" title="提示" @submit="onDeleteInform">
    <span>您确定要删除这篇通知吗?</span>
  </OADialog>
  <OAMain title="通知列表">
    <el-card>
      <el-table :data="informs" style="width: 100%">
        <el-table-column label="标题">
          <template #default="scope">
            <RouterLink
              :to="{ name: 'inform_detail', params: { pk: scope.row.id } }"
              >{{ scope.row.title }} </RouterLink
            ><el-badge
              v-if="scope.row.reads.length == 0"
              is-dot
              class="item"
            ></el-badge>
          </template>
        </el-table-column>
        <el-table-column label="发布者">
          <template #default="scope">
            {{
              "[" +
              scope.row.author.department.name +
              "]" +
              scope.row.author.realname
            }}
          </template>
        </el-table-column>
        <el-table-column label="发布时间">
          <template #default="scope">
            {{ timeFormatter.stringFromDateTime(scope.row.create_time) }}
          </template>
        </el-table-column>
        <el-table-column label="部门可见">
          <template #default="scope">
            <el-tag v-if="scope.row.public" type="success">公开</el-tag>
            <el-tag
              v-else
              v-for="department in scope.row.departments"
              :key="department.name"
              type="info"
              >{{ department.name }}</el-tag
            >
          </template>
        </el-table-column>
        <el-table-column label="操作">
          <template #default="scope">
            <el-button
              v-if="scope.row.author.uid == usAuth.user.uid"
              type="danger"
              icon="Delete"
              @click="onShowDialog(scope.$index)"
            ></el-button>
            <el-button v-else disabled type="default">无</el-button>
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
.el-tag {
  margin-right: 5px;
}

.el-badge {
  margin-right: 5px;
  margin-top: 5px;
}
</style>
