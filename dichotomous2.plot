set terminal png size 1024,768
set output "res5.png"
set xlabel 'Iterations'
set ylabel 'Nb instances'


set key outside right ; set key title ""
set boxwidth 0.5 relative
set style fill solid 0.2

plot "./res5_100.txt" u 1:2 w boxes title "SLA Violation", "./res5_100.txt" u 1:3 w l title "Srv Instances"