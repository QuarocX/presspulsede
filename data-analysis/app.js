const basePath = '../'; // Path to JSON files one level up
const newspapers = ['spiegel.json', 'taz.json', 'faz.json', 'sueddeutsche.json', 'zeit.json']; // Add your JSON files here

async function loadData() {
    const articles = []; // Array to hold all articles

    try {
        for (const newspaper of newspapers) {
            const response = await fetch(basePath + newspaper);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            if (!Array.isArray(data)) {
                throw new Error('Expected an array from the JSON file');
            }
            articles.push(...data); // Add articles from this newspaper to the array
        }
        return articles; // Return all articles for use in charts
    } catch (error) {
        console.error('Error loading data:', error);
        return null; // Return null on error
    }
}

// Load data and initialize charts after data is fetched
loadData().then(articles => {
    if (articles) {
        window.articles = articles; // Make articles globally accessible for other scripts
        renderCategoryChart(); // Call to render the category chart
        renderWeekdayChart();   // Call to render the weekday chart
        renderTimeChart(); //Call to render time chart
        // Call additional chart functions as needed
    }
});
