let latencyChart, throughputChart, bandwidthChart;

async function fetchData() {
  const response = await fetch('/data');
  return await response.json();
}

function createChart(ctx, label, borderColor) {
  return new Chart(ctx, {
    type: 'line',
    data: {
      labels: [],
      datasets: [{
        label: label,
        data: [],
        borderColor: borderColor,
        fill: false
      }]
    },
    options: {
      scales: {
        x: { title: { display: true, text: "Time" } },
        y: { title: { display: true, text: label + " (ms or Mbps)" } }
      }
    }
  });
}

async function updateCharts() {
  const data = await fetchData();
  const timestamps = data.map(d => d.timestamp);

  latencyChart.data.labels = timestamps;
  latencyChart.data.datasets[0].data = data.map(d => d.latency);
  latencyChart.update();

  throughputChart.data.labels = timestamps;
  throughputChart.data.datasets[0].data = data.map(d => d.throughput);
  throughputChart.update();

  bandwidthChart.data.labels = timestamps;
  bandwidthChart.data.datasets[0].data = data.map(d => d.bandwidth);
  bandwidthChart.update();
}

window.onload = async () => {
  latencyChart = createChart(document.getElementById("latencyChart"), "Latency", "red");
  throughputChart = createChart(document.getElementById("throughputChart"), "Throughput", "blue");
  bandwidthChart = createChart(document.getElementById("bandwidthChart"), "Bandwidth", "green");

  await updateCharts();
  setInterval(updateCharts, 60000);
};
