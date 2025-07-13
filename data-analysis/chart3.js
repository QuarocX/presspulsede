function renderTimeChart() {
    const ctx = document.getElementById('timeChart').getContext('2d');

    // Prepare data for the time series chart
    const timeData = [];

    window.articles.forEach(article => {
        const dateTime = article.date_time; // Get date_time from article
        if (dateTime) {
            // Convert date_time to a Date object
            const date = new Date(dateTime);
            timeData.push({ x: date.getTime(), y: 1 }); // Use getTime() for linear scale
        }
    });

    // Aggregate data by date
    const aggregatedData = {};
    timeData.forEach(dataPoint => {
        const dateKey = new Date(dataPoint.x).toISOString().split('T')[0]; // Get date in YYYY-MM-DD format
        if (!aggregatedData[dateKey]) {
            aggregatedData[dateKey] = 0;
        }
        aggregatedData[dateKey] += dataPoint.y; // Sum occurrences for each day
    });

    // Create an array of all dates in the range
    const allDates = Object.keys(aggregatedData);
    const startDate = new Date(Math.min(...allDates.map(date => new Date(date))));
    const endDate = new Date(Math.max(...allDates.map(date => new Date(date))));
    
    // Fill in missing dates with zero counts
    const chartData = [];
    for (let d = startDate; d <= endDate; d.setDate(d.getDate() + 1)) {
        const dateKey = d.toISOString().split('T')[0]; // Format as YYYY-MM-DD
        chartData.push({
            x: d.getTime(),
            y: aggregatedData[dateKey] || 0 // Use 0 if no articles were published on this date
        });
    }

    // Create the line chart
    new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'Number of Articles Published Over Time',
                data: chartData,
                borderColor: 'rgba(75, 192, 192, 1)',
                fill: false,
                tension: 0 // Set tension to 0 for straight lines
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'linear', // Change to linear scale
                    position: 'bottom',
                    title: {
                        display: true,
                        text: 'Date'
                    },
                    ticks: {
                        callback: function(value) {
                            return new Date(value).toLocaleDateString(); // Format ticks as dates
                        }
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Articles'
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        title: function(tooltipItems) {
                            const date = new Date(tooltipItems[0].parsed.x); // Get the x value (timestamp)
                            const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
                            return date.toLocaleDateString(undefined, options); // Format the date nicely for the tooltip title
                        },
                        label: function(tooltipItem) {
                            return `Number of Articles: ${tooltipItem.parsed.y}`; // Show number of articles in tooltip label
                        }
                    }
                }
            }
        }
    });
}

// Call this function to render the time chart after loading data
loadData().then(() => renderTimeChart());
