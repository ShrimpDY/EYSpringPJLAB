<template>
  <div>
    <div class="OA_header_layout">
      <h3 class="OA_header">
        <span class="OA_header_span">Overtime Detail Analysis</span>
      </h3>
    </div>
    <b-form id="main-input" inline>
      <b-form-group inline id="input-group-1" label="Start Quarter: " label-for="input-quarter-1">
        <b-form-input id="input-quarter-1" name="input-quarter" v-model.trim="quarter1"
                      placeholder="example: 2016Q3" required>
        </b-form-input>
      </b-form-group>
      <b-form-group inline id="input-group-2" label="End Quarter: " label-for="input-quarter-2">
        <b-form-input id="input-quarter-2" name="input-quarter" v-model.trim="quarter2"
                      placeholder="example: 2020Q3" required>
        </b-form-input>
      </b-form-group>
      <b-form-group inline id="select-group" label="Select Company:">
      </b-form-group>
      <b-form-checkbox-group
          id="checkbox-group-1"
          v-model="selected"
          :options="options"
          name="Company-Select"
      ></b-form-checkbox-group>
      <b-button @click="getData()" variant="primary" :disabled="!validationDate || !validationSelection">Search</b-button>
    </b-form>
    <b-form id="error-catcher">
      <b-form-group id="error-catcher-box" label="You may have following errors:">
        <b-form-invalid-feedback :state="validationQ1">
          Your start quarter input should be at the form format like 2016Q4
        </b-form-invalid-feedback>
        <b-form-valid-feedback :state="validationQ1">
          Your start quarter input format looks good.
        </b-form-valid-feedback>
        <b-form-invalid-feedback :state="validationQ2">
          Your end quarter input should be at the form format like 2020Q4
        </b-form-invalid-feedback>
        <b-form-valid-feedback :state="validationQ2">
          Your end quarter input format looks good.
        </b-form-valid-feedback>
        <b-form-invalid-feedback :state="validationSelection">
          You need to select at least one company
        </b-form-invalid-feedback>
        <b-form-valid-feedback :state="validationSelection">
          Your selection of companies looks good.
        </b-form-valid-feedback>
        <b-form-invalid-feedback :state="validationDate">
          Your end quarter should be later than the start quarter
        </b-form-invalid-feedback>
        <b-form-valid-feedback :state="validationDate">
          Your quarter sequence input looks good.
        </b-form-valid-feedback>
      </b-form-group>
    </b-form>
    <detail-overtime-analysis ref="DetailOvertimeAnalysis"></detail-overtime-analysis>
  </div>
</template>

<script>
import DetailOvertimeAnalysis from '@/components/Cards/DetailOvertimeAnalysis'
// import OverTimeBarChart from '@/components/Cards/OverTimeBarChart'
// import OverTimeTable from '@/components/Cards/OverTimeTable'
import DataSetting from '../../../../../backend/data_setting.json'
import helper from '../../helper'

export default {
  created () {
    let keyList = []
    let optionCatcher = DataSetting['institutions']
    for (let institution in optionCatcher) {
      if (optionCatcher.hasOwnProperty(institution)) {
        keyList.push(institution)
      }
    }
    let options = []
    for (let key in keyList) {
      if (keyList.hasOwnProperty(key)) {
        let option = {}
        option.text = optionCatcher[keyList[key]]['Nick']
        option.value = optionCatcher[keyList[key]]['Nick']
        options.push(option)
        this.selected.push(option.value)
      }
    }
    this.options = options
  },
  computed: {
    validationQ1 () {
      return /^[0-9]{4}[Qq][1-4]$/.test(this.quarter1)
    },
    validationQ2 () {
      return /^[0-9]{4}[Qq][1-4]$/.test(this.quarter2)
    },
    validationDate () {
      return /^[0-9]{4}[Qq][1-4]$/.test(this.quarter1) && /^[0-9]{4}[Qq][1-4]$/.test(this.quarter2) && this.quarter1 < this.quarter2
    },
    validationSelection () {
      console.log('1111111', this.selected.length)
      return this.selected.length !== 0
    }
  },
  name: 'overtime-charts',
  components: {DetailOvertimeAnalysis},
  data: function () {
    return {
      selected: [],
      options: [],
      quarter1: helper.getDefaultStartQuarter(),
      quarter2: helper.getLatestQuarter()
    }
  },
  methods: {
    getData () {
      console.log(this.selected)
      this.$refs.DetailOvertimeAnalysis.getDataLine('t1-retained-earnings', this.quarter1, this.quarter2, this.selected)
      this.$refs.DetailOvertimeAnalysis.getDataLine('t1-goodwill', this.quarter1, this.quarter2, this.selected)
      this.$refs.DetailOvertimeAnalysis.getDataLine('total-capital-minority-interest-not-included-in-tier-1-overtime', this.quarter1, this.quarter2, this.selected)
      this.$refs.DetailOvertimeAnalysis.getDataLine('cet-1-ratio-overtime', this.quarter1, this.quarter2, this.selected)
      this.$refs.DetailOvertimeAnalysis.getDataLine('tier-1-ratio-overtime', this.quarter1, this.quarter2, this.selected)
      this.$refs.DetailOvertimeAnalysis.getDataLine('cet-vs-tier-1-ratio-overtime', this.quarter1, this.quarter2, this.selected)
      this.$refs.DetailOvertimeAnalysis.getDataLine('on-balance-sheet-exposure-overtime', this.quarter1, this.quarter2, this.selected)
      this.$refs.DetailOvertimeAnalysis.getDataLine('derivative-exposure-overtime', this.quarter1, this.quarter2, this.selected)
      this.$refs.DetailOvertimeAnalysis.getDataLine('repo-exposure-overtime', this.quarter1, this.quarter2, this.selected)
      this.$refs.DetailOvertimeAnalysis.getDataLine('off-balance-exposure-overtime', this.quarter1, this.quarter2, this.selected)
      this.$refs.DetailOvertimeAnalysis.getDataLine('on-balance-sheet-exposure-ratio-overtime', this.quarter1, this.quarter2, this.selected)
      this.$refs.DetailOvertimeAnalysis.getDataLine('derivative-exposure-ratio-overtime', this.quarter1, this.quarter2, this.selected)
      this.$refs.DetailOvertimeAnalysis.getDataLine('repo-exposure-ratio-overtime', this.quarter1, this.quarter2, this.selected)
      this.$refs.DetailOvertimeAnalysis.getDataLine('off-balance-exposure-ratio-overtime', this.quarter1, this.quarter2, this.selected)
      this.$refs.DetailOvertimeAnalysis.getDataLine('ratio-of-tier-2-capital-and-total-capital-overtime', this.quarter1, this.quarter2, this.selected)
      this.$refs.DetailOvertimeAnalysis.getDataLine('ratio-of-total-capital-and-on-balance-sheet-items-overtime', this.quarter1, this.quarter2, this.selected)
      this.$refs.DetailOvertimeAnalysis.getDataLine('ratio-of-total-capital-and-derivative-assets', this.quarter1, this.quarter2, this.selected)
      this.$refs.DetailOvertimeAnalysis.getDataLine('ratio-of-total-capital-and-repo-assets', this.quarter1, this.quarter2, this.selected)
      this.$refs.DetailOvertimeAnalysis.getDataLine('ratio-of-total-capital-and-off-balance-sheet-items', this.quarter1, this.quarter2, this.selected)
      this.$refs.DetailOvertimeAnalysis.getDataLine('ratio-of-rwa-and-total-assets', this.quarter1, this.quarter2, this.selected)
      this.$refs.DetailOvertimeAnalysis.getDataLine('tier-two-deduction', this.quarter1, this.quarter2, this.selected)
      this.$refs.DetailOvertimeAnalysis.getDataLine('tier-2-ratio-overtime', this.quarter1, this.quarter2, this.selected)
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
  margin-bottom: 10px;
}
.OA_header_layout{
  border-bottom: 1px solid;
  border-bottom-color: #CACACA;
  margin-bottom: 15px;
  margin-top: 5px;
  box-sizing: border-box;
}
</style>
