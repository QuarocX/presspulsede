<?php
$pythonScript = "/home/llm/sentiment-analysis1.py";
exec("python3.7 $pythonScript", $output, $returnCode);

if ($returnCode === 0) {
    // Join the output array into a single string
    $jsonString = implode("\n", $output);
    
    // Remove the ```json at the start and ``` at the end
    $jsonString = preg_replace('/^```json\s*|\s*```$/s', '', $jsonString);
    
    // Decode the JSON string
    $data = json_decode($jsonString, true);
    
    if ($data === null && json_last_error() !== JSON_ERROR_NONE) {
        echo "<p>Error decoding JSON: " . htmlspecialchars(json_last_error_msg()) . "</p>";
    } else {
        // Output the HTML
        echo "<!DOCTYPE html>\n<html lang='en'>\n<head>\n";
        echo "<meta charset='UTF-8'>\n";
        echo "<meta name='viewport' content='width=device-width, initial-scale=1.0'>\n";
        echo "<title>Sentiment Analysis Results</title>\n";
        echo "<style>\n";
        echo "body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }\n";
        echo "h1 { color: #2c3e50; }\n";
        echo "h2 { color: #34495e; }\n";
        echo ".overall { font-size: 1.2em; font-weight: bold; margin-bottom: 20px; }\n";
        echo ".subtopic { background-color: #f9f9f9; border: 1px solid #ddd; padding: 15px; margin-bottom: 20px; border-radius: 5px; }\n";
        echo ".sentiment { font-weight: bold; }\n";
        echo ".comments { margin-top: 10px; }\n";
        echo "</style>\n";
        echo "</head>\n<body>\n";
        
        echo "<h1>Sentiment Analysis Results</h1>\n";
        echo "<p class='overall'>Overall Sentiment: " . htmlspecialchars($data['overall_sentiment']) . "</p>\n";
        
        foreach ($data['subtopics'] as $subtopic) {
            echo "<div class='subtopic'>\n";
            echo "<h2>" . htmlspecialchars($subtopic['topic']) . "</h2>\n";
            echo "<p class='sentiment'>Sentiment: " . htmlspecialchars($subtopic['sentiment']) . "</p>\n";
            echo "<div class='comments'>\n<h3>Comments:</h3>\n<ul>\n";
            foreach ($subtopic['comments'] as $comment) {
                echo "<li>" . htmlspecialchars($comment) . "</li>\n";
            }
            echo "</ul>\n</div>\n";
            echo "</div>\n";
        }
        
        echo "</body>\n</html>";
    }
} else {
    echo "<p>Error running Python script. Return code: " . htmlspecialchars($returnCode) . "</p>";
}
?>