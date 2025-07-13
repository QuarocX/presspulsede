function renderCategoryChart() {
    const ctx = document.getElementById('categoryChart').getContext('2d');
    
    const categoryCounts = {};
    
    window.articles.forEach(article => {
        const category = article.category;
        if (category) { // Ensure category exists
            categoryCounts[category] = (categoryCounts[category] || 0) + 1;
        }
    });

    const labels = Object.keys(categoryCounts);
    const data = Object.values(categoryCounts);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Number of Articles per Category',
                data: data,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
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
