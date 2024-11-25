<script setup name="OAPageHeader">
import { useRouter } from "vue-router";

const router = useRouter();
const goBack = () => {
  router.go(-1);
};

import {defineProps} from 'vue'

let props = defineProps({
    content:''
})
</script>

<template>
  <el-page-header @back="goBack" :icon="ArrowLeft" title="返回">
    <template #content>
      <span class="text-large font-600 mr-3"> {{ props.content }} </span>
    </template>
  </el-page-header>
</template>

<style scoped></style>
