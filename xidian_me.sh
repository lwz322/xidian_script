#!/bin/sh
log_file="./xidian_me.log"
[ -f $log_file ] && pre_value=$(tail -1 $log_file | awk '{print $6}')
query_output=$(python3 ./xidian_me_log.py 2>/dev/null)
query_value=$(echo $query_output | awk '{print $6}')
[ $pre_value != $query_value ] || exit 0
[ -z $pre_value ] && useage=`echo $pre_value-$query_value | bc`
echo $query_output $useage >> $log_file