# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 14:31:37 2021

@author: Erwin Tredmonfall
"""

from manim import *
from manim.utils.file_ops import open_file as open_media_file
import tkinter as tk
import numpy as np

class Tool(Scene):
    
    def left_align(self,obj, reference, buff=0.3):
        obj.next_to(Dot(self.pos(reference,DL,buff),0.01,fill_opacity=0),DR,buff)
    
    def next_align(self,obj,reference,direction,alignment,buff=3):
        obj.next_to(Dot(self.pos(reference,direction+alignment,buff),0.01,fill_opacity=0),direction-alignment,buff)
    
    def pos(self,obj, direction, buffer=0):
        d = Dot(fill_opacity = 0, radius=0.0001)
        d.next_to(obj, direction, buffer)
        return d.get_center()
    
    def str_expr(self,coeff,exp):
        r = r"""\("""+str(coeff)
        if exp >= 1:
            r+= r"""x"""
        if exp >= 2:
            r+= r"""^""" + str(exp)
        r += r"""\)"""
        return r
    
    def inv_poly_list(self,p,remove_zeros = True):
        p.reverse()
        P=[]
        if len(p)==0:
            return[r"""\(0\)"""]
        for i in range(len(p)):
            if remove_zeros:
                if len(P) > 0:
                    if p[i]>0:
                        P.append(r"""\(+\)""")
                    elif p[i]<0:
                        P.append(r"""\(-\)""")
                    if p[i]!=0:
                        P.append(self.str_expr(abs(p[i]),len(p)-i-1))
                else:
                    if p[i]!=0:
                        P.append(self.str_expr(p[i],len(p)-i-1))
            else:
                if len(P)>0:
                    if p[i]>=0:
                        P.append(r"""\(+\)""")
                    else:
                        P.append(r"""\(-\)""")
                    P.append(self.str_expr(abs(p[i]),len(p)-i-1))
                else:
                    P.append(self.str_expr(p[i],len(p)-i-1))
        p.reverse()
        return P
    
    def standard_divide(self,rp,p1,upper_left,scale=0.7):
        def count_indent(p_column,rp_new):
            print(p_column)
            print(rp_new)
            a = 0
            for i in range(len(rp_new),len(p_column)):
                if p_column[i] !=0:
                    a+=2
            return a
        def division_step(rp,p1,rp_tex,first_step,scale):
            ### calculate component of result
            result_coeff = int(round(rp[-1]/p1[-1],1))
            result_exp = len(rp)-len(p1)
            add_to_result = []
            if result_coeff >= 0:
                sign = Tex(r"""\(+\)""")
                if not first_step:
                    add_to_result.append(sign)
            else:
                sign = Tex(r"""\(-\)""")
                add_to_result.append(sign)
            result_comp =  Tex(self.str_expr(abs(result_coeff), result_exp))
            add_to_result.append(result_comp)
            ### create the component
            first_line_create=[]
            for e in add_to_result:
                e.scale(scale)
                e.next_to(first_line[-1],RIGHT,0.05)
                first_line.append(e)
                first_line_create.append(Write(e))
            self.play(*first_line_create)
            ### "fill" the rest of the "column" (what needs to be subtracted)...
            p_column = []
            for i in range(result_exp):
                p_column.append(0)
            for i in p1:
                p_column.append(i*result_coeff)
            p_c_tex = Tex(*self.inv_poly_list(p_column,True))
            p_c_tex.scale(scale)
            self.left_align(p_c_tex, rp_tex,buff=0.04)
            sub_left = Tex(r"""\(-(\)""")
            sub_left.scale(scale)
            self.next_align(sub_left,p_c_tex,LEFT,UP,0.05)
            sub_right = Tex(r"""\()\)""")
            sub_right.scale(scale)
            self.next_align(sub_right,p_c_tex,RIGHT,UP,0.05)
            self.play(Write(p_c_tex),Write(sub_left),Write(sub_right))
            ### horizontal line...
            l1 = Dot(fill_opacity=0)
            l1.next_to(sub_left,DL,buff=0.02)
            l2 = Dot(fill_opacity=0)
            l2.next_to(sub_right,DR,buff=0.02)
            horizontal = Line(start=l1.get_center(),end=l2.get_center())
            self.play(Write(horizontal))
            ### calulate remaining polynomial
            while len(p_column) < len(rp):
                p_column.append(0)
            rp_new = []
            for i in range(len(rp)):
                rp_new.append(rp[i]-p_column[i])
            while len(rp_new)>0 and rp_new[-1] == 0:
                rp_new = rp_new[:-1]
            rp_new_tex = Tex(*self.inv_poly_list(rp_new))
            rp_new_tex.scale(scale)
            if len(rp_new)==0:
                rp_new.append(0)
            if rp_new[-1]>=0:
                self.left_align(rp_new_tex,p_c_tex[count_indent(p_column,rp_new)],buff=0.15)
            else:
                self.left_align(rp_new_tex,p_c_tex[count_indent(p_column,rp_new)-1],buff=0.15)
            self.play(Write(rp_new_tex))
            if len(rp_new) > 1:
                division_step(rp_new, p1, rp_new_tex, False, scale)
            
                
        ul= Dot(point=upper_left,radius=0.001,fill_opacity=0)
        rp_tex = Tex(*self.inv_poly_list(rp))
        p1_tex = Tex(*self.inv_poly_list(p1))
        first_line = [Tex(r"""\((\)"""),
                      rp_tex,
                      Tex(r"""\()\divisionsymbol (\)"""),
                      p1_tex,
                      Tex(r"""\()=\)""")]
        for i in range(len(first_line)):
            first_line[i].scale(scale)
            if i==0:
                first_line[i].next_to(ul,DR,buff=0.05)
            else:
                first_line[i].next_to(first_line[i-1],RIGHT,buff=0.05)
            self.play(Write(first_line[i]))
        s = len(first_line)
        division_step(rp, p1, rp_tex, True,scale)
        dl = Dot(radius=0.001,fill_opacity=0)
        dl.next_to(first_line[s],DL,0.05)
        dr = Dot(radius=0.001,fill_opacity=0)
        dr.next_to(first_line[-1],DR,0.05)
        final_1 = Line(dl.get_center(),dr.get_center(),stroke_width=0.5*DEFAULT_STROKE_WIDTH)
        final_2 = Line(dl.get_center(),dr.get_center(),stroke_width=0.5*DEFAULT_STROKE_WIDTH)
        final_2.shift(0.05*DOWN)
        self.play(Write(final_1),run_time=0.2)
        self.play(Write(final_2),run_time=0.2)
    
    def construct(self):
        self.standard_divide(self.rp, self.p1, -4.5*RIGHT+2.5*UP)

T = Tool()
def number(a):
    a = float(a)
    if a-int(a)==0:
        a=int(a)
    return a
def poly_str2list(text):
    if text[0]=="+":
        text=text[1:]
    strings = []
    a = text.split("+")
    for i in a:
        b = i.split("-")
        if b[0] != "":
            strings.append(b[0])
        if len(b)>1:
            for u in b[1:]:
                strings.append("-"+u)
    print("strings: ",strings)
    doubles = []
    for i in strings:
        c1=1
        if i[0] == "-":
            c1=-1
            i=i[1:]
        if "x" in i:
            if i[0]=="x":
                c2=1
            else:
                c2 = number(i.split("x")[0])
        else:
            c2 = number(i)
        if "^" in i:
            e = number(i.split("^")[1])
        elif "x" in i:
            e = 1
        else:
            e=0
        doubles.append((c1*c2,e))
    print("doubles: ",doubles)
    doubles.sort(key=lambda x:x[1])
    print("doubles: ",doubles)
    final_list=[]
    for i in range(doubles[-1][1]+1):
        if doubles[0][1] == i:
            final_list.append(doubles[0][0])
            doubles=doubles[1:]
        else:
            final_list.append(0)
    print("final_list: ",final_list)
    return final_list
def proper_filename(text,default_name="big_video"):
    if text=="":
        return default_name
    while not (65<=ord(text[0])<=90 or 97<=ord(text[0])<=122):
        text=text[1:]
    if text=="":
        return default_name
    text=text.replace(" ","_")
    i=0
    while i<len(text):
        o = ord(text[i])
        if not (65<=o<=90 or 97<=o<=122 or 48<=o<=57 or o==95):
            text_front = text[:i]
            if i<len(text)-1:
                text_front += text[i+1:]
            text=text_front
        i+=1
    return text
r = tk.Tk()
r.title('Simple tool for polynomial division')
r.geometry('400x400')
r.configure(bg='black')
L0 = tk.Label(r,text='Creating animations of polynomial division\nusing "Manim Community v0.9.0"',bg="black",fg="white")
L0.place(x=50,y=50)
L05 = tk.Label(r,text="Enter name of output file",bg="black",fg="white")
L05.place(x=50,y=100)
E0 = tk.Entry()
E0.place(x=200,y=100)
E0.insert(0,"polynomial_division")
E1 = tk.Entry(r)
E1.place(x=200,y=150)
E1.insert(0,"-1+x^4")
L15=tk.Label(r,text="Enter dividend",bg="black",fg="white")
L15.place(x=50,y=150)
L1 = tk.Label(r,text="÷",bg="black",fg="white")
L1.place(x=200,y=175)
E2 = tk.Entry(r)
E2.place(x=200,y=200)
E2.insert(0,"x^3+x^2+x+1")
L25=tk.Label(r,text="Enter divisor",bg="black",fg="white")
L25.place(x=50,y=200)
L1 = tk.Label(r,text="=",bg="black",fg="white")
L1.place(x=200,y=225)
def render_video(T=T,E1=E1,E2=E2):
    global config
    config.OUTPUT_FILE = proper_filename(E0.get())
    file_name = proper_filename(E0.get())
    Tool2 = type(file_name,(Tool,),{})
    T2=Tool2()
    T2.rp=poly_str2list(E1.get())
    T2.p1=poly_str2list(E2.get())
    T2.render(True)
    open_media_file(T2.renderer.file_writer.movie_file_path)
    del T2
    del Tool2
B = tk.Button(r,text="Create animated Video",command=render_video,bg="black",fg="white")
B.place(x=100,y=250)
r.mainloop()
