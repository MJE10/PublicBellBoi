<?php

$events = json_decode($_POST['events']);

$dbServername = "";
$dbUsername = "";
$dbPassword = "";
$dbName = "";

$conn = mysqli_connect($dbServername, $dbUsername, $dbPassword, $dbName);

$stmt = $conn->prepare("DELETE FROM periods");
$stmt->execute();

$type = "period";
$event_number = "4";
$time_start = strval(time() + 1000);
$time_end = strval(time() + 2000);

$stmt = $conn->prepare("INSERT INTO periods (event_type, event_number, time_start, time_end) VALUES (?, ?, ?, ?)");
$stmt->bind_param("ssss", $type, $event_number, $time_start, $time_end);

foreach ($events as $event) {
    $type = $event[0];
    $event_number = $event[1];
    $time_start = $event[2];
    $time_end = $event[3];
    $stmt->execute();
    echo $type." ".$event_number.": ".$time_start." to ".$time_end."<br>";
}