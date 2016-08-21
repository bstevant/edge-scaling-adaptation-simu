set terminal png
set output "rtt2.png"
set xlabel '% mean RTT'
set ylabel '% of nodes < RTT'
plot "./rtt2.txt" u 1:2 w l