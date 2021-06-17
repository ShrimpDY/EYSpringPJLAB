import Vue from 'vue'
import Router from 'vue-router'
import OverTimeAnalysis from '@/components/Connectors/OverTimeAnalysis'
import QuarterlyHighlight from '@/components/Connectors/QuarterlyHighlight'
import QuarterlyHighlightKey from '@/components/Connectors/QuarterlyHighlightKey'
import QuarterlyHighlightDetail from '@/components/Connectors/QuarterlyHighlightDetail'
import OverTimeAnalysisKey from '@/components/Connectors/OverTimeAnalysisKey'
import OverTimeAnalysisDetail from '@/components/Connectors/OverTimeAnalysisDetail'
import home from '@/components/Connectors/home'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/home',
      name: 'home',
      component: home,
      meta: {
        keepalive: true
      }
    },
    {
      path: '/OverTimeAnalysis',
      name: 'OverTimeAnalysis',
      component: OverTimeAnalysis,
      meta: {
        keepalive: true
      }
    },
    {
      path: '/QuarterlyHighlight',
      name: 'QuarterlyHighlight',
      component: QuarterlyHighlight,
      meta: {
        keepalive: true
      }
    },
    {
      path: '/QuarterlyHighlightKey',
      name: 'QuarterlyHighlightKey',
      component: QuarterlyHighlightKey,
      meta: {
        keepalive: true
      }
    },
    {
      path: '/QuarterlyHighlightDetail',
      name: 'QuarterlyHighlightDetail',
      component: QuarterlyHighlightDetail,
      meta: {
        keepalive: true
      }
    },
    {
      path: '/OverTimeAnalysisKey',
      name: 'OverTimeAnalysisKey',
      component: OverTimeAnalysisKey,
      meta: {
        keepalive: true
      }
    },
    {
      path: '/OverTimeAnalysisDetail',
      name: 'OverTimeAnalysisDetail',
      component: OverTimeAnalysisDetail,
      meta: {
        keepalive: true
      }
    }
  ]
})
