function renderWeekdayChart() {
    const ctx = document.getElementById('weekdayChart').getContext('2d');
    
    const weekdayCounts = {};
    
    window.articles.forEach(article => {
        const weekday = article.weekday;
        if (weekday) { // Ensure weekday exists
            weekdayCounts[weekday] = (weekdayCounts[weekday] || 0) + 1;
        }
    });

    const labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    const data = labels.map(day => weekdayCounts[day] || 0); // Fill in counts or zero

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Number of Articles Published per Weekday',
                data: data,
                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                borderColor: 'rgba(153, 102, 255, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}
