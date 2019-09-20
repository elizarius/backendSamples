How to run:
----------
git clone https://github.com/elizarius/backendSamples.git
cd  backendSamples/httpScanner
python3 http_scan.py


Design questions
----------------
Assuming we wanted to simultaneously monitor the connectivity (and latencies) from multiple
geographically distributed locations and collect all the data to a single report that always
reflects the current status across all locations. Describe how the design would be different.

How would you transfer the data?
- Cliens starts on remote location
- Syslog logger should be used (rsyslog)
- Syslog logger initiated in main function when scanner instance created
- Syslog logger prints messages  to rsyslog
- Rsyslog configured to transfer logs to remote server via rsyslog  protocol (RFC 3164)
- Remote rsyslog server accumulates logs from multiple  sources
- Time zone should be taken into considearation when analyse log files

Security considerations?
 - Use rsyslog with tls:
   https://www.golinuxcloud.com/secure-remote-logging-rsyslog-tls-certificate/

 - Extra option could be use IPSec (Ikev2 / Strongswan ) as secure transmission (actually heavy solution)

TBD
---
1. Implement logging to file
2. Implement class based approach
