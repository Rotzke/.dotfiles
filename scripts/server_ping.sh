#!/bin/bash

/bin/ping -c 1 8.8.8.8 &> /dev/null || /usr/bin/notify-send "Google DNS" "is not available"

