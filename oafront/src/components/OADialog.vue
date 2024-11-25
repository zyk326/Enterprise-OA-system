<script setup name="OADialog">

import {defineEmits, defineModel, defineProps} from 'vue'

let props = defineProps({
    title:{
        type:String,
        default:''
    },
    width:{
        type:String,
        defalut:'500'
    }
})

let FormVisible = defineModel({required:true})

const emits = defineEmits(['cancel', 'submit'])

const onCancel = () => {
    FormVisible.value = false
    emits('cancel')
}

const onSubmit = () => {
    console.log("insub")
    FormVisible.value = false
    emits('submit')
    console.log("finish upper")
}

</script>

<template>
  <el-dialog v-model="FormVisible" :title="props.title" :width="props.width">
    <slot></slot>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="onCancel">取消</el-button>
        <el-button type="primary" @click="onSubmit"> 提交 </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style scoped></style>
