
// Set Chart.js global dark theme
Chart.defaults.font.color = '#e5e7eb'
Chart.defaults.color = '#e5e7eb'
Chart.defaults.borderColor = '#374151'
Chart.defaults.backgroundColor = '#1f2937'
Chart.defaults.plugins.legend.labels.color = '#d1d5db'
Chart.defaults.scales = {
  x: { grid: { color: '#374151' }, ticks: { color: '#e5e7eb' } },
  y: { grid: { color: '#374151' }, ticks: { color: '#e5e7eb' } }
}

console.log(window.djangoData)
const classes = window.djangoData.classes
const countByClass = window.djangoData.countByClass

const top10 = window.djangoData.top10
const topNames = top10.map(r => r.Name.split(',')[0])
const topFares = top10.map(r => r.Fare)

const survivedByClass = window.djangoData.survivedByClass
const diedByClass = window.djangoData.diedByClass

const ports = window.djangoData.ports
const embarkedData = window.djangoData.embarkedData

// Charts
new Chart('chart-class-donut', {
  type: 'doughnut',
  data: {
    labels: ['1st', '2nd', '3rd'],
    datasets: [
      {
        data: countByClass,
        backgroundColor: ['#67817D', '#C5C9B5', '#85B0A2 ']
      }
    ]
  },
  options: { responsive: true, maintainAspectRatio: false }
})

new Chart('chart-top-fare', {
  type: 'bar',
  data: {
    labels: topNames,
    datasets: [{ data: topFares, backgroundColor: '#67817D' }]
  },
  options: {
    indexAxis: 'y',
    responsive: true,
    plugins: {
      legend: {
        display: false // Show the legend
      }
    },
    scales: {
      x: {
        grid: { color: '#374151' },
        ticks: { color: '#e5e7eb' }
      },
      y: { 
        grid: { color: '#374151' },
        ticks: { 
          color: '#e5e7eb',
          callback: value => topNames[value]
        }
      }
    }
  }
})

new Chart('chart-survived-class', {
  type: 'bar',
  data: {
    labels: ['1st', '2nd', '3rd'],
    datasets: [
      { label: 'Died', data: diedByClass, backgroundColor: '#85B0A2' },
      {
        label: 'Survived',
        data: survivedByClass,
        backgroundColor: '#C5C9B5'
      }
    ]
  },
  options: { responsive: true, 
    scales: {
      x: {
        grid: Chart.defaults.scales.x.grid,
        ticks: {
          callback: value => classes[value],
        }
      },
      y: {
        grid: Chart.defaults.scales.y.grid,
        ticks: Chart.defaults.scales.y.ticks
      }
    } }
})

new Chart('chart-embarked-class', {
  type: 'bar',
  data: {
    labels: ['Southampton', 'Queenstown', 'Cherbourg'],
    datasets: classes.map((c, i) => ({
      label: `${c}st Class`,
      data: ports.map((_, p) => embarkedData[p][i]),
      backgroundColor: ['#67817D', '#C5C9B5', '#85B0A2'][i]
    }))
  },
  options: {
    responsive: true,
    scales: {
      x: {
        stacked: true,
        grid: { color: '#374151' },
        ticks: { 
          color: '#e5e7eb', 
          display: true, 
          font: { size: 14 },
          callback: p => ['Southampton', 'Queenstown', 'Cherbourg'][p]
        }
      },
      y: {
        stacked: true,
        grid: Chart.defaults.scales.y.grid,
        ticks: Chart.defaults.scales.y.ticks
      }
    }
  }
})