# -*- coding: utf-8 -*-
"""
Created on Wed May 31 14:15:40 2017

@author: yuwang

This is the Python code for parsing the data table in xls or xlsx extension.
"""

import os
import xlrd
import xlwt
import csv
import math
import datetime
import copy

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
        elif (len(AA)>0) and (any(c.isdigit() for c in AA)):
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
    if type(sheet) is list:
        W = sheet
        tpos = L-1
        II = -1
        for i in range(I+1,len(W)):
            if isblank(W[i][L]) is True:
                continue
            elif (isvalue(W[i][L]) is True) and (II < 0):
                II = i
                III = i
            elif (isvalue(W[i][L]) is True) and (II > 0):
                III = i
                break
            else:
                Error = 'Error: find incognitive values'
                print(Error)
                return 0
        while ((isblank(W[II][tpos]) is True) or (isblank(W[III][tpos]) is True)) and (tpos > 0):
            tpos = tpos -1
            
        if (istitle(W[II][tpos]) is True) and (istitle(W[III][tpos]) is True):
            return tpos
        else:
            Error = 'Error: cannot find titles'
            print(Error)
    else:
        tpos = L-1
        II = -1
        for i in range(I+1,sheet.nrows):
            if isblank(sheet.cell(i,L).value) is True:
                continue
            elif (isvalue(sheet.cell(i,L).value) is True) and (II < 0):
                II = i
                III = i
            elif (isvalue(sheet.cell(i,L).value) is True) and (II > 0):
                III = i
                break
            else:
                Error = 'Error: find incognitive values'
                print(Error)
                return 0
        while ((isblank(sheet.cell(II,tpos).value) is True) or (isblank(sheet.cell(III,tpos).value) is True)) and (tpos > 0):
            tpos = tpos -1
            
        if (istitle(sheet.cell(II,tpos).value) is True) and (istitle(sheet.cell(III,tpos).value) is True):
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

def transpose(sheet,bookname = None,sheetname = None,sym = None,dirout = None):
    if type(sheet) is list:
        W=sheet
        WW = []
        for j in range(0,len(W[0])):
            WW.append([W[i][j] for i in range(0,len(W))])
        return WW
    else:
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
        dir = dirout + sym + bookname + '_' + 'Transposed' +'.xls'
        outbook.save(dir)
        return dir
            
def findfirstyear(W):
    for i in range(0,len(W)):
        for j in range(0,len(W[0])):
            if isyear(W[i][j]) is True:
                return [i,j]
    return [-1,-1]
                
def isunique(W0):
    W=copy.deepcopy(W0)
    FY = findfirstyear(W)
    if FY[0]<0:
        return ['TN',-1,-1,-1]
    I=FY[0]
    J=FY[1]
    i = I
    j = J
    W[i][j] = ''
    while (isyear(W[i][j+1]) is True):
        j=j+1
        W[i][j] = ''
        if j==(len(W[0])-1):
            break
    if j>J:
        R = findfirstyear(W)
        if R[0]<0:
            return ['TR',I,J,j]
        else:
            return ['FR',I,J,j]
    else:
        while (isyear(W[i+1][j]) is True):
            i=i+1
            W[i][j] = ''
            if i==len(W)-1:
                break
        if i>I:
            R = findfirstyear(W)
            if R[0]<0:
                return ['TC',I,J,i]
            else:
                return ['FC',I,J,i]
        else:
            print('Warning: only one year found, maybe an error.')
            return ['TO',I,J,I]
def cutblock(W0,R):
    W = copy.deepcopy(W0)
    if R[0] == 'TN':
        Error = 'Error: There are no years found'
        print(Error)
        return [-1,-1,-1,-1]
    elif R[0] == 'TO':
        Error = 'Error: There is only one year found'
        print(Error)
        return [-1,-1,-1,-1]
    else:
        if R[0][1]=='R':
            I = R[1]
            L = R[2]
            R = R[3]
            tpos = titlepos(W,I,L)
            #print(I)
            #print(L)
            #print(W)
            #print(tpos)
            TW = [[W[I][tpos]]+copy.deepcopy(W[I][L:R+1])]
            #print(TW)
            W[I][tpos] = ''
            for j in range(L,R+1):
                W[I][j] = ''
            
            for i in range(I+1,len(W)):
                if (any(isyear(ele) for ele in W[i][L:R+1]) or (any(istitle(ele) for ele in W[i][L:R+1]))):
                    return [W,TW]
                else:
                    #print([W[i][tpos]]+copy.deepcopy(W[i][L:R+1]))
                    TW.append([W[i][tpos]]+copy.deepcopy(W[i][L:R+1]))
                    W[i][tpos] = ''
                    for j in range(L,R+1):
                        W[i][j]=''
            return [W,TW]
        else:
            WT = transpose(W)
            T = cutblock(WT,['*R',R[2],R[1],R[3]])
            WTC = T[0]
            TW = T[1]
            W = transpose(WTC)
            return [W,TW]
            

def prep(dirin,dirout,NAME = None):
    book = xlrd.open_workbook(dirin)
    dd= -1
    for cc in range(len(dirin)-1,-1,-1):
        if (dirin[cc]=='.') and (dd < 0):
            dd=cc
        elif (dirin[cc]=='\\') or (dirin[cc]=='/'):
            sym = dirin[cc]
            bookname = dirin[cc+1:dd]
            break
    sheetnames = book.sheet_names()
    Dict = {}
    for s in range(0,book.nsheets):
        sheet = book.sheet_by_index(s)
        #print(sheetnames[s])
        W = []
        I = sheet.nrows
        J = sheet.ncols
        for i in range(0,I):
            W.append(sheet.row_slice(i,0,J))
            for j in range(0,J):
                W[-1][j] = W[-1][j].value
        R = isunique(W)
        part = 1
        #print(R)
        #print(W)
        while ((R[0][0] == 'F')):
            RR = cutblock(W,R)
            W = RR[0]
            TW = RR[1]
            
            #print(W)
            Dict.update({sheetnames[s]+'_part_'+str(part) : TW})
            part = part + 1
            R = isunique(W)
            #print(R)
        Dict.update({sheetnames[s] : W})
    
    #print(Dict.keys())
    outbook = xlwt.Workbook()
    for Snames in Dict.keys():
        outsheet = outbook.add_sheet(Snames)
        W = Dict[Snames]
        I = len(W)
        J = len(W[0])
        for i in range(0,I):
            for j in range(0,J):
                outsheet.write(i,j,W[i][j])
    dirinter = dirout + sym + bookname + '_' + 'preped' +'.xls'
    outbook.save(dirinter)
        

def xlsparser(dirin,dirout,NAME = None):
    prep(dirin,dirout)
    dd = -1;
    for cc in range(len(dirin)-1,-1,-1):
        if (dirin[cc]=='.') and (dd<0):
            dd=cc
        elif (dirin[cc]=='\\') or (dirin[cc]=='/'):
            sym = dirin[cc]
            bookname = dirin[cc+1:dd]
            break
    dirprep = dirout + sym + bookname + '_preped.xls'
    book = xlrd.open_workbook(dirprep)
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
            if NAME is None:
                outbook.save(dirout + sym + bookname + '_' + sheetnames[s] +'.xls')
            else:
                outbook.save(dirout + sym + NAME + '_' + sheetnames[s] +'.xls')
        else:
            if (NAME is None):
                dirinter = transpose(sheet,bookname,sheetnames[s],sym,dirout)
                xlsparser(dirinter,dirout,bookname)
            else:
                dirinter = transpose(sheet,NAME,sheetnames[s],sym,dirout)
                xlsparser(dirinter,dirout,NAME)
            os.remove(dirinter)
    
    os.remove(dirprep)
        
def csvparser(dirin,dirout,NAME = None):
    dd = -1
    for cc in range(len(dirin)-1,-1,-1):
        if (dirin[cc]=='.') and (dd < 0):
            dd=cc
        elif (dirin[cc]=='\\') or (dirin[cc]=='/'):
            sym = dirin[cc]
            bookname = dirin[cc+1:dd]
            break
    W = []
    with open(dirin) as csvfile:
        FILE = csv.reader(csvfile, delimiter=',')
        for row in FILE:
            W.append(row)
    outbook = xlwt.Workbook()
    outsheet = outbook.add_sheet(bookname)
    I = len(W)
    J = len(W[0])
    for i in range(0,I):
        for j in range(0,J):
            outsheet.write(i,j,W[i][j])
    dirinter = dirout + sym + bookname + '_' + 'Exceled' +'.xls'
    outbook.save(dirinter)
    if NAME is None:
        xlsparser(dirinter,dirout,bookname)
    else:
        xlsparser(dirinter,dirout,NAME)
        
    os.remove(dirinter)
    
def parser(dirin,dirout):
    ext = ''
    dd = -1;
    for cc in range(len(dirin)-1,-1,-1):
        if (dirin[cc]=='.') and (dd<0):
            dd=cc
            ext = dirin[cc+1:]
        elif (dirin[cc]=='\\') or (dirin[cc]=='/'):
            sym = dirin[cc]
            bookname = dirin[cc+1:dd]
            break
    Dirout = dirout + sym + bookname + '_parsed'
    if ext=='':
        Error = 'Error: Invalid directory - No extension found.'
        print(Error)
        return
    elif (ext == 'xlsx') or (ext == 'xls'):
        if not os.path.exists(Dirout):
            os.makedirs(Dirout)
        xlsparser(dirin,Dirout)
    elif (ext == 'csv'):
        if not os.path.exists(Dirout):
            os.makedirs(Dirout)
        csvparser(dirin,dirout)
    else:
        Error = 'Error: Only support .xls .xlsx and .csv. Exit.'
        print(Error)
        return



""" --------Debug--------- """

dirin = "/Users/yuwang/Documents/PPI/Downloader_Git/Sample_Data/Test.xlsx"
dirout = "/Users/yuwang/Documents/PPI/Downloader_Git/Parsed_Data"

#csvparser(dirin,dirout)
#xlsparser(dir,dirout)
#xlsparser(dirin,dirout)
#prep(dirin,dirout)
parser(dirin,dirout)














