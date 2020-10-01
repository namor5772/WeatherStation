<!DOCTYPE html>
<html>

<head>

<title>RMG IOT</title>

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
html {
    font-family:"LucindaSans", sans-serif:
    }

.header {
    background-color: #9933cc;
    color: #ffffff;
    padding: 3px;
    }

.center {
    display: block;
    margin-left: auto;
    margin-right: auto;
    width: 98%;
    }

.footer {
    background-color: $0099cc;
    color: #ffffff;
    text-align: center;
    font-size: 20x;
    padding: 3px;
    }

h1 {
    margin-top: 5px;
    margin-bottom: 5px;
    margin-left: 5px;
    }

* {
    box-sizing: border-box;
    }

.row::after {
    content: "";
    clear: both;
    display: table;
    }

[class*="col-"] {
    float: left;
    padding: 3px;
    width: 100%;
}

@media screen and (orientation:portrait){
    body {
        margin: 1em;
        font-family: Tahoma, Verdana, Arial, sans-serif;
        background-color: lightgray;
    }
    .col-s-1 {width: 50%;}
    .col-s-2 {width: 100%;}
}

@media screen and (orientation:landscape){
    body {
        margin: 1em;
        font-family: Tahoma, Verdana, Arial, sans-serif;
	background-color: white;
    }
    .col-1 {width: 50%;}
    .col-2 {width: 100%;}
}

</style>
</head>

<body>

<div class="header">
    <h1> Raspberry Pi IOT interface </h1>
</div>

<div class="row">

    <div class="col-1 col-s-1">
        <br>
	<form action="#" method="post">
		Command:
		<input type="text" name="cmd" autofocus/>
		<input type="submit" value="SUBMIT" />
	</form>
	<br>

<?php
    $input = strtolower($_POST['cmd']);

    echo "The cmd you sent is: <br />\n";
    echo $input, "<br /><br />\n";
    $timeID = date("His");
    $regrec = implode(", ", $_POST);
    $finalrec = strtolower($timeID . $regrec);

    // Read 1st line of current result file
    $myresult1 = fopen("/var/tmp/result.txt","r");
    $result1 = fgets($myresult1);
    fclose($myresult1);

    $fp = fopen("/var/tmp/text.txt","w");
    if (fwrite($fp,$finalrec) == FALSE) {
	    echo "Cannot write file.", "<br />\n";
    }
    else {
        // keep waiting until result.txt file changes, which means results
        // are ready to be viewed on this webpage
       do {
           sleep(1);    
           // Read 1st line of current result file
           $myresult2 = fopen("/var/tmp/result.txt","r");
           $result2 = fgets($myresult2);
           fclose($myresult2);
        } while (strcmp($result1,$result2)==0);    

        echo "The Result is:", "<br /> \n";
        $myresult = fopen("/var/tmp/result.txt","r");
        fgets($myresult);
        while(! feof($myresult)) {  
            echo fgets($myresult),"<br />";
	    }
	    fclose($myresult);
    }
    fclose($fp);

   echo '</div>';
   echo '<div class="col-1 col-s-2">';
   sleep(2);
    if (substr($input,0,2)=="tp"){
        // display photo if "take photo" command starting with "tp" was sent to server (it might have more arguments)
	    echo '<p> <img src="photo.jpg" alt="Just taken photo" class="center"></p>';}
    elseif (substr($input,0,2)=="gp"){
        // display photo if "get photo" command starting with "gp" was sent to server (it might have more arguments)
	    echo '<p> <img src="photo.jpg" alt="Last photo taken" class="center"></p>';}
    elseif (strtoupper(substr($input,0,3))=="LDG"){
        // display appropriate archive photo if command "LDG" was sent to server
	    echo '<p> <img src="LDG.jpg" alt="photo of LDG in studio" class="center"></p>';}
    elseif (substr($input,0,2)=="gd"){
        // display link to appropriate file (for download) if command "gd" was sent to server
	    echo '<a href="SensorData.csv" download> sensor data</a>';}
    elseif (substr($input,0,3)=="php"){
        // display php info if command "php" was sent to server
	    phpinfo();}
    echo '</div>';
    echo '</div>';
?>

</body>
</html>
