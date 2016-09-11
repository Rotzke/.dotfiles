#!/bin/bash

/bin/ping -c 1 8.8.8.8 &> /dev/null && (/bin/ping -c 1 10.100.82.141 &> /dev/null && : || /usr/bin/notify-send "Server Status" "Server is down") || /usr/bin/notify-send "Google DNS" "is not available"

