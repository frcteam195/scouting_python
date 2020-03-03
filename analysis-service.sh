#!/usr/bin/env bash

if [ "$(id -u)" -ne 0 ] ; then
  echo "This script must be run as root or with sudo"
exit 1
fi

if [ -z "$1" ]; then
  echo "you must enter an argument [start] or [stop]"
  echo "Usage: sudo analysis-service.sh start|stop"
fi

if [ "$1" != "start" ] && [ "$1" != "stop" ]; then
  echo "'start' and 'stop' are the only valid arguments"
  exit 1
fi

if [ "$1" == start ]; then
  if grep -q AnalysisIR /var/spool/cron/crontabs/nmradmin
  then
    echo 'It appears that AnalysisIR.py is already running as a cron job!'
    echo 'Aborting!'
    exit 1
  else
    echo 'Creating clean log file AnalysisIR.log'
    echo 'Adding AnalysisIR.py to cron'
    rm -f /tmp/AnalysisIR.log
    touch /tmp/AnalysisIR.log
    chmod a+rw /tmp/AnalysisIR.log
    echo '*/1 * * * * /usr/bin/python3 /home/nmradmin/scouting_python/AnalysisIR.py >> /tmp/AnalysisIR.log' >> /var/spool/cron/crontabs/nmradmin
  fi
fi

if [ "$1" == stop ]; then
  if grep -q AnalysisIR /var/spool/cron/crontabs/nmradmin
  then
    echo 'AnalysisIR.py is being removed from cron'
    sed -i '/AnalysisIR/d' /var/spool/cron/crontabs/nmradmin
  else
    echo 'AnalysisIR.py is not currently in cron. Doing nothing!'
    exit 1
  fi
fi
