<template>
  <div class="line-charts">
    <div class="tier-header">
      <h1 class="tierDisplay">
        Tier I Assets
      </h1>
    </div>
    <b-card-group deck>
      <b-card class="line-chart-card" title="Tier I Capital Decomposition - Retained Earnings">
        <div class="line-chart" id="t1-retained-earnings"></div>
      </b-card>
      <b-card class="line-chart-card" title="Tier I Capital Adjustment - Goodwill">
        <div class="line-chart" id="t1-goodwill"></div>
      </b-card>
    </b-card-group>
    <b-card-group deck>
      <b-card class="line-chart-card" title="Tier I Ratio">
        <div class="line-chart" id="tier-1-ratio-overtime"></div>
      </b-card>
      <b-card class="line-chart-card" title="CET I Ratio">
        <div class="line-chart" id="cet-1-ratio-overtime"></div>
      </b-card>
      <b-card class="line-chart-card" title="CET / Tier I Ratio">
        <div class="line-chart" id="cet-vs-tier-1-ratio-overtime"></div>
      </b-card>
    </b-card-group>
    <div class="tier-header">
      <h1 class="tierDisplay">
        Tier II Assets
      </h1>
    </div>
    <b-card-group deck>
      <b-card class="line-chart-card" title="Tier II Ratio">
        <div class="line-chart" id="tier-2-ratio-overtime"></div>
      </b-card>
      <b-card class="line-chart-card" title="Tier II Capital Decomposition - Total Capital Minority Interest">
        <div class="line-chart" id="total-capital-minority-interest-not-included-in-tier-1-overtime"></div>
      </b-card>
      <b-card class="line-chart-card" title="Tier II Asset Deduction Ratio">
        <div class="line-chart" id="tier-two-deduction"></div>
      </b-card>
    </b-card-group>
    <div class="tier-header">
      <h1 class="tierDisplay">
        Exposures
      </h1>
    </div>
    <b-card-group deck>
      <b-card class="line-chart-card" title="On Balance Sheet Exposure">
        <div class="line-chart" id="on-balance-sheet-exposure-overtime"></div>
      </b-card>
      <b-card class="line-chart-card" title="Derivative Exposure">
        <div class="line-chart" id="derivative-exposure-overtime"></div>
      </b-card>
      <b-card class="line-chart-card" title="Repo Exposure">
        <div class="line-chart" id="repo-exposure-overtime"></div>
      </b-card>
      <b-card class="line-chart-card" title="Off-balance Sheet Exposure">
        <div class="line-chart" id="off-balance-exposure-overtime"></div>
      </b-card>
    </b-card-group>
    <b-card-group deck>
      <b-card class="line-chart-card" title="On Balance Sheet Exposure / Total Exposure Ratio">
        <div class="line-chart" id="on-balance-sheet-exposure-ratio-overtime"></div>
      </b-card>
      <b-card class="line-chart-card" title="Derivative Exposure / Total Exposure Ratio">
        <div class="line-chart" id="derivative-exposure-ratio-overtime"></div>
      </b-card>
    </b-card-group>
    <b-card-group deck>
      <b-card class="line-chart-card" title="Repo Exposure / Total Exposure Ratio">
        <div class="line-chart" id="repo-exposure-ratio-overtime"></div>
      </b-card>
      <b-card class="line-chart-card" title="Off-balance Sheet Exposure / Total Exposure Ratio">
        <div class="line-chart" id="off-balance-exposure-ratio-overtime"></div>
      </b-card>
    </b-card-group>
    <div class="tier-header">
      <h1 class="tierDisplay">
        Total Capital Ratios
      </h1>
    </div>
    <b-card-group deck>
      <b-card class="line-chart-card" title="Tier 2 Capital / Total Capital Ratio">
        <div class="line-chart" id="ratio-of-tier-2-capital-and-total-capital-overtime"></div>
      </b-card>
      <b-card class="line-chart-card" title="On Balance Sheet Items / Total Capital Ratio">
        <div class="line-chart" id="ratio-of-total-capital-and-on-balance-sheet-items-overtime"></div>
      </b-card>
      <b-card class="line-chart-card" title="Derivative Assets / Total Capital Ratio">
        <div class="line-chart" id="ratio-of-total-capital-and-derivative-assets"></div>
      </b-card>
    </b-card-group>
    <b-card-group deck>
      <b-card class="line-chart-card" title="Repo Assets / Total Capital Ratio">
        <div class="line-chart" id="ratio-of-total-capital-and-repo-assets"></div>
      </b-card>
      <b-card class="line-chart-card" title="Off Balance Sheet Items / Total Capital Ratio">
        <div class="line-chart" id="ratio-of-total-capital-and-off-balance-sheet-items"></div>
      </b-card>
      <b-card class="line-chart-card" title="RWA / Total Assets Ratio">
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
        't1-retained-earnings': 'getTier1RetainedEarningOvertime',
        't1-goodwill': 'getTier1GoodwillOvertime',
        'total-capital-minority-interest-not-included-in-tier-1-overtime': 'getTier2MinorityIntOvertime',
        'cet-1-ratio-overtime': 'getCET1RatioOvertime',
        'tier-1-ratio-overtime': 'getTier1RatioOvertime',
        'cet-vs-tier-1-ratio-overtime': 'getCETVsTier1RatioOvertime',
        'on-balance-sheet-exposure-overtime': 'getOnBalanceSheetOvertime',
        'derivative-exposure-overtime': 'getDerivativeOvertime',
        'repo-exposure-overtime': 'getRepoOvertime',
        'off-balance-exposure-overtime': 'getOffBalanceOvertime',
        'on-balance-sheet-exposure-ratio-overtime': 'getOnBalanceSheetRatio',
        'derivative-exposure-ratio-overtime': 'getDerivativeExposureRatio',
        'repo-exposure-ratio-overtime': 'getRepoExposureRatio',
        'off-balance-exposure-ratio-overtime': 'getOffBalanceExposureRatio',
        'ratio-of-tier-2-capital-and-total-capital-overtime': 'getT2CTCRatio',
        'ratio-of-total-capital-and-on-balance-sheet-items-overtime': 'getTCOBSIRatio',
        'ratio-of-total-capital-and-derivative-assets': 'getTCDARatio',
        'ratio-of-total-capital-and-repo-assets': 'getTCRARatio',
        'ratio-of-total-capital-and-off-balance-sheet-items': 'getTCOFFBSIRatio',
        'ratio-of-rwa-and-total-assets': 'getRWATARatio',
        'tier-two-deduction': 'getTier2DeductionOvertime',
        'tier-2-ratio-overtime': 'getTier2CapitalRatioOvertime'
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
                  if (id === 'total-exposure-overtime' || id === 'on-balance-sheet-exposure-overtime' || id === 'derivative-exposure-overtime' || id === 'repo-exposure-overtime' || id === 'off-balance-exposure-overtime' || id === 'tier-2-capital-overtime' || id === 'tier-1-capital-overtime' || id === 'total-capital-minority-interest-not-included-in-tier-1-overtime' || id === 't1-retained-earnings' || id === 't1-goodwill') {
                    chartItem.data.push((item[1] / 1000).toFixed(2))
                    pan.push((item[1] / 1000).toFixed(2))
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
                  chartItemOne.axisYIndex = 0
                  for (const item of data[key]) {
                    groupOne.push((item[1] / 1000).toFixed(2))
                    pan.push((item[1] / 1000).toFixed(2))
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
                    groupTwo.push((item[1] / 1000).toFixed(2))
                    panTwo.push((item[1] / 1000).toFixed(2))
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
          // let curMinMinority = Math.floor(Math.min.apply(Math, panTwo))
          // let curMaxMinority = Math.floor(Math.max.apply(Math, panTwo))
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
          let ratioYAxisThree = [
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
              min: curMin - 0.1,
              max: curMax + 1
            }
          ]
          let yAxisOne = {}
          yAxisOne.name = 'Millions - other'
          yAxisOne.scale = true
          yAxisOne.type = 'value'
          yAxisOne.max = 400
          yAxisOne.min = 0
          yAxisOne.axisLabel = {
            formatter: function (value) {
              // Original Amount: Dollar Amounts in Thousands
              // show tick with comma
              return (value).toLocaleString()
            }
          }
          let yAxisTwo = {}
          yAxisTwo.name = 'Millions - BAC/WF'
          yAxisTwo.scale = true
          yAxisTwo.type = 'value'
          // yAxisTwo.max = Math.round(Math.max.apply(Math,groupTwo) + 20);
          // yAxisTwo.min = Math.round(Math.min.apply(Math,groupTwo) - 20);
          yAxisTwo.max = 3000
          yAxisTwo.min = 0
          yAxisTwo.axisLabel = {
            formatter: function (value) {
              // Original Amount: Dollar Amounts in Thousands
              // show tick with comma
              return (value).toLocaleString()
            }
          }

          let yAxisMap = {
            'total-exposure-overtime': millionYAxis,
            'on-balance-sheet-exposure-overtime': millionYAxis,
            'derivative-exposure-overtime': millionYAxis,
            'repo-exposure-overtime': millionYAxis,
            'off-balance-exposure-overtime': millionYAxis,
            'on-balance-sheet-exposure-ratio-overtime': ratioYAxis,
            'derivative-exposure-ratio-overtime': ratioYAxis,
            'repo-exposure-ratio-overtime': ratioYAxis,
            'off-balance-exposure-ratio-overtime': ratioYAxis,
            'tier-2-capital-overtime': millionYAxis,
            'tier-1-capital-overtime': millionYAxis,
            't1-retained-earnings': millionYAxis,
            't1-goodwill': millionYAxis,
            'cet-1-ratio-overtime': ratioYAxisTwo,
            'tier-1-ratio-overtime': ratioYAxisTwo,
            'cet-vs-tier-1-ratio-overtime': ratioYAxisTwo,
            'ratio-of-tier-2-capital-and-total-capital-overtime': ratioYAxisTwo,
            'ratio-of-total-capital-and-on-balance-sheet-items-overtime': ratioYAxisTwo,
            'ratio-of-total-capital-and-derivative-assets': ratioYAxis,
            'ratio-of-total-capital-and-repo-assets': ratioYAxis,
            'ratio-of-total-capital-and-off-balance-sheet-items': ratioYAxisTwo,
            'ratio-of-rwa-and-total-assets': ratioYAxisTwo,
            'tier-two-deduction': ratioYAxisThree,
            'tier-2-ratio-overtime': ratioYAxisTwo
          }
          that.lineChartData.legend = companies
          that.lineChartData.xAxisData = xString
          if (id !== 'total-capital-minority-interest-not-included-in-tier-1-overtime') {
            that.lineChartData.yAxis = yAxisMap[id]
          } else {
            that.lineChartData.yAxis = [yAxisOne, yAxisTwo]
          }
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

.tierDisplay {
  font-family: "Georgia";
  text-align: center;
  margin-bottom: 20px;
  margin-top: 20px;
  font-size: 2em;
}

</style>
