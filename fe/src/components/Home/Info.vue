<template>
  <div class="box-card">
    <div class="card-header">
      <span>当前位置信息</span>
      <span>{{ props.cur_dot.type }}</span>
    </div>
    <div class="more-info">
      <div v-if="props.cur_dot.type == dot_type.pdr" class="info">
        <div>x:{{ round(show_dot.x, 2) }}</div>
        <div>y:{{ round(show_dot.y, 2) }}</div>
        <div>length:{{ round(show_dot.length, 2) }}</div>
        <div>angle:{{ round(show_dot.angle, 2) }}°</div>
        <div>accx:{{ round(show_dot.accx, 2) }}</div>
        <div>gyroscopex:{{ round(show_dot.gyroscopex, 2) }}</div>
        <div>accy:{{ round(show_dot.accy, 2) }}</div>
        <div>gyroscopey:{{ round(show_dot.gyroscopey, 2) }}</div>
        <div>accz:{{ round(show_dot.accz, 2) }}</div>
        <div>gyroscopez:{{ round(show_dot.gyroscopez, 2) }}</div>
        <div>error:{{ round(show_dot.error, 2) }}</div>
      </div>
      <div v-else class="info">
        <div>x:{{ round(show_dot.x, 2) }}</div>
        <div>y:{{ round(show_dot.y, 2) }}</div>
      </div>
      <div v-if="props.cur_dot.type != dot_type.truth" class="time">time:{{ show_dot.sample_time }}</div>
    </div>
  </div>
  <div class="box-card">
    <div id="cdfbox"></div>
  </div>
</template>

<script lang="ts" setup>
import * as echarts from 'echarts/core';
import { GridComponent } from 'echarts/components';
import { LineChart } from 'echarts/charts';
import { UniversalTransition } from 'echarts/features';
import { CanvasRenderer } from 'echarts/renderers';
import { round } from "lodash";
import { defineProps, ref, watch, onMounted } from 'vue';
import { getCDF } from "./test.js";
echarts.use([GridComponent, LineChart, CanvasRenderer, UniversalTransition]);
const props = defineProps(['cur_dot', 'batch_track']);
const show_dot = ref({} as dot_info);
watch(props.cur_dot, (newVal) => {
  if (newVal.type == dot_type.pdr) {
    show_dot.value = props.batch_track.pdr[newVal.index];
    const err_arr: any = [];
    props.batch_track.pdr.forEach((e: any) => {
      err_arr.push(e.error);
    });
    // cdf
    const { cdf, avg } = getCDF(props.batch_track.truth.length, err_arr);
    option.series[0].data = [{ value: [0, 0] }];
    for (let i of cdf) {
      option.series[0].data.push({ value: [i.x, i.y] });
    }
    option.title.subtext = '平均误差：' + round(avg, 3);
    myChart.setOption(option);
  } else if (newVal.type == dot_type.pos) {
    show_dot.value = props.batch_track.pos[newVal.index];
  } else if (newVal.type == dot_type.truth) {
    show_dot.value = props.batch_track.truth[newVal.index];
  }
});

onMounted(() => {
  init()
})

var chartDom;
var myChart: any;
function init() {
  chartDom = document.getElementById('cdfbox');
  myChart = echarts.init(chartDom);
  option && myChart.setOption(option);
}

var option = {
  title: {
    show: true,
    text: 'CDF曲线',
    x: 'center',
    y: 'top',
    subtext: ''
  },
  xAxis: {
    type: 'value'
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      data: [
        {
          value: [0, 0]
        }
      ],
      type: 'line'
    }
  ]
};


interface dot_info {
  x: number;
  y: number;
  length: number;
  angle: number;
  error: number;
  sample_time: string;
  gyroscopex: number;
  gyroscopey: number;
  gyroscopez: number;
  accx: number;
  accy: number;
  accz: number;
}

enum dot_type {
  pos = 'position',
  pdr = 'pdr',
  truth = 'groundTruth'
}
</script>

<style scoped>
.info {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
}

#cdfbox {
  width: 300px;
  height: 300px;
}

.box-card {
  box-shadow: var(--el-box-shadow-lighter);
  margin-bottom: 10px;
}

.card-header {
  padding: 10px 0;
}

.more-info {
  margin-bottom: 10px;
  padding-bottom: 10px;
}

.time {
  margin-top: 10px;
}
</style>