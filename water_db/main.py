from tkinter import *
import tkinter as tk
import pyglet
import tkinter.messagebox as MB
from PIL import Image,ImageTk
import mysql.connector as mysql


con=mysql.connect(host="localhost",user="root",password="root",database="water_management")
db=con.cursor()
bg_color="#B0B0E0"

pyglet.font.add_file("fonts/Ubuntu-Bold.ttf")
pyglet.font.add_file("fonts/Shanti-Regular.ttf")
#e_bid=Entry()
#e_pin=Entry()
#-----------------------------------functions--------------------
def clear_widgets(frame):
	# select all frame widgets and delete them
	for widget in frame.winfo_children():
		widget.destroy()

def my_show(e1,c_v1):
    if(c_v1.get()==1):
        e1.config(show='') # display the chars 
    else:
        e1.config(show='*')# hide the chars using mask

def fetching():
	db.execute("select * from wsc")
	de=db.fetchall()
	l1=[
		"SUPPLY CENTER ID(SCID) : ","AVAILABILITY OF WATER(MLD) : ","REGION : ",
		"PIPELINE LENGTH (Kms) : ","LOCATION : ","Population (Millions) : "
	]
	for info in de:
		for j in range (len(info)):

			l=Label(frame2,width=8,text=l1[j]+str(info[j]),bg="grey",font="bold")
			l.pack(side=TOP,fill=BOTH,padx=100)
#---------------------------------area_function-----------------------------------------
def fetch_area():
	while len(flist)>0:
		flist.pop().destroy()
	tf=Frame(frame2)
	table="am"
	db.execute("select * from " + table+";")
	de=db.fetchall()
	l1=[
		"PIN","NO OF BUILDING","Station Address",
		"DEMAND (MLD)","contact no.","email ID","SCID"
	]
	i=100	
	topic_frame=Frame(tf)
	for i in l1:
		l0=Label(topic_frame,width=15,text=i,font="bold",bg="black",fg="white",borderwidth=5)
		l0.pack(side=LEFT)
	topic_frame.pack(side=TOP)
	for info in de:
		row_frame=Frame(tf)
		for j in range (len(info)):
			#size=(len(str(info[j])))
			l=Label(row_frame,width=15,text=str(info[j]),font="bold",bg=bg_color,borderwidth=5)
			l.pack(side=LEFT)
		row_frame.pack(side=TOP)
	tf.pack(side=TOP)
	flist.append(tf)
#-------------------------------------build_function----------------------
def build_fetch(eb):
	while len(flist)>0:
		flist.pop().destroy()
	tf1=Frame(frame2,bg="#FFFFD3")
	if(eb.get()==""):
		MB.showinfo("Insert status","All fields are required")
	
		
	db.execute("select * from build where bid="+eb.get()+";")
	de=db.fetchall()
	status=len(de)

	if(status==0):
		MB.showinfo("ERROR","This building is not available")
	else:
		l1=[
			"BUILDING ID(BID)  :  ","PIN  :  ","No. of Houses  :  ",
			"No. of people  :  ","BUILDING NAME  :  ","Consumption (ltr)  :  ","Address  :  ","CONNECTION  :  "
		]
		i=0
		for info in de:
			row_frame=Frame(tf1,background="black")
			for j in range (len(info)):

				l=Label(tf1,width=8,text=l1[j]+str(info[j]),bg="black",fg="#FFFFD3",font="bold",border=5)
				l.pack(fill=BOTH,padx=100)
				tf1.pack(side=TOP,fill=BOTH)
			i+=1

	tf1.pack(side=TOP,fill=BOTH)
	flist.append(tf1)
#--------------------------------------own_fetch---------------------------------------
def own_fetch(bid,passwd):
	con=mysql.connect(host="localhost",user="root",password="root",database="water_management")
	db=con.cursor()
	db.execute(f"select bid,b_name,phno from owners where bid={bid} and passwd='{passwd}'")
	de=db.fetchall()
	l1=[
		"building ID(BID) :","Building Name :","Building phone no. :"
	]
	i=0
	for info in de:
		row_frame=Frame(frame4)
		for j in range (len(info)):

			l=Label(frame4,width=8,text=l1[j]+str(info[j]),bg="#FFFFD3",font="bold")
			l.pack(side=TOP,fill=BOTH)
		row_frame.pack(side=TOP)
		i+=1
#------------------------------------delete_from_building_&_owners------------------------
def del_build_own(bid):
	db.execute(f"delete from build where bid={bid}")
	con.commit()
	MB.showinfo("Delete Status","Deletion from building and owners table sucessful")
	owner_frame()
#-------------------------------------------------complain_frmae------------------------------
def comp_frame():
	def update():
		tf=Frame(frame2)
		bid=e_bid.get()
		scid=e_scid.get()
		sub=e_sub.get()
		comp=e_comp.get()
		if(bid=="" or scid=="" or sub==""  or comp==""):
			MB.showinfo("Insert status","All field are required")
		else:
			de=db.execute(f"insert into complaints values({bid},{scid},'{sub}','{comp}')")
			db.execute(de)
			con.commit()
			MB.showinfo("Insert STATUS","Insert Successfull")
			e_scid.delete(0,'end')
			e_sub.delete(0,'end')
			e_comp.delete(0,'end')		

	clear_widgets(frame4)
	frame5.tkraise()
	frame5.pack_propagate(False)
	img=Image.open("D:\water_db\water_db\ws.png")
	bgimg=ImageTk.PhotoImage(img)
	limg=Label(frame5,image=bgimg,bg="black",width=1200)
	limg.image=bgimg
	limg.pack()
	temp=Frame(frame3,bg="#FFFFD3")
	tk.Label(
		frame5, 
		text="Fill all fields given below :- ",
		fg="black",
		bg="#FFFFD3",
		font=("Ubuntu", 20),
		).pack()
	bid=Label(frame5, 
		text="BID :",
		fg="black",
		bg="#FFFFD3",
		font="bold"
		).place(x=100,y=200)
	scid=Label(frame5, 
		text="SCID:",
		fg="black",
		bg="#FFFFD3",
		font="bold"
		).place(x=100,y=250)
	sub=Label(frame5, 
		text="SUBJECT :",
		fg="black",
		bg="#FFFFD3",
		font="bold"
		).place(x=100,y=300)
	comp=Label(frame5, 
		text="Complaints:",
		fg="black",
		bg="#FFFFD3",
		font="bold"
		).place(x=100,y=350)
	
	e_bid=Entry(frame5,width=15,font=("Ubuntu", 15))
	e_bid.place(x=300,y=200)
	e_scid=Entry(frame5,width=15,font=("Ubuntu", 15))
	e_scid.place(x=300,y=250)
	e_sub=Entry(frame5,width=15,font=("Ubuntu", 15))
	e_sub.place(x=300,y=300)
	e_comp=Entry(frame5,font=("Ubuntu", 15))
	e_comp.place(x=300,y=350,width=500,height=100)
	sub=tk.Button(
		frame5,
		text="UPDATE",
		font=("Ubuntu", 18),
		bg="#28393a",
		fg="white",
		cursor="hand2",
		activebackground="#badee2",
		activeforeground="black",
		command=lambda:update(bid)
		).pack(side=BOTTOM)
	lgout=tk.Button(
		frame5,
		text="LOG OUT",
		font=("Ubuntu", 18),
		bg="#28393a",
		fg="white",
		cursor="hand2",
		activebackground="#badee2",
		activeforeground="black",
		command=lambda:owner_frame()
		).place(x=0,y=100)
#---------------------------
#-----------------------------------------update_build_owners-----------------------
def up_build_own():
	def update():
		tf=Frame(frame2)
		bid=e_bid.get()
		name=e_name.get()
		noh=e_noh.get()
		nop=e_nop.get()
		cons=e_cons.get()
		conn=e_conn.get()
		phno=e_phno.get()
		psd=e_psd.get()
		if(bid=="" or name=="" or noh==""  or nop=="" or cons=="" or conn=="" or phno==""):
			MB.showinfo("Insert status","All field are required")
		else:
			du=db.execute(f"update build set noh={noh},nop={nop},b_name='{name}',consumption={cons},conn='{conn}' where bid={bid}")
			db.execute(du)
			con.commit()

			du=db.execute(f"update owners set passwd='{psd}', b_name='{name}',phno='{phno}' where bid={bid}")
			db.execute(du)
			con.commit()
			MB.showinfo("UPDATE STATUS","update Successfull")
			e_name.delete(0,'end')
			e_noh.delete(0,'end')
			e_nop.delete(0,'end')
			e_cons.delete(0,'end')
			e_conn.delete(0,'end')
			e_phno.delete(0,'end')
			e_psd.delete(0,'end')			

	clear_widgets(frame4)
	frame5.tkraise()
	frame5.pack_propagate(False)
	img=Image.open("D:\water_db\water_db\ws.png")
	bgimg=ImageTk.PhotoImage(img)
	limg=Label(frame5,image=bgimg,bg="black",width=1200)
	limg.image=bgimg
	limg.pack()
	temp=Frame(frame3,bg="#FFFFD3")
	tk.Label(
		frame5, 
		text="Fill all fields given below :- ",
		fg="black",
		bg="#FFFFD3",
		font=("Ubuntu", 20),
		).pack()
	bid=Label(frame5, 
		text="BID :",
		fg="black",
		bg="#FFFFD3",
		font="bold"
		).place(x=100,y=200)
	name=Label(frame5, 
		text="Building Name :",
		fg="black",
		bg="#FFFFD3",
		font="bold"
		).place(x=100,y=250)
	noh=Label(frame5, 
		text="No. of Houses :",
		fg="black",
		bg="#FFFFD3",
		font="bold"
		).place(x=100,y=300)
	nop=Label(frame5, 
		text="No. of people :",
		fg="black",
		bg="#FFFFD3",
		font="bold"
		).place(x=100,y=350)
	cons=Label(frame5, 
		text="Consumption :",
		fg="black",
		bg="#FFFFD3",
		font="bold"
		).place(x=100,y=400)
	conn=Label(frame5, 
		text="Connection :",
		fg="black",
		bg="#FFFFD3",
		font="bold"
		).place(x=100,y=450)
	
	psd=Label(frame5, 
		text="Enter password :",
		fg="black",
		bg="#FFFFD3",
		font="bold"
		).place(x=500,y=200)
	phno=Label(frame5, 
		text="Building Phone no. :",
		fg="black",
		bg="#FFFFD3",
		font="bold"
		).place(x=500,y=300)
	e_bid=Entry(frame5,width=15,font=("Ubuntu", 15))
	e_bid.place(x=300,y=200)
	e_name=Entry(frame5,width=15,font=("Ubuntu", 15))
	e_name.place(x=300,y=250)
	e_noh=Entry(frame5,width=15,font=("Ubuntu", 15))
	e_noh.place(x=300,y=300)
	e_nop=Entry(frame5,width=15,font=("Ubuntu", 15))
	e_nop.place(x=300,y=350)
	e_cons=Entry(frame5,width=15,font=("Ubuntu", 15))
	e_cons.place(x=300,y=400)
	e_conn=Entry(frame5,width=15,font=("Ubuntu", 15))
	e_conn.place(x=300,y=450)
	e_phno=Entry(frame5,width=15,font=("Ubuntu", 15))
	e_phno.place(x=680,y=300)

	e_psd=Entry(frame5,width=15,font=("Ubuntu", 15),textvariable=StringVar(),show="*")
	e_psd.place(x=675,y=200)
	c_v1=IntVar(value=0)
	c1 = tk.Checkbutton(frame5,bg="#FFFFD3",font=("Ubuntu", 10),text='Show',variable=c_v1,
	onvalue=1,offvalue=0,command=lambda:my_show(e_psd,c_v1))
	c1.place(x=675,y=230)
	sub=tk.Button(
		frame5,
		text="UPDATE",
		font=("Ubuntu", 18),
		bg="#28393a",
		fg="white",
		cursor="hand2",
		activebackground="#badee2",
		activeforeground="black",
		command=lambda:update()
		).pack(side=BOTTOM)
	lgout=tk.Button(
		frame5,
		text="LOG OUT",
		font=("Ubuntu", 18),
		bg="#28393a",
		fg="white",
		cursor="hand2",
		activebackground="#badee2",
		activeforeground="black",
		command=lambda:owner_frame()
		).place(x=0,y=100)
#-------------------------------------main_frame--------------------------
def load_frame1():
	clear_widgets(frame2)
	frame1.tkraise()
	frame1.pack_propagate(False)
	img=Image.open("D:\water_db\water_db\ws.png")         #give ther directory of your image
	bgimg=ImageTk.PhotoImage(img)
	limg=Label(frame1,image=bgimg,bg="black",width=1400)
	limg.image=bgimg
	limg.pack()

	tk.Label(
		frame1,text="Get all details associated to Water Supply Management",
		bg=bg_color,fg="black",font=("TkMenuFont",20)
	).pack()

	wss=tk.Button(
		frame1,text="Water supply center",font=("Ubuntu", 18),
		bg="#28393a",
		fg="white",
		cursor="hand2",
		activebackground="#badee2",
		activeforeground="black",
		command=wss_frame
	).pack(pady=20)

	am=tk.Button(
		frame1,text="AREA MANAGEMENT",font=("Ubuntu", 18),
		bg="#28393a",
		fg="white",
		cursor="hand2",
		activebackground="#badee2",
		activeforeground="black",
		command=amm_frame
	).pack(pady=20)

	build=tk.Button(
		frame1,text="BUILDINGS",font=("Ubuntu", 18),
		bg="#28393a",
		fg="white",
		cursor="hand2",
		activebackground="#badee2",
		activeforeground="black",
		command=build_frame
	).pack(pady=20)

	own=tk.Button(
		frame1,text="Building MANGER/OWNER",font=("Ubuntu", 18),
		bg="#28393a",
		fg="white",
		cursor="hand2",
		activebackground="#badee2",
		activeforeground="black",
		command=owner_frame
	).pack(pady=20)
#---------------------------------wss_FRAME-----------------------------------------------
def wss_frame():
	clear_widgets(frame1)
	frame2.tkraise()
	frame2.pack_propagate(False)
	img=Image.open("D:\water_db\water_db\ws.png")
	bgimg=ImageTk.PhotoImage(img)
	limg=Label(frame2,image=bgimg,bg="black",width=1200)
	limg.image=bgimg
	limg.pack()
	tk.Label(
		frame2, 
		text="User cannot change anything on this page as it is supervised by\n KARANATAKA GOVT.",
		bg="#FFFFD3",fg="black",font=("Ubuntu", 20),
		).pack()
	tk.Label(frame2, text="click below to see all information",bg="#FFFFD3",fg="black",font=("Ubuntu", 10)
		).pack()
	show=tk.Button(frame2,text="RECORDS",font=("Ubuntu", 18),bg="#28393a",fg="white",cursor="hand2",
		activebackground="#badee2",activeforeground="black",command=lambda:fetching()
		).pack()
	back=tk.Button(frame2,text="BACK",font=("Ubuntu", 18),bg="#28393a",fg="white",cursor="hand2",
		activebackground="#badee2",activeforeground="black",command=lambda:load_frame1()
		).place(x=0,y=150)

#-----------------------------amm_frame---------------------------------------------
def amm_frame():
	clear_widgets(frame1)
	frame2.tkraise()
	frame2.pack_propagate(False)
	img=Image.open("D:\water_db\water_db\ws.png")
	bgimg=ImageTk.PhotoImage(img)
	limg=Label(frame2,image=bgimg,bg="black",width=1200)
	limg.image=bgimg
	limg.pack()
	tk.Label(frame2, text="User cannot change anything on this page as it is supervised by \n BBMP",fg="black",
		bg="#FFFFD3",font=("Ubuntu", 20)).pack()
	show=tk.Button(frame2,text="RECORDS",font=("Ubuntu", 18),bg="#28393a",fg="white",cursor="hand2",
		activebackground="#badee2",activeforeground="black",command=lambda:fetch_area()).pack()
	back=tk.Button(frame2,text="BACK",font=("Ubuntu", 18),bg="#28393a",fg="white",cursor="hand2",
		activebackground="#badee2",activeforeground="black",command=lambda:load_frame1()).place(x=0,y=0)
#----------------------------------build_frame----------------------------

def build_frame():

	clear_widgets(frame1)
	frame2.tkraise()
	frame2.pack_propagate(False)
	img=Image.open("D:\water_db\water_db\ws.png")
	bgimg=ImageTk.PhotoImage(img)
	limg=Label(frame2,image=bgimg,bg="black",width=1200)
	limg.image=bgimg
	limg.pack()
	tk.Label(frame2, text="Enter the building ID(BID) and PIN code of the location to get all informatioin",
		fg="black",bg="#FFFFD3",font=("Ubuntu", 20)).pack()
	bid=Label(frame2, text="BID :",fg="black",bg="#FFFFD3",font="bold").place(x=200,y=200)
	e_bid=Entry(frame2,width=15,font=("Ubuntu", 18))
	e_bid.place(x=300,y=200)
	show=tk.Button(frame2,text="GET",font=("Ubuntu", 10),bg="#28393a",fg="white",cursor="hand2",
		activebackground="#badee2",activeforeground="black",command=lambda:build_fetch(e_bid)
		).pack(side=TOP,pady=20)
	
	back=tk.Button(frame2,text="BACK",font=("Ubuntu", 18),bg="#28393a",fg="white",cursor="hand2",
		activebackground="#badee2",activeforeground="black",command=lambda:load_frame1()
		).place(x=0,y=0)
#------------------------------------login_frame-------------------------------
def log_frame(eb,ep):
	bid=eb.get()
	passwd=ep.get()
	if(bid=="" or passwd==""):
		MB.showinfo("Insert status","All fields are required")
	db.execute(f"select * from owners where bid={bid} and passwd='{passwd}';")
	status=len(db.fetchall())
	
	if(status==1):
		clear_widgets(frame2)
		frame4.tkraise()
		frame4.pack_propagate(False)
		img=Image.open("D:\water_db\water_db\ws.png")
		bgimg=ImageTk.PhotoImage(img)
		limg=Label(frame4,image=bgimg,bg="black",width=1200)
		limg.image=bgimg
		limg.pack()
		own_fetch(bid,passwd)
	else :
		MB.showinfo("ERROR","Incorrect BID or Password")
	show=tk.Button(
		frame4,
		text="COMPLAINTS",
		font=("Ubuntu", 18),
		bg="#28393a",
		fg="white",
		cursor="hand2",
		activebackground="#badee2",
		activeforeground="black",
		command=lambda:comp_frame()
		).place(x=200,y=400)
	upd=tk.Button(
		frame4,
		text="UPDATE PROFILE",
		font=("Ubuntu", 18),
		bg="#28393a",
		fg="white",
		cursor="hand2",
		activebackground="#badee2",
		activeforeground="black",
		command=lambda:up_build_own()
		).place(x=500,y=400)
	lgout=tk.Button(
		frame4,
		text="LOG OUT",
		font=("Ubuntu", 18),
		bg="#28393a",
		fg="white",
		cursor="hand2",
		activebackground="#badee2",
		activeforeground="black",
		command=lambda:owner_frame()
		).place(x=850,y=400)
	delete=tk.Button(
		frame4,
		text="DELETE MY PROFILE",
		font=("Ubuntu", 18),
		bg="#28393a",
		fg="white",
		cursor="hand2",
		activebackground="#badee2",
		activeforeground="black",
		command=lambda:del_build_own(bid)
		).pack(side=BOTTOM)

#----------------------------------reg_frame----------------------------
def reg_frame():
	def insert():
		tf=Frame(frame2)
		bd=e_bid.get()
		adr=e_adr.get()
		name=e_name.get()
		noh=e_noh.get()
		nop=e_nop.get()
		cons=e_cons.get()
		conn=e_conn.get()
		phno=e_phno.get()
		pin=e_pin.get()
		psd=e_psd.get()
		if(bd=="" or adr=="" or name=="" or noh==""  or nop=="" or cons=="" or conn=="" or phno==""):
			MB.showinfo("Insert status","All field are required")
		else:
			de=db.execute(f"insert into build values({bd},{pin},{noh},{nop},'{name}',{cons},'{adr}','{conn}')")
			db.execute(de)
			con.commit()
			du=db.execute(f"insert into owners values({bd},'{psd}','{name}','{phno}')")
			db.execute(du)
			con.commit()
			MB.showinfo("Insert status","Insert Successfull")
			e_bid.delete(0,'end')
			e_adr.delete(0,'end')
			e_name.delete(0,'end')
			e_noh.delete(0,'end')
			e_nop.delete(0,'end')
			e_cons.delete(0,'end')
			e_conn.delete(0,'end')
			e_phno.delete(0,'end')
			e_psd.delete(0,'end')
			e_pin.delete(0,'end')
			

	clear_widgets(frame2)
	clear_widgets(frame4)
	clear_widgets(frame5)
	frame3.tkraise()
	frame3.pack_propagate(False)
	img=Image.open("D:\water_db\water_db\ws.png")
	bgimg=ImageTk.PhotoImage(img)
	limg=Label(frame3,image=bgimg,bg="black",width=1200)
	limg.image=bgimg
	limg.pack()
	temp=Frame(frame3,bg="#FFFFD3")
	tk.Label(
		frame3, 
		text="Fill all fields given below :- ",
		fg="black",
		bg="#FFFFD3",
		font=("Ubuntu", 20),
		).pack()
	bid=Label(frame3, 
		text="BID :",
		fg="black",
		bg="#FFFFD3",
		font="bold"
		).place(x=100,y=200)
	adr=Label(frame3, 
		text="Address :",
		fg="black",
		bg="#FFFFD3",
		font="bold"
		).place(x=100,y=250)
	name=Label(frame3, 
		text="Building Name :",
		fg="black",
		bg="#FFFFD3",
		font="bold"
		).place(x=100,y=300)
	noh=Label(frame3, 
		text="No. of Houses :",
		fg="black",
		bg="#FFFFD3",
		font="bold"
		).place(x=100,y=350)
	nop=Label(frame3, 
		text="No. of people :",
		fg="black",
		bg="#FFFFD3",
		font="bold"
		).place(x=100,y=400)
	cons=Label(frame3, 
		text="Consumption :",
		fg="black",
		bg="#FFFFD3",
		font="bold"
		).place(x=100,y=450)
	cons=Label(frame3, 
		text="Connection :",
		fg="black",
		bg="#FFFFD3",
		font="bold"
		).place(x=100,y=500)
	conn=Label(frame3, 
		text="Connection :",
		fg="black",
		bg="#FFFFD3",
		font="bold"
		).place(x=100,y=500)
	psd=Label(frame3, 
		text="Enter password :",
		fg="black",
		bg="#FFFFD3",
		font="bold"
		).place(x=500,y=200)
	phno=Label(frame3, 
		text="Building Phone no. :",
		fg="black",
		bg="#FFFFD3",
		font="bold"
		).place(x=500,y=300)
	pin=Label(frame3, 
		text="PIN :",
		fg="black",
		bg="#FFFFD3",
		font="bold"
		).place(x=600,y=400)
	e_bid=Entry(frame3,width=15,font=("Ubuntu", 15))
	e_bid.place(x=300,y=200)
	e_adr=Entry(frame3,width=15,font=("Ubuntu", 15))
	e_adr.place(x=300,y=250)
	e_name=Entry(frame3,width=15,font=("Ubuntu", 15))
	e_name.place(x=300,y=300)
	e_noh=Entry(frame3,width=15,font=("Ubuntu", 15))
	e_noh.place(x=300,y=350)
	e_nop=Entry(frame3,width=15,font=("Ubuntu", 15))
	e_nop.place(x=300,y=400)
	e_cons=Entry(frame3,width=15,font=("Ubuntu", 15))
	e_cons.place(x=300,y=450)
	e_conn=Entry(frame3,width=15,font=("Ubuntu", 15))
	e_conn.place(x=300,y=500)
	e_phno=Entry(frame3,width=15,font=("Ubuntu", 15))
	e_phno.place(x=680,y=300)
	e_pin=Entry(frame3,width=15,font=("Ubuntu", 15))
	e_pin.place(x=680,y=400)

	e_psd=Entry(frame3,width=15,font=("Ubuntu", 15),textvariable=StringVar(),show="*")
	e_psd.place(x=675,y=200)
	c_v1=IntVar(value=0)
	c1 = tk.Checkbutton(frame3,bg="#FFFFD3",font=("Ubuntu", 10),text='Show',variable=c_v1,
	onvalue=1,offvalue=0,command=lambda:my_show(e_psd,c_v1))
	c1.place(x=675,y=230)
	sub=tk.Button(
		frame3,
		text="SUBMIT",
		font=("Ubuntu", 18),
		bg="#28393a",
		fg="white",
		cursor="hand2",
		activebackground="#badee2",
		activeforeground="black",
		command=lambda:insert()
		).pack(side=BOTTOM)
	back=tk.Button(
		frame3,
		text="BACK",
		font=("Ubuntu", 18),
		bg="#28393a",
		fg="white",
		cursor="hand2",
		activebackground="#badee2",
		activeforeground="black",
		command=lambda:owner_frame()
		).place(x=0,y=0)
	temp.pack()
#-----------------------------------owner_frame-----------------------
def owner_frame():
	clear_widgets(frame5)
	clear_widgets(frame4)
	clear_widgets(frame3)
	clear_widgets(frame1)
	frame2.tkraise()
	frame2.pack_propagate(False)
	img=Image.open("D:\water_db\water_db\ws.png")
	bgimg=ImageTk.PhotoImage(img)
	limg=Label(frame2,image=bgimg,bg="black",width=1200)
	limg.image=bgimg
	limg.pack()
	tk.Label(frame2, text="login here to go to your profile.....  ",fg="black",bg="#FFFFD3",font=("Ubuntu", 20),
		).pack()
	bid=Label(frame2, text="BID :",fg="black",bg="#FFFFD3",font="bold"
		).place(x=200,y=200)
	bid=Label(frame2, text="PASSWORD :",fg="black",bg="#FFFFD3",font="bold"
		).place(x=200,y=300)
	e_bid=Entry(frame2,width=15,font=("Ubuntu", 18))
	e_bid.place(x=400,y=200)
	e_psd=Entry(frame2,width=15,font=("Ubuntu", 18),textvariable=StringVar(),show="*")
	e_psd.place(x=400,y=300)
	c_v1=IntVar(value=0)
	c1 = tk.Checkbutton(frame2,bg="#FFFFD3",font=("Ubuntu", 10),text='Show',variable=c_v1,
	onvalue=1,offvalue=0,command=lambda:my_show(e_psd,c_v1))
	c1.place(x=610,y=300)
	show=tk.Button(frame2,text="Login",font=("Ubuntu", 14),bg="#28393a",fg="white",cursor="hand2",
		activebackground="#badee2",activeforeground="black",command=lambda:log_frame(e_bid,e_psd)
		).place(x=400,y=350)
	show=tk.Button(frame2,text="NEW REGISTRATION",font=("Ubuntu", 14),bg="#28393a",fg="white",cursor="hand2",
		activebackground="#badee2",activeforeground="black",command=lambda:reg_frame()
		).place(x=500,y=350)
	back=tk.Button(frame2,text="BACK",font=("Ubuntu", 18),bg="#28393a",fg="white",cursor="hand2",
		activebackground="#badee2",activeforeground="black",command=lambda:load_frame1()
		).place(x=0,y=0)

#------------------WINDOW--------------------------------------------
root=tk.Tk()
root.title("WATER-MANAGEMENT-SYSTEM")
#------------------------frames------------------------------------

frame1=tk.Frame(root,height=600,width=1200,bg="#B0B0E0")
frame2=tk.Frame(root,height=600,width=1200,bg="#FFFFD3")
frame3=tk.Frame(root,height=600,width=1200,bg="#FFFFD3")
frame4=tk.Frame(root,height=600,width=1200,bg="#FFFFD3")
frame5=tk.Frame(root,height=600,width=1200,bg="#FFFFD3")
flist=[]
for frame in (frame1,frame2,frame3,frame4,frame5):
	frame.grid(row=0,column=0,sticky="nesw")

#-------------------------------------------------------------------------
load_frame1()
root.resizable(False,False)
root.mainloop()