#modules generaux
import time
import threading
from random import randint
import keyboard
import socket
import globala
import traceback
import sys
import platform
import os
from tkinter import filedialog
from functools import partial

#font
import UnispaceInstaller

#tk
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

#selenium
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.command import Command
from selenium.common.exceptions import WebDriverException

#report
import smtplib
import email.message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email.message
from email.mime.base import MIMEBase
from email import encoders

#---------------------------------------
#--------------- CLASSES ---------------
#---------------------------------------
class Classe:

	def __init__(self,name="",typeClass="",date="",link="",username="",endDate=""):

		self.name = name
		self.typeClass = typeClass
		#0. Black Board Collaborate
		#1. Jitsi
		self.date = date
		self.link = link
		self.username = username
		self.endDate=endDate

#---------------------------------------
#--------- NOS PETITS THREADS ----------
#---------------------------------------
#notes: la fermeture du logiciel fermera l'instance de chrome pour éviter des restes de threads
#bon bah en fait non ca peut être utile de le garder ouvert

#autoChat Jitsi
class chaterJitsi(threading.Thread):
	
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		
		try:
			time.sleep(2)
			
			python_button = untilselector('#new-toolbox > div > div > div.toolbox-content-items > div.toolbar-button-with-badge > div')
			python_button.send_keys(Keys.RETURN)
		
			enter = untilselector("#usermsg")
			enter.send_keys(str(globala.msgMa))		
			enter.send_keys(Keys.RETURN)

			time.sleep(1)
			
			i=-1
			for msg in reversed(driver.find_elements_by_class_name('usermessage')):
				i+=1
				if msg.text == str(globala.msgMa):
					longeurAEnlever = len(driver.find_elements_by_class_name('usermessage'))-i
					print(i)
					break

			oldListeMessages = []
			nmbreYes = 0
			nmbreNo = 0
			nmbreCheck = 0
			longeurAEnlever = 0
			infinite = 1001091305162520081514
			while infinite != "":
				
				time.sleep(1)
				#pour éteindre le thread une fois fini
				try:
					root.geometry("720x480")
				except:
					infinite = ""
				
				if globala.instanceExist == True:
					#on récupere la liste des messages
					listeChat = driver.find_elements_by_class_name('usermessage')
					
					#si il y a un nouveau message:
					if oldListeMessages != listeChat:
						nmbreNo = 0
						nmbreYes = 0
						#on prend tous les messages
						for msg in listeChat[longeurAEnlever:]:
							if msg.text == "oui" or msg.text == "Oui" or msg.text == "OUI" or msg.text == "ui" or msg.text == "yes" :
								if nmbreYes == 0:
									nmbreCheck = 0
								nmbreYes += 1

							if msg.text == "non" or msg.text == "Nui" or msg.text == "Non" or msg.text == "NON" or msg.text == "no":	
								if nmbreNo == 0:
									nmbreCheck = 0
								nmbreNo += 1
						
						if (nmbreNo == 2 or nmbreYes == 2)and nmbreCheck < 10:
							enterd = driver.find_element_by_id('usermsg')
							if nmbreYes == 2:
								enterd.send_keys("Oui")
							if nmbreNo == 2:
								enterd.send_keys("Non")
							enterd.send_keys(Keys.RETURN)
							#on patiente 60 secondes avant de recommencer a checker (for and timesleep de 1 pour fermer rapidement le thread)
							for k in range(60):
								time.sleep(1)
								try:
									root.geometry("720x480")
								except:
									infinite = ""
									print("this is the end")
									break
							longeurAEnlever = len(listeChat)
							nmbreCheck = 0
							nmbreYes = -1
							nmbreNo = -1
							longeurAEnlever += len(driver.find_elements_by_class_name('usermessage'))-len(listeChat)



					else:
						nmbreCheck+=1

					if nmbreCheck > 10:
						nmbreYes = 0
						nmbreNo = 0
						nmbreCheck = 0
						longeurAEnlever = len(driver.find_elements_by_class_name('usermessage'))

					if globala.modDev == 1:
						print(nmbreYes)
						print(nmbreNo)
					time.sleep(1)
					oldListeMessages = listeChat
		except Exception as error:
			report(error)
		print("Auto-Chat: Closed")

#autoChat Jitsi
class chaterCned(threading.Thread):
	
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		try:
			enterd = driver.find_element_by_xpath('/html/body')
			for nmhtg in range(2):
				enterd.send_keys(Keys.TAB)
			keyboard.press_and_release('enter')
			time.sleep(1)

			infinite = 1001091305162520081514
			while infinite != "":
				try:
					enterdMsg = driver.find_element_by_xpath('//*[@id="chat-input-container"]/bb-chat-input-rich-text-editor/div/div/div[1]/div/div[1]')
					enterdMsg.send_keys(str(globala.msgMa))
					enterdMsg.send_keys(Keys.RETURN)
					infinite = ""
					time.sleep(1)
				except:
					pass
			time.sleep(1)

			oldListeMessages = []
			nmbreYes = 0
			nmbreNo = 0
			nmbreCheck = 0
			nmbreYR = 2
			nmbreNR = 2
			infinite = 1001091305162520081514
			longeurAEnlever=0
			nmbreMsgY = 0
			nmbreMsgN = 0
			while infinite != "":
				time.sleep(1)
				#pour éteindre le thread une fois fini
				try:
					root.geometry("720x480")
				except:
					infinite = ""

				print(nmbreYes)
				print(nmbreNo)
				print(nmbreYR)
				print(nmbreNR)

				if globala.instanceExist == True:
					#on récupere la liste des messages
					listeChat = driver.find_elements_by_xpath('//*[@id="chat-channel-history"]')
					#si il y a un nouveau message:

					nmbreNo = 0
					nmbreYes = 0

					listeStrY = ["oui","Oui","OUI","yes","YES","Yes","yep"]
					for stry in listeStrY:
						nmbreYes += listeChat[0].text.count(stry)

					listeStrN = ["non","Non","NON","nan"]
					for strn in listeStrN:
						nmbreNo += listeChat[0].text.count(strn)
					
					#on prend tous les messages
					if (nmbreNo == nmbreNR or nmbreYes == nmbreYR):
						
						rep = ""
						enterdMsg = driver.find_element_by_xpath('//*[@id="chat-input-container"]/bb-chat-input-rich-text-editor/div/div/div[1]/div/div[1]')
						if nmbreYes == nmbreYR:
							enterdMsg.send_keys("Oui")
							nmbreYR=0
							nmbreYR += 2
							rep = 1
						if nmbreNo == nmbreNR:
							enterdMsg.send_keys("Non")
							nmbreNR=0
							nmbreNR += 2
							rep = 0
						enterdMsg.send_keys(Keys.RETURN)
					
						#on patiente 60 secondes avant de recommencer a checker (for and timesleep de 1 pour fermer rapidement le thread)
						for k in range(60):
							time.sleep(1)
							try:
								root.geometry("720x480")
							except:
								infinite = ""
								print("this is the end")
								break
						

						for stry in listeStrY:
							nmbreYR += listeChat[0].text.count(stry)

						for strn in listeStrN:
							nmbreNR += listeChat[0].text.count(strn)
						
						if nmbreNR == 0:
							nmbreNR = 2
						if nmbreYR == 0:
							nmbreYR = 2
					

					time.sleep(1)
					oldListeMessages = listeChat
		except Exception as error:
			report(error)
		print("Auto-Chat: Closed")

#gere la classe virtuelle
class adminVisio(threading.Thread):
	
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self,classe):
		if globala.iprint.get() == 1: #output dev mode
			print("Admin visio: Connecting")
			print(classe.typeClass)
		connect(classe)

		print("Admin Visio: closed")

#checker de classes virtuelles
class classChecker(threading.Thread):
	
	def __init__(self): 
		threading.Thread.__init__(self) 

	def run(self):
		
		time.sleep(3) #10 secondes pour éviter des erreurs si l'assignement des valeurs est pas encore bon
		print("Class Checker: Start...")
		while globala.closeThread == False:
			
			checkDate()

			print("Class Checker: Check effectué")
			for i in range (60):
				time.sleep(1)
				if globala.closeThread == True:
					break
				try: #si l'utilisateur a fermé comme un bourrin on tente de provoquer une erreur pour arreter
					root.configure(bg='white')
				except:
					globala.closeThread = True
		print("Checker: closed")


class chromeChecker(threading.Thread):
	
	def __init__(self): 
		threading.Thread.__init__(self)  

	def run(self):
		
		time.sleep(3) #10 secondes pour éviter des erreurs si l'assignement des valeurs est pas encore bon
		print('ChromeChecker: starting...')
		while globala.closeThread == False:
			try:#si l'utilisateur a fermé le navigateur
				driver.title
				if globala.iprint.get() == 1:
					print("Chrome existe")
				globala.instanceExist = True

			except:
				globala.instanceExist = False
				try:
					driver.quit()
				except:
					pass
			time.sleep(1)
			if globala.iprint.get() == 1: #output dev mode
				print(globala.instanceExist)
				print("ChromeChecker: Check effectué")

		print("ChromeChecker: closed...")

#---------------------------------------
#------------- FONCTIONS ---------------
#---------------------------------------

#pour augmenter les perfs on fait une fonction pour chaque maniere de localisation
def untilxpath(xpath,delay=1):
	infinite = 1001091305162520081514
	while infinite != "":
		try:
			element = driver.find_element_by_xpath(xpath)		
			infinite = ""
			time.sleep(delay)
		except Exception as e:
			print(e)
	return(element)

def untilselector(selector,delay=1):
	infinite = 1001091305162520081514
	while infinite != "":
		try:
			element = driver.find_element_by_css_selector(selector)		
			infinite = ""
			time.sleep(delay)
		except Exception as e:
			print(e)
	return(element)

def saveConfig():
	configFile = open("data/config.cfg", "w")
	configFile.write(str(int(globala.geoVar.get())))
	configFile.write(str(int(globala.microVar.get())))
	configFile.write(str(int(globala.cameraVar.get())))
	configFile.write(str(int(globala.autoChatVar.get())))
	configFile.write(str(1))
	configFile.write(str(int(globala.explorer.get())))
	configFile.write(str(int(globala.modDev)))
	configFile.write(str(int(globala.iprint.get())))
	configFile.write(str(int(globala.afkRecorder.get())))
	configFile.write(str("\n"+str(globala.directory)))
	configFile.close()

def connect(classe):

	try:
		if globala.iprint.get() == 1: #output dev mode
			print(globala.explorer.get())
		global driver
		if globala.explorer.get() == 1: #Chrome
			opt = Options()
			opt.add_argument("--disable-infobars")
			opt.add_argument("start-maximized")
			opt.add_argument("--disable-extensions")
			opt.add_argument("--use-fake-ui-for-media-stream")
			opt.add_argument("-disable-user-media-security=true")
			
			if classe.typeClass == 0:
				opt.add_experimental_option("prefs", { \
				    "profile.default_content_setting_values.media_stream_mic": 1, 
				    "profile.default_content_setting_values.media_stream_camera": globala.microVar.get(),
				    "profile.default_content_setting_values.geolocation": globala.geoVar.get(), 
				    "profile.default_content_setting_values.notifications": 0,
				  })
			else:
				opt.add_experimental_option("prefs", { \
				    "profile.default_content_setting_values.media_stream_mic": globala.cameraVar.get(), 
				    "profile.default_content_setting_values.media_stream_camera": globala.microVar.get(),
				    "profile.default_content_setting_values.geolocation": globala.geoVar.get(), 
				    "profile.default_content_setting_values.notifications": 0
				  })
			driver = webdriver.Chrome(options=opt,executable_path='ressources/chromedriver.exe')
		
		if globala.explorer.get() == 2: #Firefox
			opt = FirefoxOptions()
			opt.set_preference("media.navigator.permission.disabled", True)
			driver = webdriver.Firefox(options=opt,executable_path='ressources/geckodriver.exe')
		
		driver.implicitly_wait(30)
		driver.get(classe.link)
		if classe.typeClass == 1:
			connectJitsi(classe)
				
		if classe.typeClass == 0:
			connectCned(classe)

	except Exception as error:
		report(error)

def connectJitsi(classe):
	# Appeler l’application web
	enter = driver.find_element_by_class_name('field')
	enter.send_keys(classe.username)
	enter.send_keys(Keys.RETURN)

def connectCned(classe):
	
	try:
		# Appeler l’application web
		enter = driver.find_element_by_id('username')
		enter.send_keys(globala.userId)
		time.sleep(1)
		enter = driver.find_element_by_id('password')
		enter.send_keys(globala.userMdp)
		time.sleep(1)
		enter = driver.find_element_by_xpath('/html/body/div/div[2]/form/input[5]')
		enter.send_keys(Keys.RETURN)



		enter = untilselector('#root > div > div > div > div > div > div > div > div:nth-child(3) > a > button')
		enter.send_keys(Keys.RETURN)   
 
		infinite = 1001091305162520081514
		while infinite != "":
			try:	
				enter = driver.find_element_by_xpath('//*[@id="dialog-description-audio"]/div[2]/button')
				infinite = ""
				enter.send_keys(Keys.RETURN)
				time.sleep(1)
				enter = ""
			except Exception as e:
				print(e)
			try:	
				enter = driver.find_element_by_xpath('//*[@id="dialog-description-audio"]/div[3]/button') 
				infinite = ""
				enter.send_keys(Keys.RETURN)
				time.sleep(1)
				enter = ""
			except Exception as e:
				print(e)

		if globala.explorer.get() == 1:
			
			enter = untilxpath('//*[@id="techcheck-video-ok-button"]')
			enter.send_keys(Keys.RETURN)

			enter = untilxpath('//*[@id="announcement-modal-page-wrap"]/div/div[4]/button')
			enter.send_keys(Keys.RETURN)

			enter = untilxpath('//*[@id="exit-tutorial"]')
			enter.send_keys(Keys.RETURN)

		elif globala.explorer.get() == 2:
			print("on utilise firefox")
			
			enter = untilxpath('/html/body/div[4]/div/button')
			enter.send_keys(Keys.RETURN)

			enter = untilxpath('/html/body/div[1]/div[2]/div/div/button')
			enter.send_keys(Keys.RETURN)

		enter = untilxpath('//*[@id="side-panel-open"]')
		enter.send_keys(Keys.RETURN)

	except Exception as error:
		report(error)

#---------- GESTION DES IDENTIFIANTS --------------
def Ids(userIdR="none",userMdpR="nonemdp"):

	global userId
	userId = userIdR
	global userMdp
	userMdp = userMdpR

#sauvegarde des identifiants
def crypt(mode=0,cle=" ",entree=" "):
	
	sortie, i = "", 0
	for caract in entree:	#parcours de la chaîne à traiter
		if mode == 0:	#chiffrement
			sortie = sortie + chr((ord(caract) + ord(cle[i])) % 256)
			i = i + 1	#parcours de la clé
			if i > len(cle) - 1:
				i = 0	#fin de clé atteinte, on repart au début
		elif mode == 1:	#déchiffrement
			sortie = sortie + chr((ord(caract) - ord(cle[i])) % 256)
			i = i + 1
			if i > len(cle) - 1:
				i = 0
	return sortie

def generateKey():
	listeChar="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMPNOPQRSTUVWXYZ!\"#$%&\'()*+,-./:;<=>?@0123456789"
	key = ""
	for i in range(512):
		key = key + listeChar[randint(0,len(listeChar)-1)]

	with open('data/key.afkc','w') as file:
		file.write(key)
		
	return()

def giveMeKey():
	key = ""
	with open('data/key.afkc','r') as file:
		key = file.read()
	return key

#---------- MAIN ----------
#fenetre principal: GUI title bar, menus, menu gauche + variables essentielles 
def main(connectedR,listeClassesRecieved,configData):
	
	global connected
	connected = connectedR
	checkClass = classChecker()  #crée le thread
	checkClass.start()#on demarre le thread

	checkChrome = chromeChecker()  #crée le thread
	checkChrome.start()
	"""global closeThread
				closeThread = False
				global listeClasses
				listeClasses = """

	#reglages fenetre globale
	global root
	root = tk.Tk()
	root.geometry("720x480")
	root.title('AFK Class')
	root.iconbitmap('ressources/icon.ico')
	root.iconbitmap(default="ressources/icon.ico")
	root.resizable(width=False, height=False)
	root.configure(bg='white')

	globala.geoVar = tk.IntVar()
	globala.microVar = tk.IntVar()
	globala.cameraVar = tk.IntVar()
	globala.autoChatVar = tk.IntVar()
	globala.explorer = tk.IntVar()
	globala.iprint = tk.IntVar()
	globala.afkRecorder = tk.IntVar()

	globala.cameraVar.set(configData[0])
	globala.microVar.set(configData[1])
	globala.geoVar.set(configData[2])
	globala.autoChatVar.set(configData[3])
	globala.explorer.set(configData[5])
	globala.iprint.set(configData[7])
	globala.afkRecorder.set(configData[8])

	#reglages du menu en haut
	global menubar
	menubar = tk.Menu(root)

	menu1 = tk.Menu(menubar, tearoff=0)
	menu1.add_command(label="Contact", command=reportWindows,font=("Unispace", 8))
	menu1.add_command(label="A propos", command=showMore,font=("Unispace", 8))
	menu1.add_command(label="Quitter", command=exitAFK,font=("Unispace", 8))
	menubar.add_cascade(label="Général",font=("Unispace", 8),menu=menu1)


	menuConnection = tk.Menu(menubar, tearoff = 0)
	
	menuConnection.add_checkbutton(label="Caméra",font=("Unispace", 8), onvalue=1, offvalue=0, variable=globala.cameraVar)
	menuConnection.add_checkbutton(label="Microphone",font=("Unispace", 8), onvalue=1, offvalue=0, variable=globala.microVar)
	menuConnection.add_checkbutton(label="Géolocalisation",font=("Unispace", 8), onvalue=1, offvalue=0, variable=globala.geoVar)
	menuConnection.add_separator()
	menuConnection.add_checkbutton(label="Chrome",font=("Unispace", 8), onvalue=1, offvalue=0, variable=globala.explorer)
	menuConnection.add_checkbutton(label="Firefox",font=("Unispace", 8), onvalue=2, offvalue=0, variable=globala.explorer)
	menubar.add_cascade(label="Paramètres", menu=menuConnection,font=("Unispace", 8))
	
	menuAFKChat = tk.Menu(menubar, tearoff = 0)
	menuAFKChat.add_checkbutton(label="AFK Chat",font=("Unispace", 8), onvalue=1, offvalue=0, variable=globala.autoChatVar)
	menuAFKChat.add_command(label="Message d'arrivée",font=("Unispace", 8), command=editMA)
	menuAFKChat.add_command(label="Message de fin",font=("Unispace", 8), command=editME)
	menubar.add_cascade(label="AFK Chat", menu=menuAFKChat,font=("Unispace", 8))
	
	"""
	menuAFKRecorder = tk.Menu(menubar, tearoff = 0)
	menuAFKRecorder.add_checkbutton(label="AFK Recorder",font=("Unispace", 8), onvalue=1, offvalue=0, variable=globala.autoChatVar)
	menuAFKRecorder.add_command(label="Configurer",font=("Unispace", 8), command=afkRecorder)
	menubar.add_cascade(label="AFK Recorder", menu=menuAFKRecorder,font=("Unispace", 8))
	"""
	menuID = tk.Menu(menubar, tearoff=0)
	menuID.add_command(label="Gerer mes identifiants", command=manageMyIDs,font=("Unispace", 8))
	menubar.add_cascade(label="Identifiants", menu=menuID,font=("Unispace", 8))
	
	menu3 = tk.Menu(menubar, tearoff=0)
	
	menu3.add_command(label="Tutoriel", command=starter,font=("Unispace", 8))
	menu3.add_command(label="Infos", command=showinfo,font=("Unispace", 8))
	
	menubar.add_cascade(label="Aide", menu=menu3,font=("Unispace", 8))
	
	if globala.modDev == 1:
		global menuDev
		menuDev = tk.Menu(menubar, tearoff=0)

		menuDev.add_command(label="Jitsi DevC Time", command=partial(newClass,name="Jitsi Dev Class",typeClass=1,link="https://meet.jit.si/DevAFKClass",date=str(time.strftime('%d'))+"/"+str(time.strftime('%m'))+"/"+str(time.strftime('%Y'))+"-"+str(time.strftime('%H'))+"."+str(int(time.strftime('%M'))),endDate=str(time.strftime('%d'))+"/"+str(time.strftime('%m'))+"/"+str(time.strftime('%Y'))+"-"+str(time.strftime('%H'))+"."+str(int(time.strftime('%M'))+10)))
		menuDev.add_command(label="Cned DevC Time", command=partial(newClass,name="Cned Dev Class",typeClass=0,link="https://lycee.cned.fr/cv/230251/497",date=str(time.strftime('%d'))+"/"+str(time.strftime('%m'))+"/"+str(time.strftime('%Y'))+"-"+str(time.strftime('%H'))+"."+str(int(time.strftime('%M'))),endDate=str(time.strftime('%d'))+"/"+str(time.strftime('%m'))+"/"+str(time.strftime('%Y'))+"-"+str(time.strftime('%H'))+"."+str(int(time.strftime('%M'))+10)))
		
		menuDev.add_command(label="Force connect", command=forceConnect)
		menuDev.add_command(label="Quit DevMode", command=quitDevMode)
		menuDev.add_checkbutton(label="IPrint", onvalue=1, offvalue=0, variable=globala.iprint)
		menubar.add_cascade(label="Dev Mode", menu=menuDev)

	root.config(menu=menubar)

	#----- Creation de l'espace principal -----
	
	#creation de la fenetre top
	global frame
	frame = tk.Frame(root)
	frame.configure(bg='white')
	
	#logo connection
	if connected == 0:
		imgConnection = tk.PhotoImage(file="ressources/connection0.png")
		textConnection = "! Non connecté !"
		imageConnection = tk.Label(frame, image=imgConnection,font=("Unispace", 10))
	if connected == 1:
		imgConnection = tk.PhotoImage(file="ressources/connection1.png")
		textConnection = "Connecté"	
		imageConnection = tk.Label(frame, image=imgConnection)
	imageConnection.configure(bg='white')
	imageConnection.grid(column=0,row=0,sticky='nw')
	

	labelConnection = tk.Label(frame,text=textConnection,font=("Unispace", 10))
	labelConnection.grid(column=0,row=1,sticky='nw')
	labelConnection.configure(bg='white')
	

	title = tk.Label(frame, text = "\nAFK Class          ",font=("Unispace", 16))
	title.configure(bg='white')
	title.grid(column=1,row=0,ipadx=50,sticky="nw")
	
	imgLogo = tk.PhotoImage(file="ressources/icon.png")
	imageLogo = tk.Label(frame, image=imgLogo)
	imageLogo.configure(bg='white')
	imageLogo.grid(column=3,row=0,)
	
	if connected == 0:
		imgSeparator = tk.PhotoImage(file="ressources/separator0.png")
	else:
		imgSeparator = tk.PhotoImage(file="ressources/separator.png")
	imageSeparator = tk.Label(frame, image=imgSeparator,borderwidth=0,padx=5)
	imageSeparator.configure(bg='white')
	imageSeparator.grid(columnspan=4,row=2)

	#frame bottom
	global frameBottom
	frameBottom = tk.Frame(frame)
	frameBottom.configure(bg="white")
	frameBottom.grid(column=0,row=3)

	titleListe = tk.Label(frameBottom, text = "Classes virtuelles:",font=("Unispace", 10))
	titleListe.configure(bg='white')
	titleListe.grid(column=0,row=0,sticky="w")

	if connected == 0:
		imgVSeparator = tk.PhotoImage(file="ressources/verticalseparator0.png")
	else:
		imgVSeparator = tk.PhotoImage(file="ressources/verticalseparator.png")
	imageVSeparator = tk.Label(frameBottom, image=imgVSeparator,borderwidth=0,padx=5)
	imageVSeparator.configure(bg='white')
	imageVSeparator.grid(column=2,row=0,rowspan=4,sticky="w")

	setGUIListeClass()

	guiListeClasses.grid(column=0,columnspan=2,row=1,sticky="w")

	modifyClassButton=tk.Button(frameBottom, text="Modifier",font=("Unispace", 10),relief="groove",command=modifyClass)
	modifyClassButton.grid(column=0,row=2,sticky="w")

	deleteClassButton=tk.Button(frameBottom, text="Supprimer",font=("Unispace", 10),relief="groove",command=deleteClass)
	deleteClassButton.grid(column=1,row=2,sticky="w")

	newClassButton=tk.Button(frameBottom, text="  Nouvelle Classe Virtuelle  ",font=("Unispace", 10),relief="groove",command=newClass)
	newClassButton.grid(column=0,row=3,columnspan = 2,sticky="w")

	#frame right
	global frameRight
	frameRight = tk.Frame(frame)
	frameRight.configure(bg="white")
	frameRight.grid(column=1,row=3)
	
	saveConfig()
	
	frame.pack()
	root.mainloop()

def afkRecorder():
	
	global recordRoot
	recordRoot = tk.Toplevel()
	recordRoot.geometry("480x360")
	recordRoot.resizable(width=False, height=False)
	recordRoot.title('Contact')
	recordRoot.iconbitmap('ressources/icon.ico')
	
	global frame
	frame = tk.Frame(recordRoot)

	title = tk.Label(frame, text = "AFK Recorder\n",font=("Unispace", 14))
	title.grid(row=0,sticky="n")

	corps = tk.Label(frame, text = "AFK Recorder vous permet d'enregistrer\nvos classes virtuelles en format video.\n\nPlus d'excuses: Vous pouvez voir et revoir\nvos classes virtuelles quand vous le souhaitez !",font=("Unispace", 8))
	corps.grid(row=1,sticky="n")

	directory = tk.Label(frame, text = str("\nDossier d'exportation vidéo:\n"+str(globala.directory)+"\n"),font=("Unispace", 8))
	directory.grid(row=2,sticky="n")

	sendButton=tk.Button(frame, text="Selectionner un dossier",font=("Unispace", 10),relief="groove",command=selectDirectory,padx=4)
	sendButton.grid(row=3)

	frame.pack()
	#filedialog.askdirectory()

def selectDirectory():
	globala.directory = filedialog.askdirectory() 
	directory = tk.Label(frame, text = str("                                                                        \n                                                                    "),font=("Unispace", 8))
	directory.grid(row=2,sticky="n") 
	directory = tk.Label(frame, text = str("\nDossier d'exportation vidéo:\n"+str(globala.directory)+"\n"),font=("Unispace", 8))
	directory.grid(row=2,sticky="n")
	saveConfig()

#fenetre report
def reportWindows():

	global contact
	contact = tk.Toplevel()
	contact.geometry("480x360")
	contact.resizable(width=False, height=False)
	contact.title('Contact')
	contact.iconbitmap('ressources/icon.ico')
	
	global frameMsg
	frameMsg = tk.Frame(contact)
	
	title = tk.Label(frameMsg, text = "AFK Virtual Class\n\n",font=("Unispace", 10))
	title.grid(row=0,sticky="n")
	title = tk.Label(frameMsg, text = "AFK Class ne peut évoluer sans vous !\nVotre avis, vos reports de bugs sont plus qu'essentiels.",font=("Unispace", 10))
	title.grid(row=1,sticky="n")
	global msgContent
	messageContent = ""
	global inputMsg
	inputMsg = tk.Text(frameMsg,font=("Unispace", 8),width=65,height=12)
	inputMsg.insert(1.0,"Saisissez votre message:")
	inputMsg.grid(row=2)

	title = tk.Label(frameMsg, text = "\n",font=("Unispace", 10))
	title.grid(row=3,sticky="n")
	
	sendButton=tk.Button(frameMsg, text="Envoyer",font=("Unispace", 10),relief="groove",command=sendReport,padx=4)
	sendButton.grid(row=4)
	
	frameMsg.pack()
	contact.mainloop()

def editMA():

	global editMATK
	global inputMsgMA
	global frameMsgMa


	editMATK = tk.Toplevel()
	editMATK.geometry("300x120")
	editMATK.resizable(width=False, height=False)
	editMATK.title("Message d'arrivée")
	editMATK.iconbitmap('ressources/icon.ico')
	
	frameMsgMa = tk.Frame(editMATK)
	
	title = tk.Label(frameMsgMa, text = "Modifiez votre message automatique\n d'arrivé en classe virtuelle:",font=("Unispace", 8))
	title.grid(row=0,sticky="n")
	
	
	inputMsgMA = tk.Text(frameMsgMa,font=("Unispace", 8),width=40,height=2)
	
	#on gere l'insertion
	try:
		file = open("data/saveMsgA.txt",'r')
		inputMsgMA.insert(1.0,file.read()[:-1])
		file.close()
	except:
		inputMsgMA.insert(1.0,"Saisissez votre message:")

	inputMsgMA.grid(row=1)

	title = tk.Label(frameMsgMa, text = "\n",font=("Unispace", 4))
	title.grid(row=3,sticky="n")
	
	sendButton=tk.Button(frameMsgMa, text="Enregistrer",font=("Unispace", 8),relief="groove",command=saveMsgMA,padx=4)
	sendButton.grid(row=4)
	
	frameMsgMa.pack()
	editMATK.mainloop()

def editME():

	global editMETK
	global inputMsgME
	global frameMsgME


	editMETK = tk.Toplevel()
	editMETK.geometry("300x120")
	editMETK.resizable(width=False, height=False)
	editMETK.title("Message d'arrivée")
	editMETK.iconbitmap('ressources/icon.ico')
	
	frameMsgME = tk.Frame(editMETK)
	
	title = tk.Label(frameMsgME, text = "Modifiez votre message automatique\n de fin de classe virtuelle:",font=("Unispace", 8))
	title.grid(row=0,sticky="n")
	
	inputMsgME = tk.Text(frameMsgME,font=("Unispace", 8),width=40,height=2)
	
	#on gere l'insertion
	try:
		file = open("data/saveMsgE.txt",'r')
		inputMsgME.insert(1.0,file.read()[:-1])
		file.close()
	except:
		inputMsgME.insert(1.0,"Saisissez votre message:")

	inputMsgME.grid(row=1)

	title = tk.Label(frameMsgME, text = "\n",font=("Unispace", 4))
	title.grid(row=3,sticky="n")
	
	sendButton=tk.Button(frameMsgME, text="Enregistrer",font=("Unispace", 8),relief="groove",command=saveMsgME,padx=4)
	sendButton.grid(row=4)
	
	frameMsgME.pack()
	editMETK.mainloop()

def saveMsgMA():
	file = open("data/saveMsgA.txt",'w')
	file.write(inputMsgMA.get(1.0, tk.END))
	file.close()
	editMATK.destroy()

def saveMsgME():
	file = open("data/saveMsgE.txt",'w')
	file.write(inputMsgME.get(1.0, tk.END))
	file.close()
	editMETK.destroy()

def sendReport():
	
	try: 
		result.grid_forget()
	except:
		pass

	try:
		expmail = "sender.afkclass@gmail.com"
		mdp= 'Ilovepython3'
		destmail = "contact.afkclass@gmail.com"
		objet = "Report d'utilisateur"
		content = inputMsg.get(1.0, tk.END)
		message=content.replace('<br>','n')

		msg = MIMEMultipart()

		"""msg.add_header('Content-Type','text/html')
					msg.set_payload('{}'.format(contenu,))"""

		s = smtplib.SMTP('smtp.gmail.com',587)

		s.starttls()
		text = MIMEText(content, 'plain', 'utf-8')
		msg.attach(text)
		
		part = MIMEBase('application', 'octet-stream')
		part.set_payload(open('data/log.txt', 'rb').read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename("log.txt"))
		msg.attach(part)

		s.login(expmail,mdp)

		s.sendmail(expmail, destmail, msg.as_string())

		s.quit()
		result = tk.Label(frameMsg, text = "Message envoyé",font=("Unispace", 10),activeforeground="green",fg='green')
		result.grid(row=5)

	except Exception as e:
		result = tk.Label(frameMsg, text = "Message non envoyé...\nVérifiez votre connexion...",font=("Unispace", 10),activeforeground="red",fg="red")
		result.grid(row=5)
		report(e)

#fenetre infos
def showMore():

	global showMore
	showMore = tk.Toplevel()
	showMore.geometry("480x360")
	showMore.resizable(width=False, height=False)
	showMore.title('A propos')
	showMore.iconbitmap('ressources/icon.ico')
	
	frame = tk.Frame(showMore)
	
	title = tk.Label(frame, text = "AFK Class 2.2",font=("Unispace", 12))
	title.grid(row=0)

	info = tk.Label(frame, text = "\n\nAway From Keyboard Class\n\n\n\nDéveloppé par Maliro Beacrupte\n\n\n\nUn grand philosophe a dit:\n\n\"Allez en cours quand même.\"\n\n\n\n\n\n\nafkclass.wixsite.com/accueil\nAFK Class - 2021 - Tous droits reservés. ",font=("Unispace", 10,"italic"))
	info.grid(row=2)
	frame.pack()
	showMore.mainloop()

#fenetre infos
def showinfo():

	showinfo = tk.Toplevel()
	showinfo.geometry("710x450")
	showinfo.resizable(width=False, height=False)
	showinfo.title('A propos')
	showinfo.iconbitmap('ressources/icon.ico')
	
	frame = tk.Frame(showinfo)
	
	img = ImageTk.PhotoImage(Image.open("ressources/infos.png"))
	image = tk.Label(frame, image=img)
	image.configure(bg="white")
	image.photo = img
	image.grid(column=0,row=0,sticky="n")
	frame.pack()
	showinfo.mainloop()

#fenetre de gestion des identifiants: UI + variables
def manageMyIDs():

	global idsWindows
	idsWindows = tk.Toplevel()
	idsWindows.geometry("480x360")
	idsWindows.title('Identifiants')
	idsWindows.resizable(width=False, height=False)
	idsWindows.iconbitmap('ressources/iconSettings.ico')
	idsWindows.configure(bg="white")

	Ids()
	loadIds()

	frameIDs = tk.Frame(idsWindows)
	frameIDs.configure(bg="white")

	title = tk.Label(frameIDs, text = "Mes identifiants\n\n\n",font=("Unispace", 14),bg='white')
	title.grid(column=0,columnspan=3,row=0,sticky="n")

	titleId = tk.Label(frameIDs, text = "  Identifiant:  ",font=("Unispace", 12),bg='white')
	titleId.grid(column=0,row=1,sticky="w")

	titleMdp = tk.Label(frameIDs, text = "  Mot de passe:",font=("Unispace", 12),bg='white')
	titleMdp.grid(column=0,row=2,sticky="w")

	global inputId
	global inputMdp

	inputId = tk.Entry(frameIDs,textvariable=globala.userId,width=28,font=("Unispace", 8))
	inputId.delete(0,len(inputId.get()))
	inputId.insert(0,str(globala.userId))
	inputId.grid(column=1,row=1,sticky="w")

	inputMdp = tk.Entry(frameIDs,textvariable=globala.userMdp,width=28,font=("Unispace", 8),show='*')
	inputMdp.delete(0,len(inputMdp.get()))
	inputMdp.insert(0,str(globala.userMdp))
	inputMdp.grid(column=1,row=2,sticky="w")

	txtIds = tk.Label(frameIDs, text = "\n\nCertains services de visioconférences nécéssite une identification.\nDans le but de toujours garder une compatibilité maximum\nvous pouvez remplir vos identifiants de connexion.\nConserver une parfaite confidentialité et sécurité sur vos données reste une priorité.\nCelles-ci sont donc cryptées à l'aide de Crpyto Python et à l'aide d'une clé unique\n et ne sont stockées que sur votre ordinateur.\n\n",font=("Unispace", 6),bg='white')
	txtIds.grid(column=0,columnspan=3,row=3,sticky="n")

	saveIDsButton=tk.Button(frameIDs, text="Sauvegarder",font=("Unispace", 10),relief="groove",command=saveIds,padx=4)
	saveIDsButton.grid(column=0,columnspan=3,row=4)

	txtNeed = tk.Label(frameIDs, text = "\n          Services supportés nécéssitant une identification:        \nBlackBoard Collaborate (CNED)",font=("Unispace", 8),bg='white')
	txtNeed.grid(column=0,columnspan=3,row=5,sticky="n")
	
	frameIDs.pack()

def loadIds():
	
	with open('data/id.id', 'r',encoding="Latin-1") as file:
		idCrypted = file.read()

	with open('data/mdp.mdp', 'r',encoding="Latin-1") as file:
		mdpCrypted = file.read()

	globala.userId = crypt(mode=1,cle=giveMeKey(),entree=str(idCrypted))
	globala.userMdp = crypt(mode=1,cle=giveMeKey(),entree=str(mdpCrypted))

def saveIds():
	
	globala.userId = inputId.get()
	globala.userMdp = inputMdp.get()
	
	mdpCrypted = crypt(mode=0,cle=giveMeKey(),entree=globala.userMdp)
	idCrypted = crypt(mode=0,cle=giveMeKey(),entree=globala.userId)

	with open('data/id.id', 'w',encoding="Latin-1") as file:
		file.write(idCrypted)

	with open('data/mdp.mdp', 'w',encoding="Latin-1") as file:
		file.write(mdpCrypted)

	idsWindows.destroy()

#exit AFK quoi
def exitAFK():
	closeThread = True
	saveConfig()
	try:
		saveClass()
	except:
		pass
	print(closeThread)
	try:
		idsWindows.destroy()
	except:
		pass
	try:
		showinfo.destroy()
	except:
		pass
	try:
		editMATK.destroy()
	except:
		pass
	try:
		contact.destroy()
	except:
		pass
	root.destroy()
	print("End of all")

#creer une nouvelle classe puis fait appelle pour modifier directement
def newClass(name="Nouvelle classe virtuelle",typeClass=1,date=str(time.strftime('%d'))+"/"+str(time.strftime('%m'))+"/"+str(time.strftime('%Y'))+"-12.00",link="https://meet.jit.si/AFKClassExample",username="Personne en or ;)",endDate=str(time.strftime('%d'))+"/"+str(time.strftime('%m'))+"/"+str(time.strftime('%Y'))+"-23.59"):

	setGUIListeClass()
	listeClasses.append(Classe(name=name,typeClass=typeClass,date=date,link=link,username=username,endDate=endDate))
	guiListeClasses.insert(len(listeClasses)-1,listeClasses[len(listeClasses)-1].name)
	guiListeClasses.selection_clear(0,len(listeClasses)-1)
	guiListeClasses.selection_set(len(listeClasses)-1)
	modifyClass()
	fileSaveUpdate()

#suprrime une classe
def deleteClass():
	if len(guiListeClasses.curselection()) == 1:
		del listeClasses[guiListeClasses.curselection()[0]]
		guiListeClasses.delete(guiListeClasses.curselection())
		
		guiListeClasses.selection_clear(0,len(listeClasses)-1)
		guiListeClasses.selection_set(len(listeClasses)-1)
		
		for element in frameRight.winfo_children():
			element.destroy()
	fileSaveUpdate()

#sauvegarde d'une classe
def saveClass():
	
	listeClasses[cursorset].name = inputName.get()
	i = -1
	for value in listeValue:
		i+=1
		if value == inputType.get():
			listeClasses[cursorset].typeClass = i
	listeClasses[cursorset].date = inputDate.get()
	listeClasses[cursorset].link = inputLink.get()
	listeClasses[cursorset].username = inputPseudo.get()
	listeClasses[cursorset].endDate = inputDateEnd.get()
	
	global savedCursor
	savedCursor = guiListeClasses.curselection()
	savedLabel = tk.Label(frameRight, text = "Sauvegardé !",font=("Unispace", 10,"bold"),bg='white',activeforeground="green",fg='green')
	savedLabel.grid(column=0,row=16,sticky="w")

	savedCursor = guiListeClasses.curselection()
	global menuDev
	if listeClasses[cursorset].name == "DevPass":
		savedLabel = tk.Label(frameRight, text = "Dev Mode Activé !",font=("Unispace", 13,"bold"),bg='white',activeforeground="green",fg='dark orange1')
		globala.modDev = 1
		try: #pour verifier si il est pas déjà activer
			menuDev.destroy()
		except:
			if globala.modDev == 1:
				menuDev = tk.Menu(menubar, tearoff=0)
				menuDev.add_command(label="Class Time", command=addClassDev)
				menuDev.add_command(label="Force connect", command=forceConnect)
				menuDev.add_command(label="Quit DevMode", command=quitDevMode)
				menubar.add_cascade(label="Dev Mode", menu=menuDev)

	else:
		savedLabel = tk.Label(frameRight, text = "Pensez à vérifiez\nles identifiants si besoin !",font=("Unispace", 9,"bold"),bg='white',activeforeground="green",fg='green')
	savedLabel.grid(column=1,row=15,columnspan=2,rowspan=2,sticky="w")
	
	setGUIListeClass()
	fileSaveUpdate()
		
#update les sauvegardes
def fileSaveUpdate():
	data = open("data/data.sav", "w")
	for SVC in listeClasses:
		data.write("|"+str(SVC.name)+"|"+str(SVC.typeClass)+"|"+str(SVC.date)+"|"+str(SVC.link)+"|"+str(SVC.username)+"|"+str(SVC.endDate)+"|\n")
	data.close()

#fonction pour modifier une classe: GUI frameRight + gestion classe
def modifyClass():

	if len(guiListeClasses.curselection()) == 1:
		#on s'occupe de la partie de droite
		global cursorset
		cursorset = guiListeClasses.curselection()[0]
		global listeValue
		listeValue = ["BlackBoard Collaborate","Jitsi Meet"]

		savedLabel = tk.Label(frameRight, text = "                        \n                    ",font=("Unispace", 10,),bg='white',activeforeground="green")
		savedLabel.grid(column=1,row=15,rowspan = 2,sticky="w")
		
		titleClasse = tk.Label(frameRight, text = "Classe virtuelle:\n",font=("Unispace", 12),bg='white')
		titleClasse.grid(column=0,row=0,sticky="n")
		space = tk.Label(frameRight, text = "none",bg='white',fg="white",font=("Unispace", 1))
		space.grid(column=0,row=1,sticky="w")

		titleName = tk.Label(frameRight, text = "Nom:",font=("Unispace", 10),bg='white')
		titleName.grid(column=0,row=4,sticky="w")

		global inputName
		inputName = tk.Entry(frameRight,textvariable=listeClasses[guiListeClasses.curselection()[0]].name,width=28,font=("Unispace", 8))
		inputName.delete(0,len(inputName.get()))
		inputName.insert(0,listeClasses[guiListeClasses.curselection()[0]].name)
		inputName.grid(column=1,row=4)

		space = tk.Label(frameRight, text = "none",bg='white',fg="white")
		space.grid(column=0,row=5,sticky="w")

		titleType = tk.Label(frameRight, text = "Type:",font=("Unispace", 10),bg='white')
		titleType.grid(column=0,row=6,sticky="w")

		global inputType
		inputType = ttk.Combobox(frameRight,values=["BlackBoard Collaborate","Jitsi Meet"],font=("Unispace", 9),width=24)
		inputType.set(listeValue[int(listeClasses[guiListeClasses.curselection()[0]].typeClass)])
		inputType.grid(column=1,row=6,sticky="w")
		
		space = tk.Label(frameRight, text = "none",bg='white',fg="white")
		space.grid(column=0,row=7,sticky="w")

		titleDate = tk.Label(frameRight, text = "Date:",font=("Unispace", 10),bg='white')
		titleDate.grid(column=0,row=8,sticky="w")

		global inputDate
		inputDate = tk.Entry(frameRight,textvariable=listeClasses[guiListeClasses.curselection()[0]].date,width=28,font=("Unispace", 8))
		inputDate.delete(0,len(inputDate.get()))
		inputDate.insert(0,listeClasses[guiListeClasses.curselection()[0]].date)
		inputDate.grid(column=1,row=8)

		space = tk.Label(frameRight, text = "none",bg='white',fg="white")
		space.grid(column=0,row=9,sticky="w")

		titleLink = tk.Label(frameRight, text = "Lien:",font=("Unispace", 10),bg='white')
		titleLink.grid(column=0,row=10,sticky="w")

		global inputLink
		inputLink = tk.Entry(frameRight,textvariable=listeClasses[guiListeClasses.curselection()[0]].link,width=28,font=("Unispace", 8))
		inputLink.delete(0,len(inputLink.get()))
		inputLink.insert(0,listeClasses[guiListeClasses.curselection()[0]].link)
		inputLink.grid(column=1,row=10)

		space = tk.Label(frameRight, text = "none",bg='white',fg="white")
		space.grid(column=0,row=11,sticky="w")

		titlePseudo = tk.Label(frameRight, text = "Pseudo de connexion:",font=("Unispace", 10),bg='white')
		titlePseudo.grid(column=0,row=12,sticky="w")

		global inputPseudo
		inputPseudo = tk.Entry(frameRight,textvariable=listeClasses[guiListeClasses.curselection()[0]].username,width=28,font=("Unispace", 8))
		inputPseudo.delete(0,len(inputPseudo.get()))
		inputPseudo.insert(0,listeClasses[guiListeClasses.curselection()[0]].username)
		inputPseudo.grid(column=1,row=12)

		space = tk.Label(frameRight, text = "none",bg='white',fg="white")
		space.grid(column=0,row=13,sticky="w")
		
		titlePseudo = tk.Label(frameRight, text = "Date de fin:",font=("Unispace", 10),bg='white')
		titlePseudo.grid(column=0,row=14,sticky="w")

		global inputDateEnd
		inputDateEnd = tk.Entry(frameRight,textvariable=listeClasses[guiListeClasses.curselection()[0]].endDate,width=28,font=("Unispace", 8))
		inputDateEnd.delete(0,len(inputDateEnd.get()))
		inputDateEnd.insert(0,listeClasses[guiListeClasses.curselection()[0]].endDate)
		inputDateEnd.grid(column=1,row=14)

		"""space = tk.Label(frameRight, text = "none",bg='white',fg="white")
								space.grid(column=0,row=13,sticky="w")"""

		saveClassButton=tk.Button(frameRight, text="Sauvegarder",font=("Unispace", 10),relief="groove",command=saveClass,padx=4)
		saveClassButton.grid(column=0,row=15,sticky="w")

#on creer la liste déroulante des classes
def setGUIListeClass():
	
	global guiListeClasses
	
	if connected == 1:
		guiListeClasses = tk.Listbox(frameBottom,width = 30, height = 14,font=("Unispace", 10),relief="groove",bd=3,bg="white",selectmode="single",exportselection=0,selectbackground='green',activestyle='none')
	else:
		guiListeClasses = tk.Listbox(frameBottom,width = 30, height = 14,font=("Unispace", 10),relief="groove",bd=3,bg="white",selectmode="single",exportselection=0,selectbackground='red',activestyle='none')

	guiListeClasses.delete(0,len(listeClasses))
	for virtualClass in listeClasses:
		guiListeClasses.insert(listeClasses.index(virtualClass)+1,virtualClass.name)
	guiListeClasses.grid(column=0,columnspan=2,row=1,sticky="w")
	try:
		guiListeClasses.selection_set(savedCursor[0])
	except:
		pass

def checkDate():
	
	for classe in listeClasses:
		
		#checkDate
		if globala.instanceExist == False:
			if str(time.strftime('%d')) == classe.date[:2] and str(time.strftime('%m')) == classe.date[3:5] and str(time.strftime('%H')) == classe.date[11:13] and str(time.strftime('%M')) == classe.date[-2:] and str(time.strftime('%Y')) == classe.date[6:10]:
				

				file = open("data/saveMsgA.txt","r")
				msgMa = str(file.read())
				file.close()
				#on demarre un thread de connection
				print("Class Checker: démarrage de la classe virtuelle")
				Ids()
				globala.instanceExist = True
				loadIds()
				adminVisioThread = adminVisio()
				adminVisioThread.run(classe)
				#si auto chat est activé:
				time.sleep(15) #1 minute de
				if globala.autoChatVar.get() == 1 and classe.typeClass == 1:
					chater = chaterJitsi()  #crée le thread
					chater.start()

				#si auto chat est activé:
				if globala.autoChatVar.get() == 1 and classe.typeClass == 0:
					chater = chaterCned()  #crée le thread
					chater.start()
		
		if str(time.strftime('%d')) == classe.endDate[:2] and str(time.strftime('%m')) == classe.endDate[3:5] and str(time.strftime('%H')) == classe.endDate[11:13] and str(time.strftime('%M')) == classe.endDate[-2:] and str(time.strftime('%Y')) == classe.endDate[6:10]:
			
			quitClass(classe)

def quitClass(classe):
	
	if globala.autoChatVar.get() == 1:
		if classe.typeClass == 1: #rappel 1 Jitsi
			enterd = driver.find_element_by_id('usermsg')				
			enterd.send_keys(globala.msgMe)
		if classe.typeClass == 0:
			enterdMsg = driver.find_element_by_xpath('//*[@id="chat-input-container"]/bb-chat-input-rich-text-editor/div/div/div[1]/div/div[1]')
			enterdMsg.send_keys(str(globala.msgMe))
	try:
		driver.close()
		driver.quit()
	except:
		print("error")		
	globala.instanceExist = False


#-------------- Mode Developpeur (code = DevPass) ----------------
#a qui lira ca: le mode developpeur est déconseillé: il utilise 30% du CPU ! jsp pourquoi... xD (fin surtout l'appli devient inutilisable quoi...)
#bon en fait c'est que dans certaines situations ?
#Plus serieusement: Le modDev provoque un ralentissement de root pendant la durée de connectX:
#cf bug tracker --> fix pour v2.1 --> FIXé

def forceConnect():
	checkDate()

def report(exception=""):
	
	try:
		file = open('data/log.txt','r')
		file.close()
		if exception != "":
			with open('data/log.txt','a') as file:
				file.write("\n\n----------\nReport:\nDate: "+str(time.strftime('%d'))+"/"+str(time.strftime('%m'))+"/"+str(time.strftime('%Y'))+"-"+str(time.strftime('%H'))+"."+str(int(time.strftime('%M')))
				+"\nException Class: "+str(sys.exc_info()[0])+"\nException: "+str(exception)+"\n-------------\n"+str(traceback.format_exc()+"-------------\n"))

	except:
		with open('data/log.txt','w') as file:
			file.write("----------- Log AFK Class ----------\n\nInstall Date: "+str(time.strftime('%d'))+"/"+str(time.strftime('%m'))+"/"+str(time.strftime('%Y'))+"-"+str(time.strftime('%H'))+"."+str(int(time.strftime('%M')))+"\nWindows: "+
				str(sys.getwindowsversion()[0])+"."+str(sys.getwindowsversion()[2])
				+"\nPlateforme: "+str(sys.getwindowsversion()[3])+"\nCPU: "+str(platform.processor()))

def quitDevMode():
	globala.modDev = 0
	menuDev.destroy()
	root.config(menu=menubar)

#---------------- Fonctions premier démarrage -----------------
def nextStart(numPageReceive):
	
	global numPage
	numPage = numPageReceive+1

	if numPage == 0:
		
		frameTitleStart = tk.Frame(frameStart)
		frameTitleStart.configure(bg=rgbtohex(r=153,g=217,b=234))
		labelTitleStart = tk.Label(frameTitleStart,text="     Bienvenue sur AFK Class !",font=("Unispace", 18))
		labelTitleStart.grid(column=1,row=0,sticky='n')
		labelTitleStart.configure(bg=rgbtohex(r=153,g=217,b=234))
		
		labelTitleStart = tk.Label(frameTitleStart,text="     Away From Keyboard Class",font=("Unispace", 12,"italic"))
		labelTitleStart.grid(column=1,row=1,sticky='n')
		labelTitleStart.configure(bg=rgbtohex(r=153,g=217,b=234))
		
		imgLogo = tk.PhotoImage(file="ressources/starticon.png")
		imageLogo = tk.Label(frameTitleStart, image=imgLogo)
		imageLogo.configure(bg=rgbtohex(r=153,g=217,b=234))
		imageLogo.grid(column=0,row=0,rowspan=2,sticky="w")
		
		frameTitleStart.grid(column=0,row=0)
		labelTextStart = tk.Label(frameStart,text="\n\n\n\n\n\nAFK Class est un logiciel conçu pour\nfaciliter les réunions ou cours en distanciels.\nProgrammez une classe virtuelle, sauvegardez et partez vous détendre !\n\n\n\n\n\n\n\n\n\n\n",font=("Unispace", 12))
		labelTextStart.grid(column=0,row=2,columnspan=2,sticky='n')
		labelTextStart.configure(bg=rgbtohex(r=153,g=217,b=234))


	if numPage == 1:
		img = ImageTk.PhotoImage(Image.open("ressources/pageConnection.png"))
		
	if numPage == 2:
		img = ImageTk.PhotoImage(Image.open("ressources/pageVCs.png"))

	if numPage == 3:
		img = ImageTk.PhotoImage(Image.open("ressources/pageEdit.png"))

	if numPage == 4:
		img = ImageTk.PhotoImage(Image.open("ressources/pageMenu.png"))
		
	if numPage == 5:
		img = ImageTk.PhotoImage(Image.open("ressources/pageIds.png"))
	if numPage == 6:
		img = ImageTk.PhotoImage(Image.open("ressources/pageAutoChat.png"))

	if numPage == 8:
		img = ImageTk.PhotoImage(Image.open("ressources/pageEnd.png"))
	
	if numPage == 7:
		img = ImageTk.PhotoImage(Image.open("ressources/pageContact.png"))

	if numPage > 0 and numPage < 9:
		image = tk.Label(frameStart, image=img)
		image.configure(bg=rgbtohex(r=153,g=217,b=234))
		image.photo = img
		image.grid(column=0,columnspan=2,row=0,rowspan=3,sticky="w")

	if numPage != 8:
		nextButton=tk.Button(frameStart, text="Suivant",font=("Unispace", 10),relief="groove",bd=3,command=nextStartCall,highlightcolor=rgbtohex(r=153,g=217,b=234))
		nextButton.grid(column=1,row=3,sticky="e")

		passButton=tk.Button(frameStart, text="Passer le tutoriel",font=("Unispace", 10),relief="groove",bd=3,command=passStart,highlightcolor=rgbtohex(r=153,g=217,b=234))
		passButton.grid(column=0,row=3,sticky="w")

	else:
		nextButton=tk.Button(frameStart, text="Utiliser AFK Class",font=("Unispace", 10),relief="groove",bd=3,command=nextStartCall,highlightcolor=rgbtohex(r=153,g=217,b=234))
		nextButton.grid(column=1,row=3,sticky="e")
	
	if numPage == 9 or numPage == -1:
		starterTk.destroy()
		

	if numPage != 9 and numPage != -1:
		frameStart.pack()
		starterTk.mainloop()
		
	return(numPage)

def nextStartCall():
	nextStart(numPage)	

def starter(connected="",listeClasses="",configData=[1,1,1,1,1]):
	
	global connectedF
	connectedF = connected
	global listeClassesF
	listeClassesF = listeClasses
	global configDataF
	configDataF = configData
	global starterTk

	if configData[4]==1:
		starterTk = tk.Toplevel()
	else:
		starterTk = tk.Tk()
	starterTk.geometry("720x490")
	starterTk.title('AFK Class')
	starterTk.iconbitmap('ressources/starticon.ico')
	starterTk.resizable(width=False, height=False)
	starterTk.configure(bg=rgbtohex(r=153,g=217,b=234))
	
	global frameStart
	frameStart = tk.Frame(starterTk)
	frameStart.configure(bg=rgbtohex(r=153,g=217,b=234))
	nextStart(-1)

def passStart():
	nextStart(-2)

def rgbtohex(r,g,b):
    return f'#{r:02x}{g:02x}{b:02x}'

#------------------------------------
#-------- DEBUT DU PROGRAMME --------
#------------------------------------

#------------------------------------
#-------- Variables globales --------
#------------------------------------

try:
	UnispaceInstaller.install("ressources/unispace bd.ttf")
except:
	pass

report()

globala.bgdfh()

connected = False 
listeClasses = []
configData = [0,0,0,0,0,0,0,0,0,0]
idData = ["Identifiant","Mot de passe"]

try:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(("www.google.com", 80))
	connected = 1
	sock.close()
except:
	pass

try:
	msgfile = open("data/saveMsgA.txt","r")
	globala.msgMa = msgfile.read()
	msgfile.close()
	msgfile = open("data/saveMsgE.txt","r")
	globala.msgMe = msgfile.read()
	msgfile.close()
except Exception as error:
	report(error)
	globala.msgMa = ""
	globala.msgMe = ""

try: 
	#au cas ou si fichier sup ou fichier corrompu
	#chargement des SVC
	data = open("data/data.sav", "r")
	dataLines = data.readlines()
	data.close()

	i=-1
	for line in dataLines:
		i+=1
		nmbreAcc=0
		instanceID = -1
		listeClasses.append(Classe())
		temp = ""
		for char in line:
			if nmbreAcc == 1 and char != "|":
				temp = temp + str(char)

			if char == "|" and nmbreAcc == 1:
				nmbreAcc-=1
				if instanceID == 0:
					listeClasses[i].name = temp
				if instanceID == 1:
					listeClasses[i].typeClass = int(temp)
				if instanceID == 2:
					listeClasses[i].date = temp
				if instanceID == 3:
					listeClasses[i].link = temp
				if instanceID == 4:
					listeClasses[i].username = temp
				if instanceID == 5:
					listeClasses[i].endDate = temp
				temp = ""
			
			if char == "|" and nmbreAcc == 0:
				nmbreAcc+=1
				instanceID +=1

	#chargement des configs
	configFile = open("data/config.cfg", "r")
	configFileData = configFile.readlines()
	
	configData[0] = configFileData[0][0] #cam
	configData[1] = configFileData[0][1] #mic
	configData[2] = configFileData[0][2] #geo
	configData[3] = configFileData[0][3] #autochat
	configData[4] = configFileData[0][4] #new user
	configData[5] = configFileData[0][5] #explorer
	configData[6] = configFileData[0][6] #devmode
	configData[7] = configFileData[0][7] #iprint
	configData[8] = configFileData[0][8] #AFK Recorder
	configData[9] = configFileData[1] #directory
	configFile.close()

except Exception as error:
	report(error)

Ids(idData[0],idData[1])

globala.closeThread = False
globala.modDev = int(configData[6])
globala.instanceExist = False
globala.directory = configData[9]


if configData[4] != "1":
	configData[4] = "1"
	try:
		expmail = "sender.afkclass@gmail.com"
		mdp= 'Ilovepython3'
		destmail = "contact.afkclass@gmail.com"
		objet = "Report d'utilisateur"
		content = "Nouvel utilisateur"
		message=content.replace('<br>','n')
		msg = MIMEMultipart()
		s = smtplib.SMTP('smtp.gmail.com',587)
		s.starttls()
		text = MIMEText(content, 'plain', 'utf-8')
		msg.attach(text)
		s.login(expmail,mdp)
		s.sendmail(expmail, destmail, msg.as_string())
		s.quit()
	except Exception as error:
		report(error)
	generateKey()
	starter(connected,listeClasses,configData)
	main(connected,listeClasses,configData)

else:
	#on creer la fenètre principale
	try:
		giveMeKey()
	except:
		generateKey()
	main(connected,listeClasses,configData)