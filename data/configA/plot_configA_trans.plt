#set term postscript enhanced eps color font "Helvetica,18" size 4in,2.5in
#set term jpg color enhanced "Helvetica" 18
set term png

testName = filename.".csv"
if (!exists("testName")) filename = "current_src_confA_trans_0000"

set output filename.".png"
#set output filename.".eps"
set border 11 lw 2
set ytics nomirror
set xtics nomirror

#set lmargin 11
#set rmargin 12
#set bmargin 10 
set xlabel "Time"
set ylabel "Current uA"

#set yrange [2.5e0:1e2]
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
plot	filename.".csv" using 2:($3/10E3*1E6) title "Transient" with lines ls 1 lc 1 lw 2

#replot;
