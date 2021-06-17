<template>
  <div>
    <div class="OA_header_layout">
      <h3 class="OA_header">
        <span class="OA_header_span">Quarterly Highlights</span>
      </h3>
    </div>
    <div class="logic-flow-button-layout">
      <b-button class="logic-flow-button" @click="getLogicFlow ('logic-flow')" variant="primary">Get Logic Flow</b-button>
    </div>
    <b-card class="logic-chart-card" title="Logic Flow">
        <div class="logic-chart" id="logic-flow"></div>
    </b-card>
  </div>
</template>

<script>
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
    drawLogicFlow (id) {
      let chartDom = document.getElementById(id)
      let myChart = echarts.getInstanceByDom(chartDom)
      if (myChart == null) {
        myChart = echarts.init(chartDom)
      }
      let option = {
        series: [
          {
            type: 'sankey',
            left: 50.0,
            top: 20.0,
            right: 150.0,
            bottom: 25.0,
            data: [
              {
                'name': 'Companes',
                'itemStyle': {
                  'color': '#FCC32E',
                  'borderColor': '#FCC32E'
                }
              },
              {
                'name': 'Total Capital Breakdown',
                'itemStyle': {
                  'color': '#3891A7',
                  'borderColor': '#3891A7'
                }
              },
              {
                'name': 'Total RWA Assets',
                'itemStyle': {
                  'color': '#0037DA',
                  'borderColor': '#0037DA'
                }
              },
              {
                'name': 'Key Ratios',
                'itemStyle': {
                  'color': '#C0BEAF',
                  'borderColor': '#C0BEAF'
                }
              },
              {
                'name': 'Key Buffers',
                'itemStyle': {
                  'color': '#EA005E',
                  'borderColor': '#EA005E'
                }
              },
              {
                'name': 'Key Exposures',
                'itemStyle': {
                  'color': '#D13438',
                  'borderColor': '#D13438'
                }
              },
              {
                'name': 'Tier I Capital Adjustments',
                'itemStyle': {
                  'color': '#D13438',
                  'borderColor': '#D13438'
                }
              },
              {
                'name': 'Tier I Capital Composition',
                'itemStyle': {
                  'color': '#9ed566',
                  'borderColor': '#9ed566'
                }
              },
              {
                'name': 'Tier II Capital Adjustments',
                'itemStyle': {
                  'color': '#2BCC7F',
                  'borderColor': '#2BCC7F'
                }
              },
              {
                'name': 'Tier II Capital Composition',
                'itemStyle': {
                  'color': '#809B48',
                  'borderColor': '#809B48'
                }
              },
              {
                'name': 'Total Consolidated Assets Adjustment',
                'itemStyle': {
                  'color': '#9B2D1F',
                  'borderColor': '#9B2D1F'
                }
              },
              {
                'name': 'Comparison Of Accounting Assets and Total Exposure',
                'itemStyle': {
                  'color': '#604878',
                  'borderColor': '#604878'
                }
              },
              {
                'name': 'Total Capital Change vs. Total Derivative Exposure Change',
                'itemStyle': {
                  'color': '#A5644E',
                  'borderColor': '#A5644E'
                }
              },
              {
                'name': 'Tier I Leverage Ratio vs. Supplementary Leverage Ratio',
                'itemStyle': {
                  'color': '#2D3F3A',
                  'borderColor': '#2D3F3A'
                }
              },
              {
                'name': 'Total On Balance Sheet Exposure',
                'itemStyle': {
                  'color': '#761721',
                  'borderColor': '#761721'
                }
              },
              {
                'name': 'Total Derivative Exposure',
                'itemStyle': {
                  'color': '#B1BADD',
                  'borderColor': '#B1BADD'
                }
              },
              {
                'name': 'Total Repo Exposure',
                'itemStyle': {
                  'color': '#B0CCB0',
                  'borderColor': '#B0CCB0'
                }
              }
            ],
            links: [
              {
                'source': 'Companes',
                'target': 'Total Capital Breakdown',
                'value': 1
              },
              {
                'source': 'Companes',
                'target': 'Total RWA Assets',
                'value': 1
              },
              {
                'source': 'Companes',
                'target': 'Key Ratios',
                'value': 1
              },
              {
                'source': 'Companes',
                'target': 'Key Buffers',
                'value': 1
              },
              {
                'source': 'Companes',
                'target': 'Key Exposures',
                'value': 1
              },
              {
                'source': 'Total Capital Breakdown',
                'target': 'Tier I Capital Adjustments',
                'value': 1
              },
              {
                'source': 'Total Capital Breakdown',
                'target': 'Tier I Capital Composition',
                'value': 1
              },
              {
                'source': 'Total Capital Breakdown',
                'target': 'Tier II Capital Adjustments',
                'value': 1
              },
              {
                'source': 'Total Capital Breakdown',
                'target': 'Tier II Capital Composition',
                'value': 1
              },
              {
                'source': 'Key Ratios',
                'target': 'Tier I Leverage Ratio vs. Supplementary Leverage Ratio',
                'value': 1
              },
              {
                'source': 'Key Ratios',
                'target': 'Total On Balance Sheet Exposure',
                'value': 1
              },
              {
                'source': 'Key Ratios',
                'target': 'Total Derivative Exposure',
                'value': 1
              },
              {
                'source': 'Key Ratios',
                'target': 'Total Repo Exposure',
                'value': 1
              },
              {
                'source': 'Total RWA Assets',
                'target': 'Comparison Of Accounting Assets and Total Exposure',
                'value': 1
              },
              {
                'source': 'Total RWA Assets',
                'target': 'Total Capital Change vs. Total Derivative Exposure Change',
                'value': 1
              },
              {
                'source': 'Key Exposures',
                'target': 'Total Consolidated Assets Adjustment',
                'value': 1
              },
              {
                'source': 'Key Exposures',
                'target': 'Comparison Of Accounting Assets and Total Exposure',
                'value': 1
              },
              {
                'source': 'Key Exposures',
                'target': 'Total Capital Change vs. Total Derivative Exposure Change',
                'value': 1
              },
              {
                'source': 'Key Exposures',
                'target': 'Tier I Leverage Ratio vs. Supplementary Leverage Ratio',
                'value': 1
              },
              {
                'source': 'Key Exposures',
                'target': 'Total On Balance Sheet Exposure',
                'value': 1
              },
              {
                'source': 'Key Exposures',
                'target': 'Total Derivative Exposure',
                'value': 1
              },
              {
                'source': 'Key Exposures',
                'target': 'Total Repo Exposure',
                'value': 1
              }
            ],
            lineStyle: {
              color: 'source',
              curveness: 0.5
            },
            itemStyle: {
              color: '#1f77b4',
              borderColor: '#1f77b4'
            },
            label: {
              color: 'rgba(0,0,0,0.7)',
              fontFamily: 'Arial',
              fontSize: 10
            }
          }
        ],
        tooltip: {
          trigger: 'item'
        }
      }
      myChart.setOption(option, true)
    },
    getLogicFlow (id) {
      let that = this
      that.drawLogicFlow(id)
    },
    getData () {
      console.log(this.selected)
      this.$refs.getLogicFlow('logic-flow')
      // this.$refs.overTimeBarChart.getData('number-of-VaR-breach', this.quarter1, this.quarter2, this.selected)
      // this.$refs.overTimeTable.getData('stress-window-table', this.quarter1, this.quarter2, this.selected)
    }
  }
}
</script>

<style scoped>
#input-group-1 {
  margin: 5px;
}
#input-quarter-1{
  margin: 10px;
  width: 200px;
}
#input-group-2 {
  margin: 5px;
}
#input-quarter-2{
  margin: 10px;
  width: 200px;
}
#select-group {
  margin: 5px;
}
#checkbox-group-1{
  margin: 10px;
}

#error-catcher {
  margin: 5px;
}
.OA_header_span{
  font-family: 'Georgia', sans-serif;
  color: #323030;
  font-weight: bold;
}
.OA_header{
  text-align: center;
  font-size: 3em;
  margin-bottom: 10px;
}
.OA_header_layout{
  margin-bottom: 15px;
  margin-top: 50px;
  box-sizing: border-box;
}

.logic-flow-button-layout{
  text-align: center;
  alignment: center;
  margin-bottom: 20px;
}

.logic-chart-card {
  max-width: 150rem;
  max-height: 60rem;
  margin-bottom: 20px;
}

.logic-chart-card {
  font-family: "Georgia";
}

.logic-chart {
  width: 100%;
  height: 50rem;
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
