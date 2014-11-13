#!/bin/bash

basename="current_src_confB_trans_"
for ii in `seq 0 255`; do
    filename=$(printf "%s%04d" "$basename" "$ii")
    echo $filename
    gnuplot -e "filename='$filename'" plot_configB_trans.plt
done
