#!/bin/bash
ping -q -w 1 -c 1 google.fr > /dev/null && echo ok || python wifirst_reconnect.py
