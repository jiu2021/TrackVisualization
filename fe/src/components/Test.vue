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
import { onMounted } from 'vue';
import axios from "axios";

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

onMounted(() => init());

function init() {
  var chartDom = document.getElementById('main')!;
  var myChart = echarts.init(chartDom);
  var option: EChartsOption;
  var img_url = 'http://localhost:8890/test.svg';
  // console.log(chartDom)
  axios.get(img_url).then(function (response) {
    register(response.data);
  });
  function register(svg: any) {
    echarts.registerMap('MacOdrum-LV5-floorplan-web', { svg: svg });
    option = {
      title: {
        text: 'Visit Route',
        left: 'center',
        bottom: 10
      },
      tooltip: {},
      geo: {
        map: 'MacOdrum-LV5-floorplan-web',
        // 开启缩放或者平移
        roam: false,
        emphasis: {
          itemStyle: {
            color: undefined
          },
          label: {
            show: false
          }
        }
      },
      series: [
        {
          name: 'Route',
          type: 'lines',
          // 地理坐标系，经纬度
          coordinateSystem: 'geo',
          geoIndex: 0,
          emphasis: {
            label: {
              show: false
            }
          },
          // 多段线
          polyline: true,
          lineStyle: {
            color: '#c46e54',
            width: 5,
            opacity: 1,
            type: 'dotted'
          },
          effect: {
            show: true,
            period: 8,
            color: '#a10000',
            constantSpeed: 80,
            trailLength: 0,
            symbolSize: [20, 12],
            symbol:
              'path://M35.5 40.5c0-22.16 17.84-40 40-40s40 17.84 40 40c0 1.6939-.1042 3.3626-.3067 5H35.8067c-.2025-1.6374-.3067-3.3061-.3067-5zm90.9621-2.6663c-.62-1.4856-.9621-3.1182-.9621-4.8337 0-6.925 5.575-12.5 12.5-12.5s12.5 5.575 12.5 12.5a12.685 12.685 0 0 1-.1529 1.9691l.9537.5506-15.6454 27.0986-.1554-.0897V65.5h-28.7285c-7.318 9.1548-18.587 15-31.2715 15s-23.9535-5.8452-31.2715-15H15.5v-2.8059l-.0937.0437-8.8727-19.0274C2.912 41.5258.5 37.5549.5 33c0-6.925 5.575-12.5 12.5-12.5S25.5 26.075 25.5 33c0 .9035-.0949 1.784-.2753 2.6321L29.8262 45.5h92.2098z'
          },
          data: [
            {
              coords: [
                [110.6189462165178, 456.64349563895087],
                [124.10988522879458, 450.8570048730469],
                [123.9272226116071, 389.9520693708147],
                [61.58708083147317, 386.87942320312504],
                [61.58708083147317, 72.8954315876116],
                [258.29514854771196, 72.8954315876116],
                [260.75457021484374, 336.8559607533482],
                [280.5277985253906, 410.2406672084263],
                [275.948185765904, 528.0254369698661],
                [111.06907909458701, 552.795792593471],
                [118.87138231445309, 701.365737015904],
                [221.36468155133926, 758.7870354617745],
                [307.86195445452006, 742.164737297712],
                [366.8489324762834, 560.9895157073103],
                [492.8750778390066, 560.9895157073103],
                [492.8750778390066, 827.9639780566406],
                [294.9255269587053, 827.9639780566406],
                [282.79803391043527, 868.2476088113839]
              ]
            }
          ]
        }
      ]
    };
    myChart.setOption(new_option);
  }
}

var new_option: EChartsOption;
new_option = {
  title: {
    text: 'TrackVisualization',
    left: 'center',
  },
  tooltip: {},
  geo: {
    map: 'MacOdrum-LV5-floorplan-web',
    // 开启缩放或者平移
    roam: false,
    emphasis: {
      itemStyle: {
        color: undefined
      },
      label: {
        show: false
      }
    }
  },
  xAxis: {
    type: 'value',
    data: [0, 50]
  },
  yAxis: {
    type: 'value',
    data: [0, 50]
  },
  series: [
    {
      name: 'Route',
      type: 'graph',
      // 地理坐标系，经纬度
      coordinateSystem: 'cartesian2d',
      // xAxisIndex: 0,
      // yAxisIndex: 0,
      emphasis: {
        label: {
          show: false
        }
      },
      edgeSymbol: ['none', 'arrow'],
      data: [
        {
          name: '1',
          value: [0, 0],
          symbolSize: 10,
          itemStyle: {
            color: 'red'
          }
        },
        {
          name: '2',
          value: [12, 5],
        },
        {
          name: '3',
          value: [10, 20],
        },
        {
          name: '4',
          value: [30, 34],
        },
        {
          name: '5',
          value: [70, 60],
          symbolSize: 10,
          itemStyle: {
            color: 'red'
          }
        },
      ],
      links: [
        {
          source: '1',
          target: '2',
          lineStyle: {
            type: 'solid',
            color: '#aaa',
            width: 2,
          },
          symbolSize: [0, 5]
        },
        {
          source: '2',
          target: '3',
          lineStyle: {
            type: 'solid',
            color: '#aaa',
            width: 2
          },
          symbolSize: [0, 5]
        }
      ]
    }
  ],
};


</script>

<style scoped>
#main {
  width: 500px;
  height: 800px;
}
</style>