#!/bin/bash
# Author : farid < farid_@msn.com >
# Restart Service 
# Restart Service high consume memory

threshold=88 #percent
total=$(free | grep "Mem:" | awk '{print $2}')
remaining=$(free | grep "Mem:" | awk '{print $4}')
current=$(echo "scale=0;100-$remaining * 100 / $total" | bc -l)

if [ $current -gt $threshold ]
then
 service uwsgi-emperor restart
      echo "Restarted Emperror  on `date +'%Y-%m-%d %H:%M:%S'`. RAM utilization at ${current}%" >> /var/log/uwsgi_restarter.log

fi

