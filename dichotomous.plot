set terminal png size 1024,768
set output "res2.png"
set xlabel 'Iterations'
set ylabel 'Nb instances'
set key outside right; set key title "SLA / Mean RTT";
plot "./res2_200.txt" u 1:2 w l title "100%", "./res3_200.txt" u 1:2 w l title "Step", "./res4_200.txt" u 1:2 w l title "Violation"