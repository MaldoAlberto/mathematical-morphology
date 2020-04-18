from Tkinter import *
from PIL import Image
from PIL import ImageTk
import tkFileDialog
import cv2
import numpy as np
import os

import argparse


root = Tk()
root.config(width=600, height=400)
root.title("Project")
root.geometry('1450x720')
spinbox = None
spinbox2 = None
spinbox3 = None
image = None
panelA = None
panelB = None
panelC = None
var = IntVar()

#sacar la desviacion estandar
def get_image_stats(img, left=0, top=0, width=0, height=0):
        crop_img = img[top:(top + height), left:(left + width)]
        (means, stds) = cv2.meanStdDev(crop_img)
        stats = np.concatenate([means, stds]).flatten()
        return stats 

#función de la erosion y dilatacion
def erosion_dilatation():
	global spinbox2, spinbox3, panelB, var
	a = int(spinbox2.get())
	b = int(spinbox3.get())

	kernel = np.ones((b,b), np.uint8)
	print var 
	if var.get() == 1: 
		kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(b,b))
	if var.get() == 2:
		kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(b,b))
	if var.get() == 3:
		kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(b,b))


	imagem = cv2.bitwise_not(image)
	img_erosion = cv2.erode(image, kernel, iterations=a) 
	img_dilation = cv2.dilate(image, kernel, iterations=a) 	
	dst2 = cv2.filter2D(image, -1, kernel)


	cv2.imshow('Erosion_'+path, img_erosion) 
	cv2.imshow('Dilation_'+path, img_dilation) 

	cv2.waitKey(0)
	cv2.destroyAllWindows()


#menu para generar la iteracion de la erocion y dilatacion
def window_erosion():
	global spinbox2,spinbox3, var
	message = "Select the iterations"
	texto = Label(root, text=message)
	texto.place(x=360, y = 30)	
	spinbox2 = Spinbox(root, from_=1, to=255)	
	spinbox2.place(x=360, y = 60)	

	var.set(1)
	texto2 = Label(root, 
		text="""EE""",
		justify = LEFT,
		padx = 20)
	texto2.place(x=360, y = 90)

	message = "Select the size"
	texto3 = Label(root, text=message)
	texto3.place(x=360, y = 120)	
	spinbox3 = Spinbox(root, from_=1, to=15)	
	spinbox3.place(x=360, y = 150)	

	r1 =Radiobutton(root, 
		      text="Square",
		      padx = 20, 
		      variable=var, 
		      value=1)#EE cuadrado
	r1.place(x=360, y = 180)
	r2 = Radiobutton(root, 
		      text="Circle",
		      padx = 20, 
		      variable=var, 
		      value=2)#EE circulo
	r2.place(x=360, y = 210)
	r3 = Radiobutton(root, 
		      text="Diamond",
		      padx = 20, 
		      variable=var, 
		      value=3)#EE diamante
	r3.place(x=360, y = 240)

	objB2 = Button(root, text="Ok", command=erosion_dilatation)
	objB2.place(x=460, y = 180)	
	

#seleccionar imagen de la computadora
def select_image():
	global panelA, path
	path = tkFileDialog.askopenfilename()


	if len(path) > 0:
		global image
		image = cv2.imread(path)

		imagec = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		imagec = Image.fromarray(imagec)
		imagec = ImageTk.PhotoImage(imagec)


		if panelA is None:

			panelA = Label(image=imagec)
			panelA.image = imagec
			panelA.pack(side="left", padx=1, pady=1)




		else:

			panelA.configure(image=imagec)
			panelA.image = imagec
		findLevel.config(state="normal")
		mor1.config(state="normal")
		mor2.config(state="normal")

#encontrar la cantidad de pixeles por nivel
def level_image():
	height = image.shape[0]
	width = image.shape[1]



	k = cv2.waitKey(0)
	if k == 27:        
	    cv2.destroyAllWindows()
	elif k == ord('s'): 
	    cv2.destroyAllWindows()




		
	i = 0

	Red = np.bincount(image[0,:][:,:][:,2])
	Red = np.pad(Red, (0, 256-len(Red)), 'constant')

	Green = np.bincount(image[0,:][:,:][:,1])
	Green = np.pad(Green, (0, 256-len(Green)), 'constant')

	Blue = np.bincount(image[0,:][:,:][:,1])
	Blue = np.pad(Blue, (0, 256-len(Blue)), 'constant')



	while i < height:
		image[i,:][:,:][:,2]

		a = np.bincount(image[i,:][:,:][:,2])
		a = np.pad(a, (0, 256-len(a)), 'constant')
		Red+=a

		b = np.bincount(image[i,:][:,:][:,1])
		b = np.pad(b, (0, 256-len(b)), 'constant')
		Green+=b

		c = np.bincount(image[i,:][:,:][:,0])
		c = np.pad(c, (0, 256-len(c)), 'constant')
		Blue+=c
		i+=1

	print(Red)
	print(Green)
	print(Blue)

        #imprimiendo los niveles
	print("Nonzero Level")
	print("Red ", np.count_nonzero(Red)," Green ", np.count_nonzero(Green)," Blue ", np.count_nonzero(Blue))

	print("Zero Level")
	print("Red ", 256-np.count_nonzero(Red)," Green ", 256-np.count_nonzero(Green)," Blue ", 256-np.count_nonzero(Blue))



	rlabel = Label(root, text="Red ",fg = "red" ).place(x = 880, y = 1) 
	glabel = Label(root, text="Green ",fg = "green" ).place(x = 950, y = 1) 
	blabel = Label(root, text="Blue ",fg = "blue" ).place(x = 1020, y = 1) 

	r = np.count_nonzero(Red)
	g = np.count_nonzero(Green)
	b = np.count_nonzero(Blue)
	nl = "    "+str(r)+"             "+ str(g) +"            "+ str(b)



	nzlevel = Label(root, text="Nonzero Level: "+nl).place(x = 760, y = 30)  
	
	r = 256-np.count_nonzero(Red)
	g = 256-np.count_nonzero(Green)
	b = 256-np.count_nonzero(Blue)
	nl = "      "+str(r)+"                 "+ str(g) +"              "+ str(b)



	zlevel = Label(root, text="Zero Level:     "+nl).place(x = 760, y = 60)  
	
	desviacion = get_image_stats(image, left=0, top=0, width=width, height=height)
	std = Label(root, text="Standard deviation : "+str(desviacion[3])+"   "+str(desviacion[4])+"   "+str(desviacion[5])).place(x = 760, y = 90)  
	

	print("levels")
	i = 0

	quote = ""
	while i < 256:
		r = Red[i]
		g = Green[i]
		b = Blue[i]
		quote += "Level "+str(i)+"\t    Red: "+ str(r)+"\t    Green: "+ str(g)+"\t    Blue: "+ str(b)+" \n"
		print(quote)
		i+=1

	#texto de los niveles de RGB
	T = Text(root, height=30, width=60)
	T.place (x=800, y = 120)
	T.insert(END, quote)


#botones de la tarea 2

newFile = Button(root, text="New File", command=select_image).place(x=30,y = 1)

findLevel = Button(root, text="Find level", command=level_image, state="disabled")
findLevel.place(x=160, y = 1)




mor1 = Button(root, text="Erosion & Dilation", command=window_erosion, state="disabled")
mor1.place(x=260, y = 1)


# generar la interfaz del canvas
root.mainloop()


