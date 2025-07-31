<template>
  <div class="report-container" ref="reportContent">
    <div class="charts-container">
      <div v-if="mode === 'user'" class="chart-row">
        <div class="chart-box">
          <canvas ref="lineCanvas"></canvas>
          <div v-if="!lineReady" class="loading-overlay">Loading line chart…</div>
        </div>
        <div class="chart-box">
          <canvas ref="pieCanvas"></canvas>
          <div v-if="!pieReady" class="loading-overlay">Loading pie chart…</div>
        </div>
      </div>
      <div v-else class="chart-row">
        <div class="chart-box">
          <canvas ref="barCanvas"></canvas>
          <div v-if="!barReady" class="loading-overlay">Loading bar chart…</div>
        </div>
        <div class="chart-box">
          <canvas ref="doughnutCanvas"></canvas>
          <div v-if="!doughnutReady" class="loading-overlay">Loading doughnut chart…</div>
        </div>
      </div>
    </div>
    <div v-if="summaryTable.length" class="summary-table-container">
      <h4>Summary Table</h4>
      <table class="summary-table">
        <thead>
          <tr>
            <th v-for="col in summaryColumns" :key="col">{{ col }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in summaryTable" :key="row.name">
            <td v-for="col in summaryColumns" :key="col">{{ row[col.toLowerCase()] }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <button @click="downloadPdf" class="btn btn-primary mt-3">Download PDF</button>
  </div>
</template>

<script>
import { ref, onMounted, nextTick } from 'vue'
import { Chart, registerables } from 'chart.js'
import { api } from '@/api/api'
import jsPDF from 'jspdf'
import html2canvas from 'html2canvas'

Chart.register(...registerables)

export default {
  name: 'MonthlyReport',
  props: {
    mode: { type: String, default: 'user' }
  },
  setup(props) {
    const lineCanvas = ref(null)
    const pieCanvas = ref(null)
    const lineReady = ref(false)
    const pieReady = ref(false)
    let lineChart = null
    let pieChart = null

    const barCanvas = ref(null)
    const doughnutCanvas = ref(null)
    const barReady = ref(false)
    const doughnutReady = ref(false)
    let barChart = null
    let doughnutChart = null

    const summaryTable = ref([])
    const summaryColumns = ref([])

    onMounted(async () => {
      if (props.mode === 'user') {
        const res = await api.getMonthlySummary()
        if (!res) return
        const { months, bookings, spent, lots } = res
        summaryTable.value = lots
        summaryColumns.value = ['Name', 'Count']
        await nextTick()
        setTimeout(() => {
          if (lineCanvas.value) {
            if (lineChart) lineChart.destroy()
            lineChart = new Chart(lineCanvas.value.getContext('2d'), {
              type: 'line',
              data: {
                labels: months,
                datasets: [
                  {
                    label: 'Bookings',
                    data: bookings,
                    borderColor: '#007bff',
                    backgroundColor: 'rgba(0, 123, 255, 0.1)',
                    fill: true,
                    tension: 0.3
                  },
                  {
                    label: 'Amount Spent',
                    data: spent,
                    borderColor: '#28a745',
                    backgroundColor: 'rgba(40, 167, 69, 0.1)',
                    fill: true,
                    tension: 0.3
                  }
                ]
              },
              options: {
                responsive: true,
                plugins: { legend: { position: 'top' } },
                scales: { y: { beginAtZero: true } }
              }
            })
            lineReady.value = true
          }

          if (pieCanvas.value) {
            if (pieChart) pieChart.destroy()
            pieChart = new Chart(pieCanvas.value.getContext('2d'), {
              type: 'pie',
              data: {
                labels: lots.map(l => l.name),
                datasets: [{
                  label: 'Most Used Lots',
                  data: lots.map(l => l.count),
                  backgroundColor: [
                    '#007bff', '#28a745', '#ffc107', '#dc3545', '#6f42c1'
                  ]
                }]
              },
              options: {
                responsive: true,
                plugins: { legend: { position: 'top' } }
              }
            })
            pieReady.value = true
          }
        }, 100)
      } else {
        const res = await api.getAdminSummary()
        if (!res) return
        const { lots, available, occupied } = res
        summaryTable.value = lots.map(lot => ({
          name: lot.name,
          revenue: lot.revenue
        }))
        summaryColumns.value = ['Name', 'Revenue']
        await nextTick()
        setTimeout(() => {
          if (barCanvas.value) {
            if (barChart) barChart.destroy()
            barChart = new Chart(barCanvas.value.getContext('2d'), {
              type: 'bar',
              data: {
                labels: lots.map(l => l.name),
                datasets: [{
                  label: 'Revenue',
                  data: lots.map(l => l.revenue),
                  backgroundColor: '#007bff'
                }]
              },
              options: {
                responsive: true,
                plugins: { legend: { position: 'top' } },
                scales: { y: { beginAtZero: true } }
              }
            })
            barReady.value = true
          }
          if (doughnutCanvas.value) {
            if (doughnutChart) doughnutChart.destroy()
            doughnutChart = new Chart(doughnutCanvas.value.getContext('2d'), {
              type: 'doughnut',
              data: {
                labels: ['Available', 'Occupied'],
                datasets: [{
                  label: 'Lot Status',
                  data: [available, occupied],
                  backgroundColor: ['#28a745', '#dc3545']
                }]
              },
              options: {
                responsive: true,
                plugins: { legend: { position: 'top' } }
              }
            })
            doughnutReady.value = true
          }
        }, 100)
      }
    })

    const downloadPdf = async () => {
      const el = document.querySelector('.report-container')
      const canvas = await html2canvas(el, { scale: 2 })
      const imgData = canvas.toDataURL('image/png')
      const pdf = new jsPDF('p', 'mm', 'a4')
      const width = pdf.internal.pageSize.getWidth()
      const height = (canvas.height * width) / canvas.width
      pdf.addImage(imgData, 'PNG', 0, 0, width, height)
      pdf.save('monthly_report.pdf')
    }

    return {
      // User
      lineCanvas, pieCanvas, lineReady, pieReady,
      // Admin
      barCanvas, doughnutCanvas, barReady, doughnutReady,
      downloadPdf,
      summaryTable,
      summaryColumns
    }
  }
}
</script>

<style scoped>
.report-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
}

.report-title {
  text-align: center;
  margin-bottom: 2rem;
  font-weight: 600;
}

.charts-container {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  justify-content: center;
}

.chart-row {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  width: 100%;
}

.chart-box {
  flex: 1 1 350px;
  min-width: 300px;
  max-width: 600px;
  background: #fafbfc;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.03);
  position: relative;
}

canvas {
  width: 100% !important;
  height: 300px !important;
  background: #fff;
  border-radius: 8px;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  background-color: rgba(255, 255, 255, 0.85);
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bold;
  z-index: 1;
}

.summary-table-container {
  margin-top: 2rem;
  overflow-x: auto;
}

.summary-table {
  width: 100%;
  border-collapse: collapse;
  margin: 0 auto;
  background: #f8f9fa;
  border-radius: 8px;
  overflow: hidden;
}

.summary-table th,
.summary-table td {
  padding: 0.75rem 1rem;
  border: 1px solid #e9ecef;
  text-align: left;
}

.summary-table th {
  background: #e9ecef;
  font-weight: 600;
}

@media (max-width: 900px) {

  .charts-container,
  .chart-row {
    flex-direction: column;
    gap: 1.5rem;
  }

  .chart-box {
    max-width: 100%;
  }
}
</style>