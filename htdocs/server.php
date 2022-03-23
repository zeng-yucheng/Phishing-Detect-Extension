<?php
header("Access-Control-Allow-Origin: *");
error_reporting(0);
$url = $_POST["url"];
// $res = exec("cmd.exe /k cd ../..", $out, $return);
$result = exec("cmd.exe /k python ../../../NUS/S2/CS5331/Proj/proj/Phishing-Detect-Extension/script/main.py $url 2>&1", $output, $return);
$idx = sizeof($output) - 3;
echo $output[$idx];
?>
