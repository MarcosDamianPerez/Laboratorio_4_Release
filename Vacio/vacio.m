close all;
clear all;
instrreset;
%%

% Crear y configurar la interfaz con el sensor de presión
interfazPesion = serial('COM14','BaudRate',9600,'DataBits',8,'StopBits',1,'Parity','none', 'terminator','CR') ;

% Crear y configurar la interfaz con el sensor de presión
interfazMultimetro = serial('COM16','BaudRate',9600,'DataBits',8,'StopBits',1,'Parity','none');
set(multimetro,'terminator','CR','InputBufferSize',15,'ReadAsyncMode','manual');

% Abrir la comunicacion con el multimetro y el sensor de presión
fopen(interfazPesion);
fopen(interfazMultimetro);

%% MEDICION SIMPLES

% El script amprobe38XRA(interfaz, verbose) se encarga de comunicarse con el multimetro y pedirle la ultima medicion.
% 	@interfaz es la interfaz serial con el multimetro
%	@verbose: si es distinto de 0, el script muestra por pantalla la informacion que devuelve el multimetro
verbose=0;
[Ylab , valueMultimetro, str, count] = amprobe38XRA(interfazMultimetro, verbose);

fprintf('Valor: %g %s \n',valueMultimetro,Ylab);

% El enviando la cadena ?GAx, el medidor de vacio devuelve un string con la presion del sensor conectado a la salida "x"
% de la electronica.
% 	Ej: query(interfaz,'?GA1') devuelve la presion del sensor conectado a la salida gauge 1 
strpresion = query(interfazPesion,'?GA1'); 

%derecha esta midiendo sobre el platino
%izquierda esta midiendo sobre la R de 1 ohm

%26 de junio medimos 

cantidadDeMediciones = 3000;		% Numero total de mediciones
pausaEntreMediciones = 2;			% Pausa en segundos entre que termina una medicion y comienza la siguiente
nombre = 'enfriamientodifusora';	% Nombre del archivo donde se van a guardar los datos

% NumeroTotal_Proceso_Descripcion_NumeroParcial

tiempo =  zeros(1,cantidadDeMediciones);
temperatura = zeros(1,cantidadDeMediciones);
presion = zeros(1,cantidadDeMediciones);

archivo_de_datos = strcat(nombre,'.txt');       %crea el nombre del archivo de datos con su extensiónn
FILE = fopen(archivo_de_datos,'at');			%crea el archivo
fprintf(FILE,'%s \n','$ Medicion; Tiempo; Presion; Temperatura' ); %Escribe el encabezado del archivo

tic												%iniciar cronometro					
for indice = 1:cantidadDeMediciones
    fprintf('Medicion: %d de %d.\n', indice, cantidadDeMediciones)
	tiempo(indice) = toc;											%Medicion de tiempo del cronometro
	presion(indice) = str2double(query(interfazPesion,'?GA1')) ;	%pide la presion y transforma el string que recibe a double
    [Ylab , valueMultimetro, str, count] = amprobe38XRA(interfazMultimetro, verbose); %pide una medicion al mulktimetro
    temperatura(indice) = valueMultimetro;							%guarda el valor del multimetro en la variable temperatura
	figure(1);
	subplot(2,1,1);													%crear una figura con 2 subplot de 2 filas y una columna y
																	%graficar en la figura de arriba 
	plot(tiempo(1:indice), presion(1:indice), '.')
	subplot(2,1,2); 												%crear una figura con 2 subplot de 2 filas y una columna y
																	%graficar en la figura de abajo 
	plot(Tiempo(1:indice), temperatura(1:indice), '.')


	fprintf(FILE, '%d ;', indice);									%guardar los valores obtenidos en el archivo
	fprintf(FILE, '%f ;', tiempo(indice));
	fprintf(FILE, '%f ;', presion(indice));
	fprintf(FILE, '%f \n', temperatura(indice));

	pause(pausaEntreMediciones);									%hacer una pausa antes de la proxima medición
end
disp('Ya termino')
fclose(FILE);


fclose(interfazMultimetro);
fclose(interfazPesion);
