#importing libraries
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import math
import random
import socket
import matplotlib.pyplot as plt
import datetime
saved_data=[]

#function to create room
def create(room):
    app = Ursina()

    window.fps_counter.enabled = False
    window.exit_button.visible = False

       
    #function to append values to file
    def append_to_file(pos):
            with open(room, "a") as myfile:
                myfile.write(pos)

    #to extract coordinates from a Vec3 Vector
    def refine_vec_data(vec):
        edit1=vec[5:]
        edit2=edit1[:-1]
        edit3=edit2.split(",")
        x_co=edit3[0].strip()
        y_co=edit3[1].strip()
        z_co=edit3[2].strip()
        return x_co,y_co,z_co

    #class to drop entities
    class Voxel(Button):
        def __init__(self, position = (0,0,0),Brick_color=color.white):
            super().__init__(
                parent = scene,
                position = position,
                model = 'cube',
                origin_y = 0.5,
                texture = 'white_cube',
                color = Brick_color)


        #function to check for mouse input, drop more bricks
        def input(self,key):

            #position to be entered into file

            if self.hovered:
                if key=='left mouse down':
                    #if left key pressed drop brick set to brown
                    voxel=Voxel(position=self.position+mouse.normal,Brick_color=color.brown)
                    new_position=str(self.position+mouse.normal)
                    x_co,y_co,z_co=refine_vec_data(new_position)
                    append_to_file(x_co+","+y_co+","+z_co+",brown\n")
                
                #if right clicked delete them
                if key=='right mouse down':
                    #delete brick
                    destroy(self)

                    count=0
                    data=[]

                    #receive data from file
                    file=open(room,'r')
                    for lines in file:
                        data.append(lines)
                        count+=1

                    #empty file
                    with open(room, "w") as myfile:
                        myfile.write("")

                    #append new data
                    for i in range(0,count-1):
                        append_to_file(data[i])


    #creating ground, -1 to whatever to not end up stuck
    for z in range(-1,19):
        #first wall
        for y in range(5):
            voxel = Voxel(position = (-1,y,z),Brick_color=color.brown)
            pos="-1,+"+str(y)+","+str(z)
            append_to_file(pos+",brown\n")


        for x in range(-1,19):
            #second wall
            for y in range(5):
                voxel = Voxel(position = (x,y,-1),Brick_color=color.brown)
                pos=str(x)+","+str(y)+",-1"
                append_to_file(pos+",brown\n")

            voxel = Voxel(position = (x,0,z),Brick_color=color.white)
            pos=str(x)+",0,"+str(z)
            append_to_file(pos+",white\n")

            voxel = Voxel(position = (x,5,z),Brick_color=color.brown)
            pos=str(x)+",5,"+str(z)
            append_to_file(pos+",brown\n")

            for y in range(5):
                voxel = Voxel(position = (x,y,19),Brick_color=color.brown)
                pos=str(x)+","+str(y)+",19"
                append_to_file(pos+",brown\n")

        for y in range(5):
            voxel = Voxel(position = (19,y,z),Brick_color=color.brown)
            pos="19,+"+str(y)+","+str(z)
            append_to_file(pos+",brown\n")

    player = FirstPersonController()

    app.run()

data_from_file=[]

#function to load existing room
def load(room,c,x,z):
    app = Ursina()

    #receive data from file for if color is not selected
    global data_from_file
    file=open(room,'r')
    for lines in file:
        refined=lines.split(",")
        refined[0]=refined[0].strip()
        refined[1]=refined[1].strip()
        refined[2]=refined[2].strip()
        refined[3]=refined[3].strip()
        data_from_file.append(refined)

    #color code number as parameter
    col=c
    #window.fullscreen = True
    window.fps_counter.enabled = False
    window.exit_button.visible = False

    def append_to_file(pos):
        with open(room, "a") as myfile:
            myfile.write(pos)

    #to extract coordinates from a Vec3 Vector
    def refine_vec_data(vec):
        edit1=vec[5:]
        edit2=edit1[:-1]
        edit3=edit2.split(",")
        first=edit3[0].strip()
        second=edit3[1].strip()
        third=edit3[2].strip()
        return first,second,third

    #to update color in file
    def change_color(x,y,z,color):
            count=0
            data=[]

            #receive data from file
            file=open(room,'r')
            for lines in file:
                data.append(lines)
                count+=1

            #empty file
            with open(room, "w") as myfile:
                myfile.write("")

            #append new data
            for i in range(0,count):
                d=data[i].split(",")

                if int(d[0])==int(x) and int(d[1])==int(y) and int(d[2])==int(z):
                    
                    append_to_file(x+","+y+","+z+","+color)
                else:
                    append_to_file(data[i])

    
    def display_msg(msg):
            print_on_screen(msg,position=window.top_left,origin=(-.5,.5),scale=2,duration=0.6)

    def display_status(col,radiation):
        if col!=1 or col!=2 or col!=3:
            position=str(player.position)
            x,y,z=refine_vec_data(position)
            msg="You are away from Radiation "+str(radiation)+" usv"
            for i in data_from_file:
                #print(round(float(x)),y,z)
                #print(i[0],i[1],i[2])
                if int(i[0])==round(float(x)) and int(i[1])==round(float(y)) and int(i[2])==round(float(z)) and str(i[3])=="green":
                    msg="You are away from Radiation "+str(radiation)+" usv"
                elif int(i[0])==round(float(x)) and int(i[1])==round(float(y)) and int(i[2])==round(float(z)) and str(i[3])=="yellow":
                    msg="You are getting closer to Radiation! "+str(radiation)+" usv"
                elif int(i[0])==round(float(x)) and int(i[1])==round(float(y)) and int(i[2])==round(float(z)) and str(i[3])=="red":
                    msg="You are being exposed to too much Radiation! "+str(radiation)+" usv"
            display_msg(msg)

    def display_radiation(col):
        if col!=1 or col!=2 or col!=3:
            position=str(player.position)
            x,y,z=refine_vec_data(position)
            first_t=(13-float(x))**2
            second_t=(9-float(z))**2
            distance=math.sqrt(first_t+second_t)
            radiation=1/distance
            radiation=round(radiation,8)

            #if random.randint(1,1000)==150:
                #save data to file
                #with open("data_"+room, "a") as myfile:
                    #currentDT = datetime.datetime.now()
                    #time_passed=int(currentDT.second)-initial_time
                    #myfile.write(x+","+y+","+z+","+str(radiation)+","+str(currentDT.second)+"\n")

            return radiation

    def send(col,value,port):
        if col!=1 or col!=2 or col!=3:
            sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            value=str(value)
            length=len(value)
            if (length<25):
                reamining=10-length
                for i in range (0,reamining):
                    value+=" "
                byte_msg=bytes(value,"utf-8")
                sock.sendto(byte_msg,("127.0.0.1",port))

    def distance(x,z):
        first_t=(13-float(x))**2
        second_t=(9-float(z))**2
        distance=math.sqrt(first_t+second_t)
        return distance

    
    def draw_path(col,x,z):
        if col!=1 or col!=2 or col!=3:
            init_x=x
            init_z=z
            x=int(x)
            z=int(z)

            walls=[]
            file=open("walls"+room,'r')
            for lines in file:
                x_co,y_co,z_co=refine_vec_data(lines)
                temp_list=[]
                temp_list.append(int(str(x_co)))
                temp_list.append(int(str(y_co)))
                temp_list.append(int(str(z_co.strip(")"))))
                walls.append(temp_list)

            initial_distance=distance(init_x,init_z)
            on_the_way=True
            global saved_data
            file=open(room,'r')
            for lines in file:
                saved_data.append(lines)

            x_and_z=[]
            while (on_the_way):
                print("Working...")
                d1=distance(int(x)+1,z)
                d2=distance(x,int(z)+1)
                if d1<initial_distance:
                    if (x+1,0,z) not in walls:
                        x_and_z.append((x+1,z))
                        x=x+1
                elif d2<initial_distance:
                    if (x,0,z+1) not in walls:
                        x_and_z.append((x,z+1))
                        z=z+1
                elif init_x==x and init_z==z:
                    on_the_way=False

            for i in x_and_z:
                change_color(x,0,z,"white")
                tim.sleep(0.5)


    #run before anything
    #draw_path(col,x,z)

    #calss to change color, equipped with entites in case needed to edit, uncomment codes below
    class Voxel(Button):
        def __init__(self, position = (0,0,0),Brick_color=color.white):
            super().__init__(
                parent = scene,
                position = position,
                model = 'cube',
                origin_y = 0.5,
                texture = 'white_cube',
                color = Brick_color)
            


        def input(self,key):
            #position to be entered into file
            
            radiation=display_radiation(col)

            #sending data
            if random.randint(1,30)==15:
                send(col,radiation,8888)
                send(col,int(time.time()),8889)
                pass

            if self.hovered:

                display_status(col,radiation)

                if key=='left mouse down':
                    #voxel=Voxel(position=self.position+mouse.normal,Brick_color=color.brown)
                    #pos=self.position+mouse.normal
                    #append_f(str(self.position+mouse.normal)[5]+","+str(self.position+mouse.normal)[8]+","+str(self.position+mouse.normal)[11]+",brown\n")

                    #appending walls
                    #with open("walls"+room, "a") as myfile:
                     #   myfile.write(str(self.position))

                    if col==1:     #red-danger
                        voxel=mouse.hovered_entity
                        voxel.color=color.red
                        pos=str(self.position)
                        x_co,y_co,z_co=refine_vec_data(pos)
                        change_color(x_co,y_co,z_co,"red\n")

                    if col==2:      #green-safe
                        voxel=mouse.hovered_entity
                        voxel.color=color.green
                        pos=str(self.position)
                        x_co,y_co,z_co=refine_vec_data(pos)
                        change_color(x_co,y_co,z_co,"green\n")
                    
                    if col==3:     #yellow-medium
                        voxel=mouse.hovered_entity
                        voxel.color=color.yellow
                        pos=str(self.position)
                        x_co,y_co,z_co=refine_vec_data(pos)
                        change_color(x_co,y_co,z_co,"yellow\n")
                    #draw a temp path
                    if col==4:
                        voxel=mouse.hovered_entity
                        voxel.color=color.white

        


    file=open(room,'r')
    for lines in file:
        #seperate by comma
        l=lines.split(",")
        x=int(l[0])
        y=int(l[1])
        z=int(l[2])
        Brick_color=str(l[3])
        

        #drop entites based on color
        if(Brick_color.strip()=="white"):
            voxel = Voxel(position = (x,y,z),Brick_color=color.white)

        if(Brick_color.strip()=="brown"):
            voxel = Voxel(position = (x,y,z),Brick_color=color.brown)

        if(Brick_color.strip()=="green"):
            voxel = Voxel(position = (x,y,z),Brick_color=color.green)

        if(Brick_color.strip()=="red"):
            voxel = Voxel(position = (x,y,z),Brick_color=color.red)

        if(Brick_color.strip()=="yellow"):
            voxel = Voxel(position = (x,y,z),Brick_color=color.yellow)
        
 
    player = FirstPersonController()

    app.run()

    
#display where the worker had the most radiation
def load_data(room):

    data=[]
    radiations=[]
    t=[]
    file=open(room,'r')
    for lines in file:
        refined=lines.split(",")
        refined[0]=refined[0].strip()
        refined[1]=refined[1].strip()
        refined[2]=refined[2].strip()
        refined[3]=refined[3].strip()
        refined[4]=refined[4].strip()
        if refined not in data:
            data.append(refined)
            radiations.append(float(refined[3]))
            t.append(float(refined[4]))

    #sorting
    for i in range(0,len(data)):
        for j in range(0,len(data)):
            if float(data[j][3])<float(data[i][3]):
                temp=data[j][3]
                data[j][3]=data[i][3]
                data[i][3]=temp


        #print(data[i][3])

    print("top 10 locations where you received the most radiation along with the value:\n")
    for i in range(0,10):
        print("Amount of radiation: "+data[i][3]+" usv, Location("+data[i][0]+","+data[i][1]+","+data[i][2]+") at time: "+data[i][4]+" s\n")

    #plot
    plt.plot(t,radiations)
    plt.xlabel("Time in s")
    plt.ylabel("Radiation in usv")
    plt.show()

def main():

    ans=input("Do you want to create a new room or load an existing room or load results for a certain room? 'c' for create, 'l' for load 'd' for 'r' for results\n")

    if ans=="c":
        room=input("please enter the name of the room you want to create\n")
        room=room+".txt"

        create(room)

    elif ans=="l":
        room=input("please enter the name of the room you want to load\n")
        room=room+".txt"
        colored_block=input("enter color, 1:red, 2:green, 3:yellow, enter anythign else if you do not want to change the colors:)\n")
        x=input("enter the given x and y coordinates of where you will be wokring: (separate by pressing enter)\n")
        y=input("")

        load(room,int(colored_block),x,y)

    elif ans=="r":
        room=input("please enter the name of the room you want to load the data for\n")
        room="data_"+room+".txt"

        load_data(room)

main()
