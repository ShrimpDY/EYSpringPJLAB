<template>
  <div class="stack-bar-charts">
    <div class="tier-header">
      <h1 class="tierDisplay">
        Tier I Assets
      </h1>
    </div>
    <b-card-group deck>
      <b-card class="stack-bar-chart-card" title="Tier I Capital Adjustments and Deduction">
        <div class="stack-bar-chart" id="tier-one-capital-adjustments"></div>
      </b-card>
      <b-card class="stack-bar-chart-card" title="Tier I Capital Composition">
        <div class="stack-bar-chart" id="tier-one-capital-composition"></div>
      </b-card>
    </b-card-group>
    <div class="tier-header">
      <h1 class="tierDisplay">
        Tier II Assets
      </h1>
    </div>
    <b-card-group deck>
      <b-card class="stack-bar-chart-card" title="Tier II Capital Adjustments and Deduction">
        <div class="stack-bar-chart" id="tier-two-capital-adjustments"></div>
      </b-card>
      <b-card class="stack-bar-chart-card" title="Tier II Capital Composition">
        <div class="stack-bar-chart" id="tier-two-capital-composition"></div>
      </b-card>
    </b-card-group>
    <div class="tier-header">
      <h1 class="tierDisplay">
        Exposures
      </h1>
    </div>
    <b-card-group deck>
      <b-card class="stack-bar-chart-card" title="Total Consolidated Assets Adjustment">
        <div class="stack-bar-chart" id="total-consolidated-assets-adjustment"></div>
      </b-card>
      <b-card class="stack-bar-chart-card" title="Comparison Of Accounting Assets and Total Exposure">
        <div class="stack-bar-chart" id="comparison-of-accounting-assets-and-total-exposure"></div>
      </b-card>
    </b-card-group>
    <b-card-group deck>
      <b-card class="stack-bar-chart-card" title="Total Capital Change vs. Total Derivative Exposure Change">
        <div class="stack-bar-chart" id="total-capital-total-derivative-comparison"></div>
      </b-card>
      <b-card class="stack-bar-chart-card" title="Tier I Leverage Ratio vs. Supplementary Leverage Ratio">
        <div class="stack-bar-chart" id="tier-1-supplementary-comparison"></div>
      </b-card>
    </b-card-group>
    <b-card-group deck>
      <b-card class="bar-line-chart-card" title="Total On Balance Sheet Exposure">
        <div class="bar-line-chart" id="total-on-balance-sheet-exposure"></div>
      </b-card>
      <b-card class="bar-line-chart-card" title="Total Derivative Exposure">
        <div class="bar-line-chart" id="total-derivative-exposure"></div>
      </b-card>
    </b-card-group>
    <b-card-group deck>
      <b-card class="bar-line-chart-card" title="Total Repo Exposure">
        <div class="bar-line-chart" id="total-repo-exposure"></div>
      </b-card>
      <b-card class="bar-line-chart-card" title="Total Off-balance Sheet Exposure">
        <div class="bar-line-chart" id="total-offbalance-exposure"></div>
      </b-card>
    </b-card-group>
    <b-card-group deck>
      <b-card class="bar-line-chart-card" title="Total On Balance Sheet Exposure Decomposition">
        <div class="bar-line-chart" id="total-on-balance-sheet-exposure-decomp"></div>
      </b-card>
      <b-card class="bar-line-chart-card" title="Total Derivative Exposure Decomposition">
        <div class="bar-line-chart" id="total-derivative-exposure-decomp"></div>
      </b-card>
    </b-card-group>
    <b-card-group deck>
      <b-card class="bar-line-chart-card" title="Total Repo Exposure Decomposition">
        <div class="bar-line-chart" id="total-repo-exposure-decomp"></div>
      </b-card>
      <b-card class="bar-line-chart-card" title="Total Off-balance Sheet Exposure Decomposition">
        <div class="bar-line-chart" id="total-offbalance-exposure-decomp"></div>
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
      barChartData: {},
      barLineChartsData: {}
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
    DrawBarLineChart (id) {
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
          data: that.barLineChartsData.legendData,
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
        grid: {show: false},
        xAxis: [
          {
            type: 'category',
            axisTick: {show: false},
            data: that.barLineChartsData.xAxisData
          }
        ],
        yAxis: that.barLineChartsData.yAxisData,
        series: that.barLineChartsData.series
      }
      myChart.setOption(option, true)
    },
    getDataStack (id, quarter, selected) {
      let that = this
      that.chartData = {}
      let endpointDict = {
        'tier-one-capital-adjustments': 'getTierIDeductionsAdjustStack',
        'tier-one-capital-composition': 'getTierICompositionStack',
        'tier-two-capital-adjustments': 'getTierIIDeductionsAdjustStack',
        'tier-two-capital-composition': 'getTierIIBeforeDeductionStack',
        'total-consolidated-assets-adjustment': 'getOverallExposureAdjustStack',
        'total-capital-total-derivative-comparison': 'getTCDA',
        'total-on-balance-sheet-exposure-decomp': 'getTotalOnBalanceSheetExposureDecomp',
        'total-derivative-exposure-decomp': 'getDerivativeExposureDecomp',
        'total-repo-exposure-decomp': 'getRepoExposureDecomp',
        'total-offbalance-exposure-decomp': 'getOffBalanceSheetExposureDecomp'
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
                    if (id === 'total-on-balance-sheet-exposure-decomp' || id === 'total-derivative-exposure-decomp' || id === 'total-repo-exposure-decomp' || id === 'total-offbalance-exposure-decomp' || id === 'tier-one-capital-adjustments' || id === 'tier-one-capital-composition' || id === 'tier-two-capital-adjustments' || id === 'tier-two-capital-composition' || id === 'total-consolidated-assets-adjustment') {
                      chartItem.data.push(Math.round(item[1] / 1000))
                    } else if (id === 'total-capital-total-derivative-comparison') {
                      chartItem.data.push((item[1] * 100).toFixed(2))
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
            'total-offbalance-exposure-decomp': [
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
            'total-repo-exposure-decomp': [
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
            'total-derivative-exposure-decomp': [
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
            'total-on-balance-sheet-exposure-decomp': [
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
            'tier-one-capital-adjustments': [
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
            'tier-one-capital-composition': [
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
            'tier-two-capital-adjustments': [
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
            'tier-two-capital-composition': [
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
            'total-consolidated-assets-adjustment': [
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
            'total-capital-total-derivative-comparison': [
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
        'comparison-of-accounting-assets-and-total-exposure': 'getAssetExposureComparison',
        'tier-1-supplementary-comparison': 'getLeverageSup'
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
                    if (id === 'comparison-of-accounting-assets-and-total-exposure') {
                      chartItem.data.push(Math.round(item[1] / 1000))
                    } else {
                      chartItem.data.push((item[1]).toFixed(2))
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
            'comparison-of-accounting-assets-and-total-exposure': [
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
            ],
            'tier-1-supplementary-comparison': [
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
    getDataBarPlusLine (id, quarter, selected) {
      let that = this
      let endpointDict = {
        'total-on-balance-sheet-exposure': 'getTotalOnBalanceSheetExposure',
        'total-derivative-exposure': 'getDerivativeExposure',
        'total-repo-exposure': 'getRepoExposure',
        'total-offbalance-exposure': 'getOffBalanceExposure'
      }
      let legendBase = {
        'total-on-balance-sheet-exposure': ['exposure/asset ratio', 'on-balance sheet exposure', 'total exposure'],
        'total-derivative-exposure': ['derivative exposure/total exposure ratio', 'derivative exposure', 'total exposure'],
        'total-repo-exposure': ['repo exposure/total exposure ratio', 'repo exposure', 'total exposure'],
        'total-offbalance-exposure': ['off-balance exposure/total exposure ratio', 'off-balance exposure', 'total exposure']
      }
      myAPI
        .getDataByQuarter(endpointDict[id], quarter)
        .then(function (response) {
          let data = response.data
          let companies = []
          let groupOne = []
          let groupTwo = []
          let groupThree = []
          for (let key of selected) {
            if (data.hasOwnProperty(key)) {
              companies.push(key)
              groupOne.push((data[key][0][1] * 100).toFixed(2))
              groupTwo.push(Math.round(data[key][1][1] / 1000))
              groupThree.push(Math.round(data[key][2][1] / 1000))
            }
          }
          let series = []
          let legendList = []
          let chartItemOne = {}
          let chartItemTwo = {}
          let chartItemThree = {}
          let yAxisOne = {}
          let yAxisTwo = {}
          let yAxis = []

          chartItemOne.name = legendBase[id][0]
          chartItemOne.type = 'line'
          chartItemOne.data = groupOne
          chartItemOne.yAxisIndex = 1
          chartItemOne.label = {show: true}

          chartItemTwo.name = legendBase[id][1]
          chartItemTwo.type = 'bar'
          chartItemTwo.data = groupTwo
          chartItemTwo.label = {show: true}

          chartItemThree.name = legendBase[id][2]
          chartItemThree.type = 'bar'
          chartItemThree.data = groupThree
          chartItemThree.label = {show: true}

          yAxisOne.name = 'Millions'
          yAxisOne.scale = true
          yAxisOne.type = 'value'
          // yAxisOne.max = Math.max.apply(Math, groupOne) + 50000000;
          let curMax = Math.max.apply(Math, groupThree).toString()
          let highestDigit = parseInt(curMax[0])
          yAxisOne.max = 3500000
          yAxisOne.min = 0
          yAxisOne.splitLine = {
            show: false
          }
          yAxisOne.axisLabel = {
            formatter: function (value) {
              // Original Amount: Dollar Amounts in Thousands
              // show tick with comma
              return (value).toLocaleString()
            }
          }

          yAxisTwo.name = 'Percentage'
          yAxisTwo.scale = true
          yAxisTwo.type = 'value'
          // yAxisTwo.max = Math.round(Math.max.apply(Math,groupTwo) + 20);
          // yAxisTwo.min = Math.round(Math.min.apply(Math,groupTwo) - 20);
          curMax = Math.ceil(Math.max.apply(Math, groupOne))
          highestDigit = parseInt(curMax / 10)
          let curMin = Math.floor(Math.min.apply(Math, groupOne))
          let minValue = curMin - 2
          while (minValue > curMin) {
            minValue -= 2
          }
          yAxisTwo.max = (highestDigit + 1) * 10 + 20
          yAxisTwo.min = minValue - 20
          yAxisTwo.splitLine = {
            show: false
          }
          yAxisTwo.axisLabel = {
            formatter: '{value} %'
          }

          series = [chartItemOne, chartItemTwo, chartItemThree]
          legendList = legendBase[id]
          yAxis = [yAxisOne, yAxisTwo]
          console.log(companies)
          console.log(series)
          console.log(legendList)
          that.barLineChartsData.legendData = legendList
          that.barLineChartsData.xAxisData = companies
          that.barLineChartsData.yAxisData = yAxis
          that.barLineChartsData.series = series
          that.DrawBarLineChart(id)
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

.tierDisplay {
  font-family: "Georgia";
  text-align: center;
  margin-bottom: 20px;
  margin-top: 20px;
  font-size: 2em;
}

.stack-bar-chart-card {
  font-family: "Georgia";
}

.bar-line-chart-card {
  max-width: 100rem;
  max-height: 60rem;
  margin-bottom: 20px;
}

.bar-line-chart {
  width: 100%;
  height: 35rem;
  display: inline-block;
}

.bar-line-chart-card {
  font-family: "Georgia";
}

</style>
