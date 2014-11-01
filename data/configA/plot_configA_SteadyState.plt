set term postscript enhanced eps color font "Helvetica,18" size 4in,2.5in

#set output
filename = "current_src_confA_steady"

set output filename.".eps"
set border 11 lw 2
set ytics nomirror
set xtics nomirror

#set lmargin 11
#set rmargin 12
#set bmargin 10 
set xlabel "Resistance"
set ylabel "Current mA"

set yrange [1E-6:103]
#set xrange[:256]
#set grid
#set log y

#set terminal postscript eps enhanced 
#set term x11

#set key at 0.24,3 font "Arial, 20" spacing 2.5 #upper right corner 
#set key out horiz
set key bottom center font "Helvetica, 16"
#set key off
#set title "uSDR cold boot"

set datafile separator ","
#start_pt=10000
#duration=110000
plot	filename.".csv" using 2:($3/10000*1E3) title "Steady State" with lines ls 1 lc 1 lw 2

#replot;
