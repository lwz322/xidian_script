#!/bin/sh
log_file="/root/xidian_me.log"
script_path="/root/xidian_me_log.py"
[ -f $log_file ] && pre_value=$(tail -1 $log_file | awk '{print $6}')
query_output=$(python3 $script_path 2>/dev/null)
query_value=$(echo $query_output | awk '{print $6}')
[ "$pre_value" != "$query_value" ] || exit 0
[ -n $pre_value ] && useage=`echo $pre_value-$query_value | bc`
echo $query_output $useage >> $log_file