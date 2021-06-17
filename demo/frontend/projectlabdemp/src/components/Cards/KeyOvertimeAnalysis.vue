<template>
  <div class="line-charts">
    <b-card-group deck>
      <b-card class="line-chart-card" title="Tier I Capital">
        <div class="line-chart" id="tier-1-capital-overtime"></div>
      </b-card>
      <b-card class="line-chart-card" title="Tier II Capital">
        <div class="line-chart" id="tier-2-capital-overtime"></div>
      </b-card>
    </b-card-group>
    <b-card-group deck>
      <b-card class="line-chart-card" title="Tier I Capital Ratio">
        <div class="line-chart" id="tier-1-ratio-overtime"></div>
      </b-card>
      <b-card class="line-chart-card" title="Total Exposure">
        <div class="line-chart" id="total-exposure-overtime"></div>
      </b-card>
      <b-card class="line-chart-card" title="Risk Weighted Assets/Total Assets">
        <div class="line-chart" id="ratio-of-rwa-and-total-assets"></div>
      </b-card>
    </b-card-group>
  </div>
</template>

<script>
import myAPI from '../../api'
import helper from '../../helper'
import * as echarts from 'echarts'

export default {
  name: 'LineChart',
  created () {
    this.getQuarterList = helper.getQuarterList
  },
  data: function () {
    return {
      lineChartData: {}
    }
  },
  methods: {
    drawLineChart (id) {
      let that = this
      let chartDom = document.getElementById(id)
      let myChart = echarts.getInstanceByDom(chartDom)
      if (myChart == null) {
        myChart = echarts.init(chartDom)
      }
      let option = {
        legend: {
          bottom: 0,
          data: that.lineChartData.legend
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
        xAxis: {
          type: 'category',
          data: that.lineChartData.xAxisData
        },
        yAxis: that.lineChartData.yAxis,
        tooltip: {
          trigger: 'axis'
        },
        series: that.lineChartData.series
      }
      myChart.setOption(option, true)
    },
    getDataLine (id, quarter1, quarter2, selected) {
      let that = this
      let endpointDict = {
        'tier-1-capital-overtime': 'getTier1CapitalOvertime',
        'tier-2-capital-overtime': 'getTier2CapitalOvertime',
        'tier-1-ratio-overtime': 'getTier1RatioOvertime',
        'total-exposure-overtime': 'getTotalExposureOvertime',
        'ratio-of-rwa-and-total-assets': 'getRWATARatio'
      }
      const start = quarter1
      const end = quarter2
      let xString = that.getQuarterList(start, end)
      myAPI
        .getDataOvertime(endpointDict[id], start, end)
        .then(function (response) {
          let data = response.data
          console.log(data)
          let companies = []
          let series = []
          let pan = []
          let panTwo = []
          if (id !== 'total-capital-minority-interest-not-included-in-tier-1-overtime') {
            for (let key of selected) {
              if (data.hasOwnProperty(key)) {
                companies.push(key)
                let chartItem = {}
                chartItem.name = key
                chartItem.type = 'line'
                chartItem.data = []
                for (const item of data[key]) {
                  if (id === 'total-exposure-overtime' || id === 'tier-2-capital-overtime' || id === 'tier-1-capital-overtime' || id === 'total-capital-minority-interest-not-included-in-tier-1-overtime') {
                    chartItem.data.push((item[1] / 1000000).toFixed(2))
                    pan.push((item[1] / 1000000).toFixed(2))
                  } else if (id === 'cet-1-ratio-overtime' || id === 'tier-1-ratio-overtime') {
                    chartItem.data.push(item[1].toFixed(2))
                    pan.push(item[1])
                  } else {
                    chartItem.data.push((item[1] * 100).toFixed(2))
                    pan.push(item[1] * 100)
                  }
                }
                series.push(chartItem)
              }
            }
          } else {
            for (let key of selected) {
              if (key !== 'BAC' && key !== 'WF') {
                console.log(key)
                if (data.hasOwnProperty(key)) {
                  companies.push(key)
                  let groupOne = []
                  let chartItemOne = {}
                  chartItemOne.name = key
                  chartItemOne.type = 'line'
                  chartItemOne.data = []
                  for (const item of data[key]) {
                    groupOne.push((item[1] / 1000000).toFixed(2))
                    pan.push((item[1] / 1000000).toFixed(2))
                  }
                  chartItemOne.data = groupOne
                  series.push(chartItemOne)
                }
              } else {
                if (data.hasOwnProperty(key)) {
                  companies.push(key)
                  let groupTwo = []
                  let chartItemTwo = {}
                  chartItemTwo.name = key
                  chartItemTwo.type = 'line'
                  chartItemTwo.data = []
                  chartItemTwo.yAxisIndex = 1
                  for (const item of data[key]) {
                    groupTwo.push((item[1] / 1000000).toFixed(2))
                    panTwo.push((item[1] / 1000000).toFixed(2))
                  }
                  chartItemTwo.data = groupTwo
                  series.push(chartItemTwo)
                }
              }
            }
          }
          console.log(companies)
          console.log(series)
          let curMin = Math.floor(Math.min.apply(Math, pan))
          let curMax = Math.floor(Math.max.apply(Math, pan))
          let curMinMinority = Math.floor(Math.min.apply(Math, panTwo))
          let curMaxMinority = Math.floor(Math.max.apply(Math, panTwo))
          let millionYAxis = [
            {
              type: 'value',
              name: 'Millions',
              axisLabel: {
                formatter: function (value) {
                  // Original Amount: Dollar Amounts in Thousands
                  // show tick with comma
                  return (value).toLocaleString()
                }
              },
              min: curMin - 0.3 * curMax,
              max: curMax + 0.3 * curMax
            }
          ]
          let millionYAxisTwo = [
            {
              type: 'value',
              name: 'Millions',
              axisLabel: {
                formatter: function (value) {
                  // Original Amount: Dollar Amounts in Thousands
                  // show tick with comma
                  return (value).toLocaleString()
                }
              },
              min: curMinMinority - 0.3 * curMinMinority,
              max: curMaxMinority + 0.3 * curMaxMinority
            }
          ]
          let ratioYAxis = [
            {
              type: 'value',
              name: 'percent',
              axisLabel: {
                formatter: function (value) {
                  // Original Amount: Dollar Amounts in Thousands
                  // show tick with comma
                  return (value).toLocaleString()
                }
              },
              min: curMin - 10,
              max: curMax + 10
            }
          ]
          let ratioYAxisTwo = [
            {
              type: 'value',
              name: 'percent',
              axisLabel: {
                formatter: function (value) {
                  // Original Amount: Dollar Amounts in Thousands
                  // show tick with comma
                  return (value).toLocaleString()
                }
              },
              min: curMin - 3,
              max: curMax + 3
            }
          ]
          let yAxisMap = {
            'total-exposure-overtime': millionYAxis,
            'on-balance-sheet-exposure-ratio-overtime': ratioYAxis,
            'derivative-exposure-ratio-overtime': ratioYAxis,
            'repo-exposure-ratio-overtime': ratioYAxis,
            'tier-2-capital-overtime': millionYAxis,
            'tier-1-capital-overtime': millionYAxis,
            'cet-1-ratio-overtime': ratioYAxisTwo,
            'tier-1-ratio-overtime': ratioYAxisTwo,
            'cet-vs-tier-1-ratio-overtime': ratioYAxisTwo,
            'total-capital-minority-interest-not-included-in-tier-1-overtime': [millionYAxis, millionYAxisTwo],
            'ratio-of-tier-2-capital-and-total-capital-overtime': ratioYAxisTwo,
            'ratio-of-total-capital-and-on-balance-sheet-items-overtime': ratioYAxisTwo,
            'ratio-of-total-capital-and-derivative-assets': ratioYAxis,
            'ratio-of-total-capital-and-repo-assets': ratioYAxis,
            'ratio-of-total-capital-and-off-balance-sheet-items': ratioYAxisTwo,
            'ratio-of-rwa-and-total-assets': ratioYAxisTwo
          }
          that.lineChartData.legend = companies
          that.lineChartData.xAxisData = xString
          that.lineChartData.yAxis = yAxisMap[id]
          that.lineChartData.series = series
          that.drawLineChart(id)
        })
    }
  }
}

</script>

<style scoped>

.line-chart-card {
  max-width: 100rem;
  max-height: 60rem;
  margin-bottom: 20px;
}

.line-chart-card {
  font-family: "Georgia";
}

.line-chart {
  width: 100%;
  height: 35rem;
  display: inline-block;
}

</style>
