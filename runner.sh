#!/usr/bin/env bash
log_dir=/home/lsh/code/bishe/static/log
log_file=$log_dir/$(date +%Y-%m-%d-%H:%M).log
echo "command:" | tee -a $log_file
echo $* | tee -a $log_file
$* | tee -a $log_file
echo "" | tee -a $log_file
