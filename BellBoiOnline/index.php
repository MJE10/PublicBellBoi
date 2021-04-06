<!DOCTYPE html>
<html>
    
<?php
if (!($_SERVER['HTTPS'] and $_SERVER['HTTPS'] == 'on')) header('Location: https://voitheia.online/ring');
?>

<head>
    <title>BellBoi Online</title>
    <meta name="author" content="Michael Elia">
    <script src='https://code.jquery.com/jquery-3.1.0.min.js'></script>
</head>

<body>

    <div id="all">
        <h2 id="bellboionline">BellBoi Online &nbsp;&nbsp;<a href="https://voitheia.online/ring/about" style="text-decoration: none;">&#9432;</a></h2>
        <br>

        <div id="oopsDiv">
            <h2>Searching for upcoming periods...</h2>
        </div>

        <div id="endTimeDiv">
            <h2>Period 2 ends in</h2><br>
            <div class="timer">
                <h1 id="endTimerText" class="timerText"></h1>
            </div>
        </div>

        <div id="startTimeDiv">
            <h2>Period 3 begins in</h2><br>
            <div class="timer">
                <h1 id="startTimerText" class="timerText"></h1>
            </div>
        </div>
        <br>
        <h2 id="dateTime"></h2>
        <br>
        <h2 id="dayNumber"></h2>
        <br><br>
        <h2 id="codedby">Coded by Michael Elia</h2>
        <br>
    </div>
</body>

<style>
    * {
        color: white;
        font-family: sans-serif;
        font-weight: normal;
    }

    body {
        background-color: #2c2f33;
        text-align: center;
        padding: 4em;
    }

    h2 {
        display: inline-block;
    }

    #all {
        display: inline-block;
        background-color: #23272a;
        padding: 2em;
        border-radius: .3em;
    }

    .timer {
        background-color: #2c2f33;
        display: inline-block;
        padding: 0 1em 0 1em;
        border-radius: .3em;
    }

    #bellboionline {
        font-size: xx-large;
        margin: 0;
    }

    #codedby {
        margin-bottom: 0;
    }

    #startTimeDiv, #endTimeDiv, #dayNumber {
        display: none;
    }
</style>

<script>
    
    dayNumber = "";

    var phpInfo = <?php

        $allInfo = "";

        $dbServername = "";
        $dbUsername = "";
        $dbPassword = "";
        $dbName = "";

        $conn = mysqli_connect($dbServername, $dbUsername, $dbPassword, $dbName);

        $tz = 'EST';
        $timestamp = time() + 3600;
        if (date('I', time())) {
            $timestamp += 3600;
        }
        $dt = new DateTime("now", new DateTimeZone($tz));
        $dt->setTimestamp($timestamp); //adjust the object to correct timestamp

        $stmt = $conn->prepare("SELECT * FROM periods WHERE time_end > ?");
        $stmt->bind_param("s", strval(time()));
        $stmt->execute();
        $result = $stmt->get_result();
        while ($row = mysqli_fetch_assoc($result)) if ($row['event_type'] == 'period') {
            if (intval($row['time_start']) < time()) {
                $diff = intval($row['time_end']) - time();
                $new_date = $dt->add(new DateInterval('PT'.strval($diff).'S'));
                $allInfo = "\"e_".$row['event_number']."_".strval($diff)."_".$new_date->format('l F jS, Y \a\t h:i A')."\";";
                break;
            }
            $diff = intval($row['time_start']) - time();
            $new_date = $dt->add(new DateInterval('PT'.strval($diff).'S'));
            $allInfo = "\"s_".$row['event_number']."_".strval($diff)."_".$new_date->format('l F jS, Y \a\t h:i A')."\";";
            break;
        }
        
        $stmt = $conn->prepare("SELECT * FROM periods WHERE event_type = 'day' AND time_end > ? AND time_start < ?");
        $stmt->bind_param("ss", strval(time()), strval(time()));
        $stmt->execute();
        $result = $stmt->get_result();
        while ($row = mysqli_fetch_assoc($result)) {
            $allInfo = $allInfo.'dayNumber = "'.$row['event_number'].'"';
            break;
        }
        
        echo $allInfo;
    ?>;
    
    var startDate = undefined;
    var endDate = undefined;

    function main() {
        if (phpInfo.charAt(0) === "s") {
            // alert('start');
            total_seconds = parseInt(phpInfo.split('_')[2]);
            startDate = new Date();
            startDate.setSeconds(startDate.getSeconds() + total_seconds);
            
            $("#startTimeDiv h2").text("Period " + phpInfo.split('_')[1] + " begins in");
            $("#dateTime").text("on "+phpInfo.split('_')[3]);
            updateOutput();
            $("#oopsDiv").hide();
            $("#startTimeDiv").show();
            
        } else if (phpInfo.charAt(0) === "e") {
            // alert('end');
            total_seconds = parseInt(phpInfo.split('_')[2]);
            endDate = new Date();
            endDate.setSeconds(endDate.getSeconds() + total_seconds);
            
            $("#endTimeDiv h2").text("Period " + phpInfo.split('_')[1] + " ends in");
            $("#dateTime").text("on "+phpInfo.split('_')[3]);
            updateOutput();
            $("#oopsDiv").hide();
            $("#endTimeDiv").show();
        }
        if (dayNumber !== "") {
            $("#dayNumber").text("It is a day " + dayNumber + "!");
            $("#dayNumber").show();
        }
    }

    function formatTime(x) {
        return x[0] + " hours, " + x[1] + " minutes, and " + x[2] + " seconds";
    }
    
    function formatTimeDate(date_seconds) {
        if (date_seconds < 0) location.reload();
        
        hours = Math.floor(date_seconds/3600);
        if (hours != 1) hours = hours + " hours, ";
        else hours = hours + " hour, ";
        
        minutes = Math.floor((date_seconds%3600)/60);
        if (minutes != 1) minutes = minutes + " minutes";
        else minutes = minutes + " minute";
        
        seconds = date_seconds%60;
        if (seconds != 1) seconds = " and " + seconds + " seconds";
        else seconds = " and " + seconds + " second";
        
        if (hours === "0 hours, ") return minutes + seconds;
        else return hours + minutes + "," + seconds;
        
        return hours + minutes + seconds;
    }

    function updateOutput() {
        var now = new Date();
        if (startDate != undefined) $("#startTimerText").text(formatTimeDate(Math.floor((startDate - now)/1000)));
        if (endDate != undefined) $("#endTimerText").text(formatTimeDate(Math.floor((endDate - now)/1000)));
        setTimeout(updateOutput, 1000);
    }

    $(document).ready(main);

</script>

</html>