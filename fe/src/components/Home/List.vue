<template>
  <div class="list-wrapper">
    <div class="list-header">采样数据</div>
    <ul class="list">
      <li class="item" v-for="(item, index) in sample_arr" :key="index" @click="showCur(item)" :style="{
        boxShadow: cur_batch == item.batch ? 'var(--el-box-shadow-dark)' : '',
      }">
        <span>batch{{ item.batch }}</span>
        <el-tag class="ml-2" type="danger" v-show="item.truth">truth</el-tag>
        <el-tag class="ml-2" v-show="item.pos">pos</el-tag>
        <el-tag class="ml-2" type="success" v-show="item.pdr">pdr</el-tag>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, defineProps, watch, defineEmits } from 'vue'
const props = defineProps(['userInfo']);
const emit = defineEmits(['showWhich']);
const cur_batch = ref(0)
const showCur = (item: batch) => {
  emit('showWhich', item);
  cur_batch.value = item.batch;
}
watch(props.userInfo, (newInfo) => {
  const { truth_arr, pos_arr, pdr_arr } = newInfo;
  sample_arr.value = [] as Array<batch>;
  for (let i of truth_arr) {
    sample_arr.value.push({ batch: i, truth: true, pos: pos_arr.includes(i), pdr: pdr_arr.includes(i) });
  }
}, { deep: true });
const sample_arr = ref([] as Array<batch>);
onMounted(() => {
  // for (let i = 27; i <= 32; i++) {
  //   sample_arr.value.push({
  //     batch: i,
  //     truth: true,
  //     pos: true,
  //     pdr: true,
  //   });
  // }
});
interface batch {
  batch: number,
  truth: boolean,
  pos: boolean,
  pdr: boolean,
}
</script>

<style scoped>
ul {
  list-style: none;
  padding-left: 20px;
}

.item {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 250px;
  height: 50px;
  /* box-shadow: 0px 0px 5px 1px #878787; */
  box-shadow: var(--el-box-shadow-lighter);
  margin-bottom: 10px;
  border-radius: 3px;
  cursor: pointer;
  transition: all .3s;
}

.item:hover {
  box-shadow: var(--el-box-shadow-dark);
}

.ml-2 {
  margin: 0 3px;
}
.list {
  height: 70vh;
  overflow-y: scroll;
}
</style>