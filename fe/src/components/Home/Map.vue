<template>
  <div id="main"></div>
</template>

<script lang="ts" setup>
import * as echarts from 'echarts/core';
import {
  TitleComponent,
  TitleComponentOption,
  TooltipComponent,
  TooltipComponentOption,
  GeoComponent,
  GeoComponentOption,
  GraphicComponent,
  GridComponent
} from 'echarts/components';
import { LinesChart, LinesSeriesOption, GraphSeriesOption, GraphChart } from 'echarts/charts';
import { CanvasRenderer } from 'echarts/renderers';
import { onMounted, defineProps, watch, ref, defineEmits } from 'vue';
echarts.use([
  TitleComponent,
  TooltipComponent,
  GeoComponent,
  LinesChart,
  CanvasRenderer,
  GraphicComponent,
  GraphChart,
  GridComponent
]);
type EChartsOption = echarts.ComposeOption<
  | TitleComponentOption
  | TooltipComponentOption
  | GeoComponentOption
  | LinesSeriesOption
  | GraphSeriesOption
>;
let cur_batch = 0
const props = defineProps(['batch_track']);
watch(props.batch_track, (newVal: track) => {
  if (newVal.batch != cur_batch) {
    option.series[0].data = [{ name: '1', value: [0, 0] }];
    option.series[0].links = [{ source: '1', target: '1' }];
    option.series[0].links = [];
    myChart.setOption(option);
    cur_batch = newVal.batch;
    newVal.truth.length != 0 && showTruth(newVal.truth);
    newVal.pos.length != 0 && showPos(newVal.pos);
    newVal.pdr.length != 0 && showPdr(newVal.pdr);
  }
}, { deep: true })

var chartDom: any;
var myChart: any;
var ecConfig = echarts.config
// var new_option: EChartsOption;
onMounted(() => init());


function showTruth(truth_arr: any) {
  for (let i = 0; i < truth_arr.length; i++) {
    const dot = truth_arr[i];
    option.series[0].data.push({ name: 'truth' + i, value: [dot.x, dot.y], symbolSize: 8, itemStyle: { color: 'red' } });
  }
  myChart.setOption(option);
}

function showPos(pos_arr: any) {
  for (let i = 0; i < pos_arr.length; i++) {
    const dot = pos_arr[i];
    option.series[0].data.push({ name: 'pos' + i, value: [dot.x, dot.y], symbolSize: 6 });
  }
  myChart.setOption(option);
}

function showPdr(pdr_arr: any) {
  for (let i = 0; i < pdr_arr.length; i++) {
    const dot = pdr_arr[i];
    // console.log(dot)
    option.series[0].data.push({ name: 'pdr' + i, value: [dot.x, dot.y], symbolSize: 10, itemStyle: { color: 'green' } });
    if (i < pdr_arr.length - 1) {
      const source = 'pdr' + i;
      let next = i + 1;
      const target = 'pdr' + next;
      option.series[0].links.push({ source, target, ineStyle: { type: 'solid', color: '#aaa', width: 10, }, symbolSize: [1, 8] });
    }
  }
  myChart.setOption(option);
}

const emit = defineEmits(['getCurDot'])
function init() {
  chartDom = document.getElementById('main')!;
  myChart = echarts.init(chartDom);
  const data = [
    {
      name: '1',
      value: [0, 0],
      symbolSize: 10,
      itemStyle: {
        color: 'red'
      }
    }
  ];

  // const links = [
  //   {
  //     source: '1',
  //     target: '2',
  // lineStyle: {
  //   type: 'solid',
  //   color: '#aaa',
  //   width: 2,
  // },
  //     symbolSize: [0, 5]
  //   },
  // ];
  option.series[0].data.push(...data);
  myChart.setOption(option);
  myChart.on('click', 'series', function (params: any) {
    emit('getCurDot', params.data.name);
  });
}
var option = {
  xAxis: {
    type: 'value',
    min: -4.653,
    max: 7.643,
    // data: [-4.653, 7.643]12.296
  },
  yAxis: {
    type: 'value',
    min: -3.906,
    max: 4.694,
    // data: [-3.906, 4.694]8.6
  },
  series: [
    {
      name: 'Route',
      type: 'graph',
      coordinateSystem: 'cartesian2d',
      emphasis: {
        label: {
          show: true
        }
      },
      edgeSymbol: ['none', 'arrow'],
      data: [],
      links: [],
    }
  ],
  grid: { // 让图表占满容器
    top: "0px",
    left: "0px",
    right: "0px",
    bottom: "0px"
  },
  graphic: [
    {
      type: 'image', // 图形元素类型
      id: 'logo', // 更新或删除图形元素时指定更新哪个图形元素，如果不需要用可以忽略。
      right: 'center', // 根据父元素进行定位 （居中）
      bottom: '0%', // 根据父元素进行定位   （0%）, 如果bottom的值是 0，也可以删除该bottom属性值。
      z: 0,  // 层叠
      bounding: 'all', // 决定此图形元素在定位时，对自身的包围盒计算方式
      style: {
        image: 'http://localhost:8888/background.svg', // 这里一定要注意、注意，必须是https开头的图片路径地址
        width: 800,
        height: 559
      }
    }
  ],
};
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

</script>

<style scoped>
#main {
  width: 800px;
  height: 559px;
}
</style>