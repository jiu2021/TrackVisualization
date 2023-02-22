<template>
  <div class="common-layout">
    <el-container>
      <el-header>
        <Header @getUserInfo="getUserInfo"></Header>
      </el-header>
      <el-container>
        <el-aside width="280px">
          <List @showWhich="showWhich" :userInfo="userInfo"></List>
        </el-aside>
        <el-main>
          <Map :batch_track="batch_track" @getCurDot="getCurDot"></Map>
        </el-main>
        <el-aside width="300px">
          <Info :cur_dot="cur_dot" :batch_track="batch_track"></Info>
        </el-aside>
      </el-container>
    </el-container>
  </div>
</template>


<script lang="ts" setup>
import Header from './Header.vue';
import List from './List.vue';
import Map from './Map.vue'
import Info from './Info.vue';

import { ref, onMounted, watch } from "vue";
import { reqPdrTrack, reqPosTrack, reqTruthTrack, reqUserData } from '@/api';
const cur_batch = ref({
  batch: 0,
  truth: true,
  pos: true,
  pdr: true,
});
const showWhich = (item: any) => {
  cur_batch.value.batch = item.batch;
  cur_batch.value.truth = item.truth;
  cur_batch.value.pos = item.pos;
  cur_batch.value.pdr = item.pdr;
}
const userInfo = ref({
  account: '',
  username: '',
  pdr_arr: [],
  pos_arr: [],
  truth_arr: []
});
const getUserInfo = () => {
  refreshInfo();
}
onMounted(() => {
  refreshInfo();
});

const batch_track = ref({
  batch: 0,
  truth: [],
  pos: [],
  pdr: []
} as track);
watch(cur_batch.value, (newVal: batch) => {
  batch_track.value.batch = newVal.batch;
  reqTruthTrack({ batch: newVal.batch }).then(function (res) {
    if (res.data.code == 200) {
      batch_track.value.truth = res.data.data;
    }
  });
  reqPosTrack({ batch: newVal.batch }).then(function (res) {
    if (res.data.code == 200) {
      batch_track.value.pos = res.data.data;
    }
  });
  reqPdrTrack({ batch: newVal.batch, direction: -90 }).then(function (res) {
    if (res.data.code == 200) {
      batch_track.value.pdr = res.data.data;
    }
  })
});

const cur_dot = ref({
  type: 'groundTruth',
  index: 0,
} as dot);
const getCurDot = (dotname: any) => {
  if (dotname.includes('truth')) {
    cur_dot.value.type = dot_type.truth;
    cur_dot.value.index = parseInt(dotname.split('truth')[1]);
  } else if (dotname.includes('pos')) {
    cur_dot.value.type = dot_type.pos;
    cur_dot.value.index = parseInt(dotname.split('pos')[1]);
  } else if (dotname.includes('pdr')) {
    cur_dot.value.type = dot_type.pdr;
    cur_dot.value.index = parseInt(dotname.split('pdr')[1]);
  }
}

function refreshInfo() {
  reqUserData().then(function (res) {
    if (res.data.code == 200) {
      const { account, username, pdr_arr, pos_arr, truth_arr } = res.data.data;
      userInfo.value.account = account;
      userInfo.value.username = username;
      userInfo.value.pdr_arr = pdr_arr;
      userInfo.value.pos_arr = pos_arr;
      userInfo.value.truth_arr = truth_arr;
    }
  });
}

interface track {
  batch: number;
  truth: Array<any>;
  pos: Array<any>;
  pdr: Array<any>;
}
interface batch {
  batch: number,
  truth: boolean,
  pos: boolean,
  pdr: boolean,
}
interface dot {
  type: dot_type;
  index: number;
}
enum dot_type {
  pos = 'position',
  pdr = 'pdr',
  truth = 'groundTruth'
}
</script>

<style scoped></style>