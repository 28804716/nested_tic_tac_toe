#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 10:52:26 2025

@author: user
"""

import streamlit as st
import numpy as np
import datetime

def n_to_xo(n):
    if n == 1:
        return r"\circ"
    elif n == 2:
        return r"\times"
    else:
        return r"\;"
    
def n_to_xo_plaintext(n):
    if n == 1:
        return "o"
    elif n == 2:
        return "x"
    else:   
        return " "

def latex_gamestate_small(gamestate_matrix,size='small',focus=False):
    
    if size == 'small':
        if focus:
            s=r"\begin{array}{|c:c:c|}"
            s+=r"\hline "
        else:
            s=r"\begin{array}{c:c:c}"
        
    if size == 'large':
        s=r"\begin{array}{c|c|c}"
    
    for i in range(3):
        for j in range(3):
            if size == 'small':
                s+=rf"{n_to_xo(gamestate_matrix[i][j])}"
            if size == 'large':
                s+=rf"{gamestate_matrix[i][j]}"
            if j<2:
                s+="&"
        if i<2:
            if size == 'small':
                s+=r"\\\hdashline"
            if size == 'large':
                s+=r"\\\hline"
                
    if focus:
        s+=r"\\\hline"
    s+=r"\end{array}"
    return s

def sub_matrix(y,r,c):
    return np.reshape([y[3*r][3*c:3*c+3],
     y[3*r+1][3*c:3*c+3],
     y[3*r+2][3*c:3*c+3]],(3,3))
        


def latex_gamestate(gamestate_matrix,game_focus=[0,0]):
    
    s=r"\begin{array}{c|c|c}"
    
    for large_row in range(3):
        for large_column in range(3):
            small_gamestate_matrix=sub_matrix(gamestate_matrix,large_row,large_column)
            
            s+=latex_gamestate_small(small_gamestate_matrix,focus=([large_row,large_column]==game_focus))
            s+="&"
        s+=r"\\\\"
        if large_row<2:
            s+=r"\hline\\"
    s+=r"\end{array}"
    
    return s

if 'gamestate_matrix' not in st.session_state:
    print("regenerated matrix")
    st.session_state.gamestate_matrix=np.zeros((9,9))#np.round(2*np.random.rand(9,9)).astype(int)
    
    
if 'gamestate_matrix' not in st.session_state:
    game_win_matrix=np.zeros((3,3))
    
if 'player_turn' not in st.session_state:
    st.session_state.player_turn=1
    

if 'game_focus' not in st.session_state:
    st.session_state.game_focus=[0,0]
    
    
st.session_state.playername1=""
st.session_state.playername2=""




with st.sidebar:
    st.session_state.playername1=st.text_area("(o) Player 1 Name")
    st.session_state.playername2=st.text_area("(x) Player 2 Name")
    
    
if 'last_button_press' not in st.session_state:
    st.session_state.last_button_press =  datetime.datetime.now()

    
player_turn_str=""

if st.session_state.player_turn == 1:
    player_turn_str+="Player 1"
    if len(st.session_state.playername1)>0:
        player_turn_str+=f" ({st.session_state.playername1})"
    player_turn_str+=f" to play ({n_to_xo_plaintext(st.session_state.player_turn)})"
        
if st.session_state.player_turn == 2:
    player_turn_str+="Player 2"
    if len(st.session_state.playername2)>0:
        player_turn_str+=f" ({st.session_state.playername2})"
    player_turn_str+=f" to play ({n_to_xo_plaintext(st.session_state.player_turn)})"
    
    
st.text(player_turn_str)

big_col1,big_col2= st.columns([1,1])


with big_col1:
    st.latex(latex_gamestate(st.session_state.gamestate_matrix,game_focus=st.session_state.game_focus))

with  big_col2:

   small_cols = st.columns([1,1,1,1])
   
   sub_gamestate_matrix=sub_matrix(st.session_state.gamestate_matrix, st.session_state.game_focus[0], st.session_state.game_focus[1])
   if 0 not in sub_gamestate_matrix:
       print("CANNOT CONTINUE")
       st.session_state.game_focus[0]=int(round(2*np.random.rand()))
       st.session_state.game_focus[1]=int(round(2*np.random.rand()))
       st.rerun()
   
   for row in range(3):
       for col in range(3):
           
           with small_cols[col]:
               
                if st.button(f"{str(n_to_xo_plaintext(sub_gamestate_matrix[row][col]))}",key=f"{col}{row}",disabled=sub_gamestate_matrix[row][col]>0,on_click=print(sub_gamestate_matrix)):
                    
                    print(f"Button {col}{row} pressed by player {st.session_state.player_turn}")
                    if ( datetime.datetime.now()- st.session_state.last_button_press>datetime.timedelta(seconds=0.2)):
                        st.session_state.last_button_press=datetime.datetime.now()
                        if st.session_state.player_turn == 1:
                            print(f"Player 1 {3*st.session_state.game_focus[1]+col}{3*st.session_state.game_focus[0]+row} pressed")
                            st.session_state.gamestate_matrix[3*st.session_state.game_focus[0]+row][3*st.session_state.game_focus[1]+col]=1
                            st.session_state.player_turn = 2
                                                    
                        elif st.session_state.player_turn == 2:
                            
                            print(f"Player 2 {3*st.session_state.game_focus[1]+col}{3*st.session_state.game_focus[0]+row} pressed")
                            st.session_state.gamestate_matrix[3*st.session_state.game_focus[0]+row][3*st.session_state.game_focus[1]+col]=2
                            st.session_state.player_turn = 1
                            
                        st.session_state.game_focus[0]=row
                        st.session_state.game_focus[1]=col
                        
                        st.rerun()
                    
                    
                                
with big_col1:

    if st.button("Reset Match",type="primary"):
        print("Resetting match")
        st.session_state.gamestate_matrix=np.zeros((9,9))
        st.rerun()
        
