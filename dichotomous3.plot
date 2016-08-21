set terminal png size 1024,768
set output "res6.png"
set xlabel 'Iterations'
set ylabel 'Nb instances'
set key outside right; set key title "SLA / Mean RTT";
plot "./res6_10.txt" u 1:2 w l title "Nb Instances", "./res6_10.txt" u 1:3 w l title "Nb Clients"