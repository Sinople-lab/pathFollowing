import math, sys, pygame, random		# 
from math import *						# 
#from pygame import *					# 
import pygame


class Rect(object):						# Clase cuyo argumento es un objeto
    def __init__(self, a, b):			# Metodo init, que inicializa el objeto y define los argumentos
        self.a = a						# Se establece el punto 'a' del objeto Rect
        self.b = b						# Se establece el punto 'b' del objeto Rect, completanto la recta

incoming= ['w','a','w','a']	# Cadena de entrada
size=[500,400]					# dimensiones de la ventana
pygame.init()					# inicia pygame
fpsClock = pygame.time.Clock()	# Variable de reloj de pygame
screen = pygame.display.set_mode(size)	# Variable de configuracion de la ventana
white = 255, 255, 255			# Blanco RGB
black = 0, 0, 0					# Negro RGB
red = 255, 0, 0					# Rojo RGB
blue = 0, 255, 0				# Azul RGB
green = 0, 0, 255				# Verde RGB
cyan = 0,180,105				# cian RGB
gray = 102,102,102				# gris rgb
maxforce=0.02					# magnitud maxima de giro
radius=15						# radio del camino
r = 4.0							# radio del robot
maxspeed=1						# Velocidad maxima en pixeles
rects=[]						# crear lista que almacenara las rectas de la ruta

def distance(p1,p2):			# funcion para caucular la distancia entre dos puntos
	v1 = [p1[0], p1[1]]			# tomar valores de entradaen v1 y v2. Tambien uso
	v2 = [p2[0], p2[1]]			# esta funcion para calcular magnitud si p1=0
	return sqrt((v2[0]-v1[0])*(v2[0]-v1[0])+(v2[1]-v1[1])*(v2[1]-v1[1]))

def dotpro(p1,p2):					# funcion para calcular el producto punto de dos vectores
	v1 = [p1[0], p1[1]]
	v2 = [p2[0], p2[1]]
	return v1[0]*v2[0]+v1[1]*v2[1]	# Producto punto

def getNormalp(p, a, b):			# funcion para obtener la proyeccion escalar
	ap = minus(p,a)					# obtener el vector a-p
	ab = minus(b,a)					# obtener el vector a-b 
	ab = scal(ab,1)					# escalar a-b a 1
	ab = scal(ab, dotpro(ap,ab))	# escalar ab a (ap)*(ab), ab-> ^u
	x = plus(a, ab)					# sumar ab al punto a para obtener la proyeccion de ap sobre ab
	return x						# devuelve el resultado

def plus(p1, p2):					# funcion para sumar dos vectores
	v1 = [p1[0], p1[1]]
	v2 = [p2[0], p2[1]]
	for i in range(2):
		v1[i] = v1[i]+v2[i]			# suma de vectores
	return v1

def minus(p1, p2):					# funcion de resta de vectores
	v1 = [p1[0], p1[1]]
	v2 = [p2[0], p2[1]]
	for i in range(2):
		v2[i] *= -1					# volver v2 negativo para...
		v1[i] += v2[i]				# sumar a v1
	return v1

def scal(p, l):						# funcion para escalar la magnitud de un vector
	v = [p[0], p[1]]
	mag = sqrt((p[0]*p[0])+(p[1]*p[1]))	# obtener la magnitud de v1
	for i in range(2):
		v[i]=(v[i]/mag)*l				# escalar v a l
	return v

def limit(p, l):						# funcion para limitar la magnitud
	v = [p[0], p[1]]
	mag = sqrt((p[0]*p[0])+(p[1]*p[1]))	# obtener la magnitud de v1
	if mag > l:							# si la magnitud es mayor a l
		for i in range(2):
 			v[i]=(v[i]/mag)*l			# escalar a l
	return v

def clean_cos(cos_angle):				# funcion para evitar argumentos invalidos para math.acos
	 return min(1,max(cos_angle,-1))	# forzar que el argumento este entre -1 y 1

def setup():
	screen.fill(black)										# fondo de la pantalla negro
	print(len(incoming))									# imprimir el total de rectas
	for i in range(len(incoming)):							# Para cada elemento de la cadena de entrada
		if i==0:											# Si se itera el primer elemento
			if incoming[i] == 'w':							# Si el primer elemento es w
				print(incoming[i])							# a *-----------* b
				a=[0,100]									# Punto inicial en la ruta
				b=[a[0]+100,a[1]]							# segundo punto de la primer recta
				rects.append(Rect(a,b))						# Agregar el par de untos como recta
				#pygame.draw.circle(screen, red, rects[i].a, 5)# dibujar circulo color rojo en la hubicacion rects[i].a, de radio 5
				#pygame.draw.circle(screen, red, rects[i].b, 5)
				
		elif i>0:											# Si ya se itero el primer elemento
			if incoming[i] =='w':							# Si el elemento actual de la cadena es w
				print(incoming[i])
				a=[rects[i-1].b[0], rects[i-1].b[1]]		# a.x=(b-1).x     a.y=(b-1).y
				b=[a[0]+100,a[1]]							# b.x=a.x + 100   b.y=a.y
				rects.append(Rect(a,b))						# Agregar la nueva recta
				#pygame.draw.circle(screen, red, rects[i].a, 5)
				#pygame.draw.circle(screen, red, rects[i].b, 5)	
 
			elif incoming[i]=='a':							# Si el elemento que se itera de la cadena es a
				print(incoming[i])
				a=[rects[i-1].b[0], rects[i-1].b[1]]		# a.x=(b-1).x   a.y=(b-1).y
				b=[a[0], a[1]+100]							# b.x=a.x     b.y=a.y+100
				rects.append(Rect(a,b))						# Agregar la nueva recta
				#pygame.draw.circle(screen, red, rects[i].a, 5)
				#pygame.draw.circle(screen, red, rects[i].b, 5)

			elif incoming[i] == 'd':
				a=[rects[i-1].b[0], rects[i-1].b[1]]		# a.x=(b-1).x   a.y=(b-1).y
				b=[a[0], a[1]-100]							# b.x=a.x     b.y=a.y+100
				rects.append(Rect(a,b))						# Agregar la nueva recta
				#pygame.draw.circle(screen, red, rects[i].a, 10)
				#pygame.draw.circle(screen, red, rects[i].b, 10)
				

def main():							# funcion principal
	position=[0, 100]				# Inicializar posicion actual
	velocity=[maxspeed, 0]			# inicializar el vector de velocidad
	k2=0							# Inicializar el control de rectas
	accel=[0,0]						# vector de asceleracion
	follow=True						# se indica que se hara el seguimiento
	setup()							# Establecer las rectas de la ruta
	for i in range(len(incoming)):	# iterar rectas
		print('Recta  '+str(i)+':    '+str(rects[i].a[0])+",  "+str(rects[i].a[1])+'    '+str(rects[i].b[0])+',  '+str(rects[i].b[1]))

	while follow:											# Seguimiento
		screen.fill(black)									# se reinicia la ventana
		for i in range(len(incoming)):							# Dibujar la ruta completa
			pygame.draw.line(screen,white,rects[i].a,rects[i].b)# dibujar la recta i
		predict = [velocity[0], velocity[1]]				# velocity.get()
		predict = scal(predict, 50)							# escalar el vector predictivo a 50 pixeles
		predpos = plus(position, predict)					# Posicion predictiva = pos + vector predictivo
		disp = [int(predpos[0]), int(predpos[1])]			# tomar la posicion predictiva truncada a enteros
		pygame.draw.circle(screen, red, disp, 5)			# dibujar un circulo en la posicion predictiva
		#print(str(predpos[0])+"    "+str(predpos[1]))
		prev = [predict[0], predict[1]]						# guardar el valor del vector predictivo			***
		if incoming[k2]=='w':										# Si se esta dirigiendo hacia el frente
			if predpos[0] > rects[k2].b[0] and k2<(len(incoming)-1):# Si la prediccion en x es mayor que b en x
				k2+=1												# Se trabajara con el siguiente segmento
		elif incoming[k2] == 'a':									# Si se esta dirigiendo hacia la derecha
			if predpos[1] > rects[k2].b[1] and k2<(len(incoming)-1):# Si la prediccion en y es mayor que b en y
				k2+=1												# Se trabajara con el siguiente segmento
		elif incoming[k2] == 'd':									# Si se esta dirigiendo hacia la izquierda
			if predpos[1] < rects[k2].b[1] and k2<(len(incoming)-1):# Si la prediccion en y es menor que b en y
				k2+=1
		
		normalp = getNormalp(predpos, rects[k2].a, rects[k2].b)		# Obtener la proyeccion de predpos sobre la recta
		disp = [int(normalp[0]), int(normalp[1])]					# tomar la posicion del vector normal truncada a enteros
		pygame.draw.circle(screen, blue, disp, 5)					# dibujar un circulo en la posicion del vector normal a la recta
		disp2 = [int(predpos[0]), int(predpos[1])]					# tomar la posicion predictiva truncada a enteros
		#print(str(normalp[0])+"    "+str(normalp[1]))				#
		pygame.draw.line(screen,white,disp, disp2)					# linea del punto normal a la posicion predictiva

		if k2 == len(incoming)-1:									# Si se esta en la ultima recta     
			target = rects[k2].b									# El objetivo sera el punto final de la ruta
			disp = [int(target[0]), int(target[1])]					# tomar la posicion del objetivo truncada a enteros
			pygame.draw.circle(screen, gray, disp, 5)				# Dibujar un circulo en la posicion objetivo actual
			#print(str(target[0])+"    "+str(target[1]))			#

		elif k2 < len(incoming)-1:									# Si no se esta iterando la recta final
			direc = minus(rects[k2].b, rects[k2].a)					# obtener la direccion de la recta actual
			direc = scal(direc,10)									# Escalar el vector de direccion a 10
			target = plus(normalp,direc)							# posicion normal + 10 pixeles sobre la recta
			disp = [int(target[0]), int(target[1])]					# tomar la posicion del objetivo truncada a enteros
			pygame.draw.circle(screen, gray, disp, 5)				# Dibujar un circulo en la posicion objetivo actual
			#print(str(target[0])+"    "+str(target[1]))			#

		lim = distance(position, rects[len(incoming)-1].b)			# medir la distancia entre position y el destino
		if	distance(predpos, normalp) > radius or lim < 50:		# Si el vec normal es mayor que el radio o la distancia con el destino...
			desired = minus(target, position)						# obtener el vector que apunta de la posicion al objetivo
			desired = scal(desired, maxspeed)						# escalar el vector de direccion deseada a la velicidad maxima
			steer = minus(desired, velocity)						# Steering = Desired - Velocity
			steer = limit(steer, maxforce)							# Limitar la magnitud del vec. steer a la fuerza de giro maxima
			accel = plus(accel, steer)								# sumar vec. de giro al vec. de accel ***
			velocity = plus(velocity, accel)						# actualiza el vector de direccion
			velocity = limit(velocity, maxspeed)					# limita la mag. del vector de direccion a la velocidad maxima
			accel = scal(accel,0)									# Reiniciar la assceleracion a 0
			if lim < 1 or lim > distance(rects[0].a, rects[3].b)+900:# Detener el seguimiento en caso de exito o fallo
				follow = False
		
		position = plus(position, velocity)							# actualiza la posicion del robot
		disp = [int(position[0]), int(position[1])]					# tomar la posicion del robot truncada a enteros
		pygame.draw.line(screen,white,disp, disp2)					# dibujar linea de la posicion actual a la posicion predictiva
		pygame.draw.circle(screen, gray, disp, 5)					# dibujar un circulo en la posicion actual
		angle = acos(clean_cos((velocity[0]*prev[0]+velocity[1]*prev[1])/(distance([0,0], velocity)*distance([0,0],prev))))
		# print('angulo: '+str(angle)+'                   '+'posicion:  '+str(position[0])+'     '+str(position[1]))
		pygame.display.update()					# Se actualiza la imagen
		fpsClock.tick(20)						# frecuencia de fotogramas por segundo
if __name__ == '__main__':						# Establece la variable name = main para el uso desde otros modulos
    main()										# Se ejecuta la funcion main