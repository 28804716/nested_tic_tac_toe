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
            s=r"\begin{array}{||c:c:c||}"
            s+=r"\hline\hline"
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
        s+=r"\\\hline\hline"
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
    
    
if 'game_win_matrix' not in st.session_state:
    st.session_state.game_win_matrix=np.zeros((3,3))
    
if 'player_turn' not in st.session_state:
    st.session_state.player_turn=1
    

if 'game_focus' not in st.session_state:
    st.session_state.game_focus=[0,0]
    
    
st.session_state.playername1=""
st.session_state.playername2=""




with st.sidebar:
    st.session_state.playername1=st.text_area(f"(o) Player 1 Name ({np.sum(st.session_state.game_win_matrix==1)} points)")
    st.session_state.playername2=st.text_area(f"(x) Player 2 Name ({np.sum(st.session_state.game_win_matrix==1)} points)")
    st.write("Game Summary:")
    st.latex(latex_gamestate_small(st.session_state.game_win_matrix,size='small',focus=False))
    
    
if 'last_button_press' not in st.session_state:
    st.session_state.last_button_press =  datetime.datetime.now()

    
player_turn_str=""

if st.session_state.player_turn == 1:
    player_turn_str+=f"Player 1 ({np.sum(st.session_state.game_win_matrix==1)} points)"

    if len(st.session_state.playername1)>0:
        player_turn_str+=f" ({st.session_state.playername1})"
    player_turn_str+=f" to play ({n_to_xo_plaintext(st.session_state.player_turn)})"
        
if st.session_state.player_turn == 2:
    player_turn_str+=f"Player 2 ({np.sum(st.session_state.game_win_matrix==2)} points)"
    if len(st.session_state.playername2)>0:
        player_turn_str+=f" ({st.session_state.playername2})"
    player_turn_str+=f" to play ({n_to_xo_plaintext(st.session_state.player_turn)})"

for row in range(3):
    for col in range(3):
        sub_gamestate_matrix=sub_matrix(st.session_state.gamestate_matrix, row, col)
        if st.session_state.game_win_matrix[row][col] == 0:
            
            for p in [1,2]:
                pwin=p*np.ones(3)
                #Diangonals
                if np.array_equal(np.fliplr(sub_gamestate_matrix).diagonal(),pwin) or np.array_equal(sub_gamestate_matrix.diagonal(),pwin):
                    st.session_state.game_win_matrix[row][col]=p
                
                #Across and down
                for i in range(3):
                    if np.array_equal(sub_gamestate_matrix[i],pwin) or np.array_equal((sub_gamestate_matrix.T)[i],pwin):
                        st.session_state.game_win_matrix[row][col]=p    
            if st.session_state.game_win_matrix[row][col]!=0:st.rerun()
    


big_cols,big_col1,big_col2= st.columns([1,3,1])

with big_cols:
    st.write("Game Summary:")
    st.latex(latex_gamestate_small(st.session_state.game_win_matrix,size='small',focus=False))

with big_col1:
    st.write("Entire Field:")
    st.latex(latex_gamestate(st.session_state.gamestate_matrix,game_focus=st.session_state.game_focus))

with  big_col2:
    st.text(player_turn_str)
    small_cols = st.columns([1,1,1])
   
    
   #Scoring:
        #Check that game has not already been scored
        
    
                                
                                
                
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
        st.session_state.game_win_matrix=np.zeros((3,3))
        st.rerun()
        
