set terminal png
set output "res1.png"
set xlabel 'Nb of service instances'
set ylabel 'Nb of SLA violations'
set key outside right; set key title "SLA / Mean RTT";
plot "./res1.txt" u 1:2 w l title "200%", "res1.txt" u 1:3 w l title "100%", "res1.txt" u 1:4 w l title "50%"  ,  "res1.txt" u 1:5 w l title "25%",  "res1.txt" u 1:6 w l title "10%",  "res1.txt" u 1:7 w l title "5%"