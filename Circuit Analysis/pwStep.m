function u = pwStep(tspan, waveVal)
for i =[1:length(tspan)]
    
     if (0<tspan(i)) && (tspan(i) <=1*waveVal)
         u(i) = 0;
     elseif (1*waveVal<tspan(i)) && (tspan(i)<=2*waveVal)
         u(i) = 1;
     elseif 2*waveVal<tspan(i) && (tspan(i)<=3*waveVal)
         u(i) = 0;
     elseif 3*waveVal<tspan(i) && tspan(i)<=4*waveVal
         u(i)= 1;
     else
         u(i) = 0;
 end
end

 
end