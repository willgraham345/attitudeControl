%%
clear; close all; clc; format compact;

% V_in = 4.1*1000; %voltage in
% I_out = .002; %A
% R = V_in/I_out;
% 
% % Define RC System
% 
% 
T_pwm = 1 / (200*100); % PWM wave time constant when duty = 1/100
T_pwm_rad = T_pwm * pi/ 180
% Therefore, step input, CAN be on/off as quickly as T_pmw each
% 
% R = 100;
% C = 100e-12;% 100 pF
% 
% num = [1 / (R*C)];
% den = [1, 1/(R*C)]
% % den = [C*R, 1];
% % num = [C*R, 0];
% sys = tf(num, den)

%% Simulate
% fig1 = stepplot(sys)



V_in = 4.1*1000; %voltage in
I_out = .002; %A

R = 1e3;
C = 5e-12;% 100 pF

cutoff_freq = 1 / (2*pi*R*C)

%%


num = [1];
den = [1/(R*C), 1]

sys = tf(num, den)
opt = stepDataOptions('InputOffset', 5000, 'StepAmplitude', 0)

[y, tspan] = step(sys, opt);

figure(1)
plot(tspan, y)
title('Problem 1 Time Response')
xlabel('Time')
ylabel('Time Displacement')

figure(2)
opts = bodeoptions;
opts.FreqUnits = 'Hz'
bode(sys, opts)
