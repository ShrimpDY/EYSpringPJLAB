<template>
  <div class="stack-bar-charts">
    <b-card-group deck>
      <b-card class="stack-bar-chart-card" title="Total Capital Breakdown">
        <div class="stack-bar-chart" id="total-capital-breakdown"></div>
      </b-card>
      <b-card class="stack-bar-chart-card" title="Total RWA Assets">
        <div class="stack-bar-chart" id="total-rwa-assets"></div>
      </b-card>
    </b-card-group>
    <b-card-group deck>
      <b-card class="stack-bar-chart-card" title="Key Ratios">
        <div class="stack-bar-chart" id="key-ratios"></div>
      </b-card>
      <b-card class="stack-bar-chart-card" title="Key Buffers">
        <div class="stack-bar-chart" id="key-buffers"></div>
      </b-card>
      <b-card class="stack-bar-chart-card" title="Key Exposures">
        <div class="stack-bar-chart" id="key-exposures"></div>
      </b-card>
    </b-card-group>
  </div>
</template>

<script>
import myAPI from '../../api'
import * as echarts from 'echarts'

export default {
  name: 'StackBarChart',
  data: function () {
    return {
      barChartData: {}
    }
  },
  methods: {
    drawStackBarChart (id) {
      let that = this
      let chartDom = document.getElementById(id)
      let myChart = echarts.getInstanceByDom(chartDom)
      if (myChart == null) {
        myChart = echarts.init(chartDom)
      }
      let option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          top: 'bottom',
          data: that.barChartData.legend
        },
        toolbox: {
          show: true,
          orient: 'vertical',
          left: 'right',
          top: 'center',
          feature: {
            mark: {show: true},
            dataView: {show: true, readOnly: false},
            magicType: {show: true, type: ['line', 'bar', 'stack', 'tiled']},
            restore: {show: true},
            saveAsImage: {show: true}
          }
        },
        xAxis: [
          {
            type: 'category',
            axisTick: {show: false},
            data: that.barChartData.xAxisData
          }
        ],
        yAxis: that.barChartData.yAxis,
        series: that.barChartData.series
      }
      myChart.setOption(option, true)
    },
    DrawBarChart (id) {
      let that = this
      let chartDom = document.getElementById(id)
      let myChart = echarts.getInstanceByDom(chartDom)
      if (myChart == null) {
        myChart = echarts.init(chartDom)
      }
      let option = {
        title: {
          show: false
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          data: that.barChartData.legendData,
          y: 'bottom'
        },
        toolbox: {
          show: true,
          orient: 'vertical',
          left: 'right',
          top: 'center',
          feature: {
            mark: {show: true},
            dataView: {show: true, readOnly: false},
            magicType: {show: true, type: ['line', 'bar', 'stack', 'tiled']},
            restore: {show: true},
            saveAsImage: {show: true}
          }
        },
        xAxis: [
          {
            type: 'category',
            axisTick: {show: false},
            data: that.barChartData.xAxisData
          }
        ],
        yAxis: that.barChartData.yAxis,
        series: that.barChartData.series
      }
      myChart.setOption(option, true)
    },
    getDataStack (id, quarter, selected) {
      let that = this
      that.chartData = {}
      let endpointDict = {
        'total-capital-breakdown': 'getTotalCapitalStack',
        'key-buffers': 'getBufferStack',
        'key-exposures': 'getTotalExposureDecomposition'
      }
      myAPI
        .getDataByQuarter(endpointDict[id], quarter)
        .then(function (response) {
          let data = response.data
          let companies = []
          let series = []
          for (let key in data) {
            if (data.hasOwnProperty(key)) {
              let chartItem = {}
              chartItem.name = key
              chartItem.type = 'bar'
              chartItem.data = []
              chartItem.stack = 'total'
              if (id === 'buffers-stack-bar-chart') {
                chartItem.label = {show: true}
              } else {
                chartItem.label = {show: true}
              }
              chartItem.emphasis = {focus: 'series'}
              for (let selectComp of selected) {
                let flag = 0
                for (const item of data[key]) {
                  if (selectComp === item[0]) {
                    if (id === 'total-capital-breakdown' || id === 'key-exposures') {
                      chartItem.data.push(Math.round(item[1] / 1000))
                    } else {
                      chartItem.data.push(Math.round(item[1]))
                    }
                    companies.push(item[0])
                    flag = 1
                  }
                }
                if (flag === 0) {
                  chartItem.data.push(0)
                }
              }
              series.push(chartItem)
            }
          }
          console.log(companies)
          console.log(series)
          let yAxisMap = {
            'total-capital-breakdown': [
              {
                type: 'value',
                name: 'Millions',
                axisLabel: {
                  formatter: function (value) {
                    // Original Amount: Dollar Amounts in Thousands
                    // show tick with comma
                    return (value).toLocaleString()
                  }
                }
              }
            ],
            'key-exposures': [
              {
                type: 'value',
                name: 'Millions',
                axisLabel: {
                  formatter: function (value) {
                    // Original Amount: Dollar Amounts in Thousands
                    // show tick with comma
                    return (value).toLocaleString()
                  }
                }
              }
            ],
            'key-buffers': [
              {
                type: 'value',
                name: 'Percentage',
                axisLabel: {
                  formatter: function (value) {
                    // Original Amount: Dollar Amounts in Thousands
                    // show tick with comma
                    return (value).toLocaleString()
                  }
                }
              }
            ]
          }
          that.barChartData.xAxisData = selected
          that.barChartData.yAxis = yAxisMap[id]
          that.barChartData.series = series
          that.drawStackBarChart(id)
        })
    },
    getDataBar (id, quarter, selected) {
      let that = this
      that.chartData = {}
      let endpointDict = {
        'key-ratios': 'getKeyRatios',
        'total-rwa-assets': 'getTotalRWA'
      }
      myAPI
        .getDataByQuarter(endpointDict[id], quarter)
        .then(function (response) {
          let data = response.data
          let companies = []
          let series = []
          for (let key in data) {
            if (data.hasOwnProperty(key)) {
              let chartItem = {}
              chartItem.name = key
              chartItem.type = 'bar'
              chartItem.data = []
              chartItem.label = {show: true}
              chartItem.emphasis = {focus: 'series'}
              for (let selectComp of selected) {
                let flag = 0
                for (const item of data[key]) {
                  if (selectComp === item[0]) {
                    if (id === 'total-rwa-assets') {
                      chartItem.data.push(Math.round(item[1] / 1000))
                    } else {
                      chartItem.data.push(Math.round(item[1]))
                    }
                    companies.push(item[0])
                    flag = 1
                  }
                }
                if (flag === 0) {
                  chartItem.data.push(0)
                }
              }
              series.push(chartItem)
            }
          }
          console.log(companies)
          console.log(series)
          let yAxisMap = {
            'key-ratios': [
              {
                type: 'value',
                name: 'Percentage',
                axisLabel: {
                  formatter: function (value) {
                    // Original Amount: Dollar Amounts in Thousands
                    // show tick with comma
                    return (value).toLocaleString()
                  }
                }
              }
            ],
            'total-rwa-assets': [
              {
                type: 'value',
                name: 'Million',
                axisLabel: {
                  formatter: function (value) {
                    // Original Amount: Dollar Amounts in Thousands
                    // show tick with comma
                    return (value).toLocaleString()
                  }
                }
              }
            ]
          }
          that.barChartData.xAxisData = selected
          that.barChartData.yAxis = yAxisMap[id]
          that.barChartData.series = series
          that.drawStackBarChart(id)
        })
    }
  }
}

</script>

<style scoped>

.stack-bar-chart-card {
  max-width: 100rem;
  max-height: 60rem;
  margin-bottom: 20px;
}

.stack-bar-chart {
  width: 100%;
  height: 35rem;
  display: inline-block;
}

.stack-bar-chart-card {
  font-family: "Georgia";
}

</style>
