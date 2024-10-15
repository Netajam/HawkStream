document.addEventListener('DOMContentLoaded', function() {
    let affluenceChart, instantaneousChart;

    const objectTypeDropdown = document.getElementById('object-type');
    const timeRangeDropdown = document.getElementById('time-range');

    // Function to fetch and update the charts
    function fetchAndUpdateCharts() {
        // Get the current values from the dropdowns
        const objectType = objectTypeDropdown.value;
        const timeRange = timeRangeDropdown.value;

        // Fetch cumulative affluence data
        fetch(`/api/cumulative_affluence_data?object_type=${objectType}&time_range=${timeRange}`)
            .then(response => response.json())
            .then(data => {
                if (affluenceChart) {
                    affluenceChart.data.labels = data.timestamps;
                    affluenceChart.data.datasets[0].data = data.affluence;
                    affluenceChart.update(); // Update the chart with new data
                } else {
                    const ctx = document.getElementById('affluenceChart').getContext('2d');
                    affluenceChart = new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: data.timestamps,
                            datasets: [{
                                label: 'Cumulative Affluence',
                                data: data.affluence,
                                borderColor: 'rgba(75, 192, 192, 1)',
                                borderWidth: 2,
                                fill: false
                            }]
                        },
                        options: {
                            scales: {
                                x: {
                                    type: 'time',
                                    time: {
                                        unit: 'minute',
                                        displayFormats: {
                                            minute: 'HH:mm'
                                        }
                                    }
                                }
                            }
                        }
                    });
                }
            }).catch(error => console.error('Error fetching cumulative data:', error));

        // Fetch instantaneous affluence data
        fetch(`/api/instantaneous_affluence_data?object_type=${objectType}&time_range=${timeRange}`)
            .then(response => response.json())
            .then(data => {
                if (instantaneousChart) {
                    instantaneousChart.data.labels = data.timestamps;
                    instantaneousChart.data.datasets[0].data = data.counts;
                    instantaneousChart.update(); // Update the chart with new data
                } else {
                    const ctx = document.getElementById('instantaneousChart').getContext('2d');
                    instantaneousChart = new Chart(ctx, {
                        type: 'bar',
                        data: {
                            labels: data.timestamps,
                            datasets: [{
                                label: 'Instantaneous Affluence (15-minute intervals)',
                                data: data.counts,
                                backgroundColor: 'rgba(153, 102, 255, 0.6)',
                                borderColor: 'rgba(153, 102, 255, 1)',
                                borderWidth: 1
                            }]
                        },
                        options: {
                            scales: {
                                x: {
                                    type: 'time',
                                    time: {
                                        unit: 'minute',
                                        displayFormats: {
                                            minute: 'HH:mm'
                                        }
                                    }
                                }
                            }
                        }
                    });
                }
            }).catch(error => console.error('Error fetching instantaneous data:', error));
    }

    // Event listeners for dropdowns
    objectTypeDropdown.addEventListener('change', fetchAndUpdateCharts);
    timeRangeDropdown.addEventListener('change', fetchAndUpdateCharts);

    // Initial fetch and chart setup
    fetchAndUpdateCharts();

    // Auto-update charts every 5 seconds
    setInterval(fetchAndUpdateCharts, 5000);
});
