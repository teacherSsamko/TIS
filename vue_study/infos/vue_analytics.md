# vue-analytics

## 설치
```
npm install vue-analytics
```

## load
```javascript
import Vue from 'vue'
import VueAnalytics from 'vue-analytics'

Vue.use(VueAnalytics, {
  id: 'UA-XXX-X',
  checkDuplicatedScript: true
})
```

## Event Tracking
```javascript
this.$ga.event('category', 'action', 'label')