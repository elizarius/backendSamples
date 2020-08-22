<?php
openlog("myScriptLog",  LOG_CONS | LOG_NDELAY | LOG_PID | LOG_PERROR, LOG_USER | LOG_SYSLOG);

echo "Hello from AELZ! <br>";
syslog(LOG_ERR, "Hello from AELZ");

closelog();

$list = array (
    array('aaa', 'bbb', 'ccc', 'dddd'),
    array('123', '456', '789'),
    array('"aaa"', '"bbb"')
);

$fp = fopen('aelz.csv', 'w');

foreach ($list as $fields) {
    fputcsv($fp, $fields);
}

fclose($fp)

?>
