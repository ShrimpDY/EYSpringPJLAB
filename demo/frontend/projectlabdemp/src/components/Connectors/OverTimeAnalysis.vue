<template>
  <div>
    <div class="OA_header_layout">
      <h3 class="OA_header">
        <span class="OA_header_span">Overtime Analysis</span>
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
                'name': 'Tier 1 Capital',
                'itemStyle': {
                  'color': '#3891A7',
                  'borderColor': '#3891A7'
                }
              },
              {
                'name': 'Tier 2 Capital',
                'itemStyle': {
                  'color': '#0037DA',
                  'borderColor': '#0037DA'
                }
              },
              {
                'name': 'Exposure Ratios',
                'itemStyle': {
                  'color': '#EA005E',
                  'borderColor': '#EA005E'
                }
              },
              {
                'name': 'Total Capital Ratios',
                'itemStyle': {
                  'color': '#C0BEAF',
                  'borderColor': '#C0BEAF'
                }
              },
              {
                'name': 'Retained Earning',
                'itemStyle': {
                  'color': '#D13438',
                  'borderColor': '#D13438'
                }
              },
              {
                'name': 'Goodwill',
                'itemStyle': {
                  'color': '#9ed566',
                  'borderColor': '#9ed566'
                }
              },
              {
                'name': 'Tier 2 Ratio',
                'itemStyle': {
                  'color': '#ac7430',
                  'borderColor': '#ac7430'
                }
              },
              {
                'name': 'Minority Interest',
                'itemStyle': {
                  'color': '#2BCC7F',
                  'borderColor': '#2BCC7F'
                }
              },
              {
                'name': 'Tier 2 Deduction Ratio',
                'itemStyle': {
                  'color': '#809B48',
                  'borderColor': '#809B48'
                }
              },
              {
                'name': 'CET1 Ratio',
                'itemStyle': {
                  'color': '#9B2D1F',
                  'borderColor': '#9B2D1F'
                }
              },
              {
                'name': 'Tier 1 Ratio',
                'itemStyle': {
                  'color': '#604878',
                  'borderColor': '#604878'
                }
              },
              {
                'name': 'CET vs Tier 1 Ratio',
                'itemStyle': {
                  'color': '#A5644E',
                  'borderColor': '#A5644E'
                }
              },
              {
                'name': 'Tier 2 Capital / Total Capital Ratio',
                'itemStyle': {
                  'color': '#B0CCB0',
                  'borderColor': '#B0CCB0'
                }
              },
              {
                'name': 'On Balance Sheet Items / Total Capital Ratio',
                'itemStyle': {
                  'color': '#8164A3',
                  'borderColor': '#8164A3'
                }
              },
              {
                'name': 'Derivative Assets Ratio / Total Capital Ratio',
                'itemStyle': {
                  'color': '#8E562E',
                  'borderColor': '#8E562E'
                }
              },
              {
                'name': 'Repo Assets / Total Capital Ratio',
                'itemStyle': {
                  'color': '#C1504D',
                  'borderColor': '#C1504D'
                }
              },
              {
                'name': 'Off Balance Sheet Items / Total Capital Ratio',
                'itemStyle': {
                  'color': '#CCAF0A',
                  'borderColor': '#CCAF0A'
                }
              },
              {
                'name': 'RWA / Total Assets Ratio',
                'itemStyle': {
                  'color': '#956251',
                  'borderColor': '#956251'
                }
              },
              {
                'name': 'On Balance Sheet Exposure Ratio',
                'itemStyle': {
                  'color': '#2D3F3A',
                  'borderColor': '#2D3F3A'
                }
              },
              {
                'name': 'Derivative Exposure Ratio',
                'itemStyle': {
                  'color': '#761721',
                  'borderColor': '#761721'
                }
              },
              {
                'name': 'Repo Exposure Ratio',
                'itemStyle': {
                  'color': '#B1BADD',
                  'borderColor': '#B1BADD'
                }
              }
            ],
            links: [
              {
                'source': 'Companes',
                'target': 'Tier 1 Capital',
                'value': 1
              },
              {
                'source': 'Companes',
                'target': 'Tier 2 Capital',
                'value': 1
              },
              {
                'source': 'Companes',
                'target': 'Capital Ratios',
                'value': 1
              },
              {
                'source': 'Companes',
                'target': 'Exposure Ratios',
                'value': 1
              },
              {
                'source': 'Companes',
                'target': 'Total Capital Ratios',
                'value': 1
              },
              {
                'source': 'Tier 1 Capital',
                'target': 'Retained Earning',
                'value': 1
              },
              {
                'source': 'Tier 1 Capital',
                'target': 'Goodwill',
                'value': 1
              },
              {
                'source': 'Tier 1 Capital',
                'target': 'CET1 Ratio',
                'value': 1
              },
              {
                'source': 'Tier 1 Capital',
                'target': 'Tier 1 Ratio',
                'value': 1
              },
              {
                'source': 'Tier 2 Capital',
                'target': 'Tier 2 Ratio',
                'value': 1
              },
              {
                'source': 'Tier 2 Capital',
                'target': 'Minority Interest',
                'value': 1
              },
              {
                'source': 'Tier 2 Capital',
                'target': 'Tier 2 Deduction Ratio',
                'value': 1
              },
              {
                'source': 'Tier 1 Capital',
                'target': 'CET1 Ratio',
                'value': 1
              },
              {
                'source': 'Tier 1 Capital',
                'target': 'Tier 1 Ratio',
                'value': 1
              },
              {
                'source': 'Tier 1 Capital',
                'target': 'CET vs Tier 1 Ratio',
                'value': 1
              },
              {
                'source': 'Exposure Ratios',
                'target': 'On Balance Sheet Exposure Ratio',
                'value': 1
              },
              {
                'source': 'Exposure Ratios',
                'target': 'Derivative Exposure Ratio',
                'value': 1
              },
              {
                'source': 'Exposure Ratios',
                'target': 'Repo Exposure Ratio',
                'value': 1
              },
              {
                'source': 'Total Capital Ratios',
                'target': 'Tier 2 Capital / Total Capital Ratio',
                'value': 1
              },
              {
                'source': 'Total Capital Ratios',
                'target': 'On Balance Sheet Items / Total Capital Ratio',
                'value': 1
              },
              {
                'source': 'Total Capital Ratios',
                'target': 'Derivative Assets Ratio / Total Capital Ratio',
                'value': 1
              },
              {
                'source': 'Total Capital Ratios',
                'target': 'Repo Assets / Total Capital Ratio',
                'value': 1
              },
              {
                'source': 'Total Capital Ratios',
                'target': 'Off Balance Sheet Items / Total Capital Ratio',
                'value': 1
              },
              {
                'source': 'Total Capital Ratios',
                'target': 'RWA / Total Assets Ratio',
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
