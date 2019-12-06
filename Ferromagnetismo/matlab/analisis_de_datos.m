tempRef = 20.0 % Temperatura ambiente ó referencia de la termicupla

%% Sensor DAQ



%s = sdaq.createSession; 
% ó
T=0.1;
Rate=round(100000);

s = daq.createSession('ni');
s.Rate = Rate; %rate de medicion
s.DurationInSeconds = T; %duracion de cada adq.
    % Agregamos los canales que vamos a medir
chH = s.addAnalogInputChannel('Dev15','ai4','Voltage');
chH.InputType = 'Differential';
chM = s.addAnalogInputChannel('Dev15','ai2','Voltage');
chM.InputType = 'Differential';
chT = s.addAnalogInputChannel('Dev15','ai13','Voltage');
chT.InputType = 'SingleEnded';
chT.Range = [-1 1];
data= startForeground(s)

%%
listaTemps=(-190:2:6-0.1)

N=4;
data_ch1= zeros(round(s.DurationInSeconds*s.Rate),N);
data_ch2= zeros(round(s.DurationInSeconds*s.Rate),N);
data_ch3= zeros(round(s.DurationInSeconds*s.Rate),N);
res=zeros(1,N);
temp=zeros(1,N);
tiempo=zeros(1,N);
% Medición de M, H y T
% Defino los valores de temperatura

% Defino los valores de resistencia 
tic
figure(1)

termoKCoef = [2.5173462E+01,-1.1662878E+00,-1.0833638E+00,-8.9773540E-01,-3.7342377E-01,-8.6632643E-02,-1.0450598E-02,-5.1920577E-04,0.0000000E+00]

for (k=1:N)
    
    data= startForeground(s);
    data_ch1(:,k)=data(:,1);
    data_ch2(:,k)=data(:,2);
    data_ch3(:,k)=data(:,3);
    tiempo(k)=toc;
    
    mV_termocupla = mean(data_ch3(:,k)) * 1000; % tension media de la termocupla durante una medicio y pasaje a milivolts
    for i = 1:length(termoKCoef)
        temp(k) = temp(k) + termoKCoef(i)* mV_termocupla^i;
    end
    temp(k)= temp(k) + tempRef;
    
    
    pause(0.8);
    disp([k temp(k)])
    %hold on
    plot(data_ch1(:,k),data_ch2(:,k),'.')
end
dlmwrite('dataH9.txt',data_ch1,'delimiter',';')
dlmwrite('dataB9.txt',data_ch2,'delimiter',';')
dlmwrite('TEMP9.txt',temp,'delimiter',';')


%% Centrar curvas de histéresis
% Calculo el corrimiento de H y de M respecto del origen   
    promH = mean(data_ch1(:,k))
    promM = mean(data_ch2(:,k))  
    mH = repmat(promH,s.DurationInSeconds*s.Rate,1)
    mM = repmat(promM,s.DurationInSeconds*s.Rate,1)
    
% Creo las nuevas variables centradas en el origen    
    H = data_ch1(:,k)-mH;
    M = data_ch2(:,k)-mM;


k = (1:98) 
    plot(H(:,k),M(:,k))


%% M(T)

% Magnetización cuando H=0
M0 = [];
for k = 1:98
    k
    MH =  [M(:,k) H(:,k)];
    MHp = [];
    MHn = [];
    for i = 1:1001
        if MH(i,2) > 0 && MH(i,1) > 0 
            MHp = [MHp; MH(i,1) MH(i,2)];
        end
        if MH(i,2) < 0 && MH(i,1) > 0 
            MHn = [MHn; MH(i,1) MH(i,2)];
        end
    end
    M0p = [];
    [Np cp] = size(MHp);
    for i = 1:Np
        if MHp(i,2) == min(MHp(:,2))
            M0p = [M0p MHp(i,1)];
        end
    end
    M0n=[];
    [Nn cn] = size(MHn);
    for i = 1:Nn
        if MHn(i,2) == max(MHn(:,2))
            M0n = [M0n MHn(i,1)];
        end
    end
    S = [mean(M0p); mean(M0n)];
    M0k = mean(S);
    M0 = [M0; M0k]  
end

%Temperatura
T = []
for k = 1:98
    k
    res = data_ch3(:,k)*1000;
    mres = mean(res);
    t_k = -242.32+2.24381*mres+0.00222*(mres)^2-4.26247*10^(-6)*(mres)^3;
    T = [T; t_k]
end
for n = 1:85
plot(T(1,1),M0(1,1),'r*')
end    
