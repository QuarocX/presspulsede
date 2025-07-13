<?php
header('Content-Type: application/json');

$resultFile = '/tmp/sentiment_result.json';

if (file_exists($resultFile)) {
    $content = file_get_contents($resultFile);
    $data = json_decode($content, true);
    if ($data !== null) {
        echo json_encode(['status' => 'complete', 'results' => $data]);
        unlink($resultFile); // Delete the temporary file
    } else {
        echo json_encode(['status' => 'processing']);
    }
} else {
    echo json_encode(['status' => 'processing']);
}
?>