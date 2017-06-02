# -*- coding: utf-8 -*-
"""
Created on Wed May 31 14:15:40 2017

@author: yuwang

This is the Python code for parsing the data table in xls or xlsx extension.
"""

import os
import xlrd
import xlwt
import math
import datetime

""" ---------Core-------- """

def isyear(A):
    if type(A) is float:
        P = math.modf(A)
        eps = 0.00001;
        Deci = P[0]
        Inti = P[1]
        if abs(Deci) <= eps:
            Y = Inti
        else:
            return False
    elif type(A) is int:
        Y = A;
    elif (type(A) is str) and len(A)<15:
        B = [int(s) for s in A.split() if s.isdigit()]
        BB = [isyear(b) for b in B]
        return any(BB)
    else:
        return False
    
    if Y in range(1700,datetime.datetime.now().year+30):
        return True
    else:
        return False

def isvalue(A):
    if type(A) in [float,int]:
        return True
    elif (type(A) is str) and (any(c.isdigit() for c in A)) and (len(A)<15):
        return True
    else:
        return False

def isblank(A):
    if type(A) is str:
        AA = A
        for c in 'Nn/Aa ':
            AA = AA.replace(c,'')
        if (len(AA)>0) and (any(c.isalpha() for c in AA)):
            return False
        else:
            return True
    else:
        return False

def istitle(A):
    if (type(A) is str) and any(c.isalpha() for c in A):
        return True
    else:
        return False

def RorC(sheet):
    for i in range(0,sheet.nrows):
        for j in range(0,sheet.ncols):
            if isyear(sheet.cell(i,j).value) is True:
                if isyear(sheet.cell(i,j+1).value) is True:
                    return 'Row'+str(i)
                elif isyear(sheet.cell(i+1,j).value) is True:
                    return 'Col'+str(j)
                else:
                    Error = 'Error: Not consistent year'
                    print(Error)
                    return Error
    Error = 'Error: cannot find any years'
    print(Error)
    return Error

def titlepos(sheet,I,L):
    tpos = L-1
    II = -1
    for i in range(I+1,sheet.nrows):
        if isblank(sheet.cell(i,L).value) is True:
            continue
        elif (isvalue(sheet.cell(i,L).value) is True) and (II < 0):
            II = i
        elif (isvalue(sheet.cell(i,L).value) is True) and (II > 0):
            III = i
            break
        else:
            Error = 'Error: find incognitive values'
            print(Error)
            return 0
    while (sheet.cell(II,tpos).value==sheet.cell(III,tpos).value or (isblank(sheet.cell(II,tpos).value) is True) or (isblank(sheet.cell(III,tpos).value) is True)) and (tpos > 0):
        tpos = tpos -1
    
    if (istitle(sheet.cell(II,tpos).value) is True) and (istitle(sheet.cell(III,tpos).value) is True) and (sheet.cell(II,tpos).value!=sheet.cell(III,tpos).value):
        return tpos
    else:
        Error = 'Error: cannot find titles'
        print(Error)
     
     
def isemptyrow(sheet,i,L,R):
    for j in range(L,R+1):
        if isblank(sheet.cell(i,j).value) is True:
            pass
        elif isvalue(sheet.cell(i,j).value) is True:
            return False
        else:
            Error = 'Error: find incognitive values'
            print(Error)
            return False
    
    return True

def transpose(sheet,bookname,sheetname,sym,dirout):
    W = []
    I = sheet.nrows
    J = sheet.ncols
    for i in range(0,I):
        W.append(sheet.row_slice(i,0,J))
        for j in range(0,len(W[-1])):
            W[-1][j] = W[-1][j].value
    outbook = xlwt.Workbook()
    outsheet = outbook.add_sheet(sheetname)
    for i in range(0,I):
        for j in range(0,J):
            outsheet.write(j,i,W[i][j])
    dir = dirout + sym + bookname + '_' + 'Transposed_Temp' +'.xls'
    outbook.save(dir)
    return dir
            
    
    

def parser(dirin,dirout):
    book = xlrd.open_workbook(dirin)
    for cc in range(len(dirin)-1,-1,-1):
        if (dirin[cc]=='.'):
            dd=cc
        elif (dirin[cc]=='\\') or (dirin[cc]=='/'):
            sym = dirin[cc]
            bookname = dirin[cc+1:dd]
            break
    sheetnames = book.sheet_names()
    
    for s in range(0,book.nsheets):
        sheet = book.sheet_by_index(s)
        structure = RorC(sheet)
        if structure[0:5]=='Error':
            print('Error: cannot recognize the structure, see error info above. Pass.')
            continue
        elif structure[0:3]=='Row':
            I = int(structure[3:])
            for j in range(0,sheet.ncols-1):
                if isyear(sheet.cell(I,j).value) is True:
                    L = j
                    break
            for j in range(sheet.ncols-1,0,-1):
                if isyear(sheet.cell(I,j).value) is True:
                    R = j
                    break
            Years = sheet.row_slice(I,L,R+1)
            for i in range(0,len(Years)):
                Years[i]=Years[i].value
                
            W = [['Years']+Years+['Row']]
            LL = titlepos(sheet,I,L)
            for i in range(I+1,sheet.nrows):
                if isemptyrow(sheet,i,L,R) is True:
                    continue
                else:
                    W.append([sheet.cell(i,LL).value]+sheet.row_slice(i,L,R+1))
                    for j in range(1,len(W[-1])):
                        W[-1][j] = W[-1][j].value
                    W[-1]=W[-1]+[i+1]
            outbook = xlwt.Workbook()
            RLen = len(W[0])
            for R in W[1:]:
                outsheet = outbook.add_sheet('Row '+str(R[-1]))
                outsheet.write(0,0,'Years')
                outsheet.write(0,1,R[0])
                for i in range(1,RLen-1):
                    outsheet.write(i,0,W[0][i])
                    outsheet.write(i,1,R[i])
            outbook.save(dirout + sym + bookname + '_' + sheetnames[s] +'.xls')
        else:
            dirinter = transpose(sheet,bookname,sheetnames[s],sym,dirout)
            parser(dirinter,dirout)
            #os.remove(dirinter)
        

        
        

""" --------Debug--------- """
"""
dir = "/Users/yuwang/Documents/PPI/Downloader_Git/Sample_Data/sbsummar.xls"
dirout = "/Users/yuwang/Documents/PPI/Downloader_Git/Sample_Data/Parsed_Data"
book = xlrd.open_workbook(dir)
parser(dir,dirout)
"""















