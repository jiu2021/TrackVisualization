<template>
  <div class="list-wrapper">
    <div class="list-header">采样数据</div>
    <ul class="list">
      <li class="item" v-for="(item, index) in sample_arr" :key="index" @click="$emit('showWhich', item)">
        <span>{{ item.batch }}</span>
        <span v-show="item.truth">truth</span>
        <span v-show="item.pos">pos</span>
        <span v-show="item.pdr">pdr</span>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, defineProps, watch } from 'vue'
const props = defineProps(['userInfo']);
watch(props.userInfo, (newInfo) => {
  const { truth_arr, pos_arr, pdr_arr } = newInfo;
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
}

.item {
  height: 50px;
  width: 200px;
  box-shadow: 0px 0px 5px 1px #878787;
  margin-bottom: 10px;
  cursor: pointer;
}
</style>