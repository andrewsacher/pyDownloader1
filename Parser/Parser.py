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
import re

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
        B = re.findall('\d+',A)
        if B == []:
            return False
        for i in range(0,len(B)):
            B[i] = int(B[i])
        BB = [isyear(b) for b in B]
        return any(BB)
    else:
        return False
    
    if Y in range(1700,datetime.datetime.now().year+30):
        return True
    else:
        return False
def year(A):
    if type(A) is float:
        return int(A)
    elif type(A) is int:
        return A
    elif type(A) is str:
        B=re.findall('\d+',A)
        for c in B:
            if isyear(c) is True:
                return int(c)
        Error = 'Error: Cannot find any years - check if this is a year'
        print(Error)
        return
    else:
        Error = 'Error: Cannot recognize the content'
        print(Error)
        return
def isvalue(A):
    if type(A) in [float,int]:
        return True
    elif (type(A) is str) and (any(c.isdigit() for c in A) is True):
        for i in range(0,len(A)):
            if A[i] in [' ','\xa0']:
                pass
            else:
                B = A[i:]
                break
        try:
            float(B)
            return True
        except:
            if B[-1] in [')',']','}',' ','\xa0'] and (B[0].isdigit() is True):
                return True
            else:
                return False
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
        if (isblank(A) is True) or (isvalue(A) is True):
            return False
        else:
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

def titlepos(sheet,I,L,R):
    #print('L: ',L)
    #print('R: ',R)
    if type(sheet) is list:
        W = sheet
        tpos = L-1
        II = -1
        for i in range(I+1,len(W)):
            #print(W[i][L:R+1])
            if isemptyrow(W,i,L,R) is True:
                #print(W[i][L:R+1])
                continue
            elif (isemptyrow(W,i,L,R) is False):
                if any([istitle(c) for c in W[i][L:R+1]]) is True:
                    break
                elif II < 0:
                    II=i
                    III=i
                else:
                    III=i
                    break
        while ((isblank(W[II][tpos]) is True) or (isblank(W[III][tpos]) is True)) and (tpos > 0):
            tpos = tpos -1
            
        if (istitle(W[II][tpos]) is True) and (istitle(W[III][tpos]) is True):
            return tpos
        else:
            #print('II= ',II)
            #print('III= ',III)
            Error = 'Error: cannot find titles'
            print(Error)
    else:
        tpos = L-1
        II = -1
        for i in range(I+1,sheet.nrows):
            if isemptyrow(sheet,i,L,R) is True:
                continue
            elif (isemptyrow(sheet,i,L,R) is False):
                if any([istitle(c.value) for c in sheet.row_slice(i,L,R+1)]) is True:
                    break
                elif II < 0:
                    II=i
                    III=i
                else:
                    III=i
                    break
        while ((isblank(sheet.cell(II,tpos).value) is True) or (isblank(sheet.cell(III,tpos).value) is True)) and (tpos > 0):
            tpos = tpos -1
            
        if (istitle(sheet.cell(II,tpos).value) is True) and (istitle(sheet.cell(III,tpos).value) is True):
            return tpos
        else:
            Error = 'Error: cannot find titles'
            print(Error)
     
def isemptyrow(sheet,i,L,R):
    if type(sheet) is list:
        W = sheet
        for j in range(L,R+1):
            if isblank(W[i][j]) is True:
                pass
            elif (isvalue(W[i][j]) is True) or (istitle(W[i][j]) is True):
                return False
            else:
                Error = 'Error: find incognitive values'
                info = W[i][j]
                print(Error)
                print('Info: W[',i,'][',j,']=',info)
                print('Info type: ',type(info))
                return False
        return True
    else:
        for j in range(L,R+1):
            if isblank(sheet.cell(i,j).value) is True:
                pass
            elif (isvalue(sheet.cell(i,j).value) is True) or (istitle(sheet.cell(i,j).value) is True):
                return False
            else:
                Error = 'Error: find incognitive values'
                info = sheet.cell(i,j).value
                print(Error)
                print('Info: sheet[',i,'][',j,']=',info)
                print('Info type: ',type(info))
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
    if j < len(W[0])-1:
        while (isyear(W[i][j+1]) is True):
            if abs(year(W[i][j+1])-year(W0[i][j]))<15:
                j=j+1
                W[i][j] = ''
                if j==(len(W[0])-1):
                    break
            else:
                break
    if j>J:
        R = findfirstyear(W)
        if R[0]<0:
            return ['TR',I,J,j]
        else:
            return ['FR',I,J,j]
    else:
        #print('{',i,j,'}')
        #print(len(W))
        if i<len(W)-1:
            while (isyear(W[i+1][j]) is True):
                if abs(year(W[i+1][j])-year(W0[i][j]))<15:
                    i=i+1
                    W[i][j] = ''
                    if i==len(W)-1:
                        break
                else:
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
    #print('Cutblock')
    W = copy.deepcopy(W0)
    if R[0] == 'TN':
        Error = 'Error: There are no years found'
        print(Error)
        return [W,[]]
    elif R[0] == 'TO':
        Error = 'Error: There is only one year found'
        print(Error)
        I = R[1]
        J = R[2]
        W[I][J] = ''
        return[W,[]]
    else:
        if R[0][1]=='R':
            I = R[1]
            L = R[2]
            R = R[3]
            tpos = titlepos(W,I,L,R)
            #print(I)
            #print(L)
            #print(W)
            #print(tpos)
            TW = [[W[I][tpos]]+copy.deepcopy(W[I][L:R+1])]
            #print(TW)
            #W[I][tpos] = ''
            for j in range(L,R+1):
                W[I][j] = ''
            #if R+1 < len(W[I]):
            #    W[I][R+1] = ''
            
            
            for i in range(I+1,len(W)):
                if any(istitle(ele) for ele in W[i][L:R+1]):
                    #print(W[i][L:R+1])
                    return [W,TW]
                elif (any(isyear(ele) for ele in W[i][L:R+1])):
                    for j in range(L,R+1):
                        if isyear(W[i][j]) is True:
                            YJ = j
                            break
                    #print('[',i, YJ,']')
                    
                    if (YJ+1 < len(W[i])):
                        if (isyear(W[i][YJ]) is True) and (isyear(W[i][YJ+1]) is True) and abs(year(W[i][YJ])-year(W[i][YJ+1]))<5:
                            #print(W[i][L:R+1])
                            return [W,TW]
                TW.append([W[i][tpos]]+copy.deepcopy(W[i][L:R+1]))
                #W[i][tpos] = ''
                for j in range(L,R+1):
                    W[i][j]=''
            #print('i=',i)
            #print(W[i][L:R+1])
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
    #print(sheetnames)
    #print(book.nsheets)
    Dict = {}
    for s in range(0,book.nsheets):
        sheet = book.sheet_by_index(s)
        print(sheetnames[s])
        W = []
        I = sheet.nrows
        J = sheet.ncols
        for i in range(0,I):
            W.append(sheet.row_slice(i,0,J))
            for j in range(0,J):
                W[-1][j] = W[-1][j].value
        R = isunique(W)
        part = 1
        print(R)
        #print(W)
        while ((R[0][0] == 'F') or (R[0]=='TO')):
            if R[0][0]=='F':
                RR = cutblock(W,R)
                W = RR[0]
                TW = RR[1]
                #print(W)
                Dict.update({sheetnames[s]+'_part_'+str(part) : TW})
                part = part + 1
            else:
                RR=cutblock(W,R)
                W=RR[0]
            R = isunique(W)
            print(R)
        if R[0]!='TN':
            Dict.update({sheetnames[s] : W})
        del W
    
    #print(Dict.keys())
    outbook = xlwt.Workbook()
    for Snames in Dict.keys():
        #print(Dict.keys())
        outsheet = outbook.add_sheet(Snames)
        W = Dict[Snames]
        if W==[]:
            continue
        I = len(W)
        J = len(W[0])
        for i in range(0,I):
            for j in range(0,J):
                try:
                    outsheet.write(i,j,W[i][j])
                except:
                    if j>= 255:
                        print('writing [',i,'][',j,']')
                    outsheet.write(i,j,'****')
                    #print(W[i][j])
                    pass
    dirinter = dirout + sym + bookname + '_' + 'preped' +'.xls'
    outbook.save(dirinter)
    return dirinter


def xlsparser(dirin,dirout,NAME = None):
    #prep(dirin,dirout)
    dd = -1;
    for cc in range(len(dirin)-1,-1,-1):
        if (dirin[cc]=='.') and (dd<0):
            dd=cc
        elif (dirin[cc]=='\\') or (dirin[cc]=='/'):
            sym = dirin[cc]
            bookname = dirin[cc+1:dd]
            break
    #dirprep = dirout + sym + bookname + '_preped.xls'
    book = xlrd.open_workbook(dirin)
    sheetnames = book.sheet_names()
    
    for s in range(0,book.nsheets):
        sheet = book.sheet_by_index(s)
        structure = RorC(sheet)
        if structure[0:5]=='Error':
            print('Error: cannot recognize the structure, see error info above. Pass.')
            continue
        elif structure[0:3]=='Row':
            I = int(structure[3:])
            for j in range(0,sheet.ncols):
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
            LL = titlepos(sheet,I,L,R)
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
            W=[]
            I = int(structure[3:])
            for i in range(0,sheet.nrows):
                W.append([])
                for j in range(0,sheet.ncols):
                    W[-1].append(sheet.cell(i,j).value)
            W = transpose(W)
            for j in range(0,len(W[0])):
                if isyear(W[I][j]) is True:
                    L = j
                    break
            for j in range(len(W[0])-1,0,-1):
                if isyear(W[I][j]) is True:
                    R = j
                    break
            Years = W[I][L:R+1]
                
            WT = [['Years']+Years+['Row']]
            LL = titlepos(W,I,L,R)
            for i in range(I+1,len(W)):
                if isemptyrow(W,i,L,R) is True:
                    continue
                else:
                    WT.append([W[i][LL]]+W[i][L:R+1])
                    WT[-1]=WT[-1]+[i+1]
            del W
            outbook = xlwt.Workbook()
            RLen = len(WT[0])
            for R in WT[1:]:
                outsheet = outbook.add_sheet('Row '+str(R[-1]))
                outsheet.write(0,0,'Years')
                outsheet.write(0,1,R[0])
                for i in range(1,RLen-1):
                    outsheet.write(i,0,WT[0][i])
                    outsheet.write(i,1,R[i])
            if NAME is None:
                outbook.save(dirout + sym + bookname + '_' + sheetnames[s] +'.xls')
            else:
                outbook.save(dirout + sym + NAME + '_' + sheetnames[s] +'.xls')
        """
        else:
            if (NAME is None):
                dirinter = transpose(sheet,bookname,sheetnames[s],sym,dirout)
                xlsparser(dirinter,dirout,bookname)
            else:
                dirinter = transpose(sheet,NAME,sheetnames[s],sym,dirout)
                xlsparser(dirinter,dirout,NAME)
            #os.remove(dirinter)
        """
        
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
    dirprep = prep(dirinter,dirout)
    if NAME is None:
        xlsparser(dirprep,dirout,bookname)
    else:
        xlsparser(dirprep,dirout,NAME)
        
    os.remove(dirinter)
    os.remove(dirprep)
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
        dirprep = prep(dirin,Dirout)
        xlsparser(dirprep,Dirout,bookname)
        os.remove(dirprep)
    elif (ext == 'csv'):
        if not os.path.exists(Dirout):
            os.makedirs(Dirout)
        csvparser(dirin,Dirout,bookname)
    else:
        Error = 'Error: Only support .xls .xlsx and .csv. Exit.'
        print(Error)
        return



""" --------Debug--------- """

#dirin = "/Users/yuwang/Documents/PPI/Downloader_Git/Sample_Data/vm202._1.csv"
#dirout = "/Users/yuwang/Documents/PPI/Downloader_Git/Parsed_Data"

#csvparser(dirin,dirout)
#xlsparser(dir,dirout)
#xlsparser(dirin,dirout)
#prep(dirin,dirout)
#parser(dirin,dirout)
#print('---------------------------------------------------------------------')
#dirin = "/Users/yuwang/Documents/PPI/Downloader_Git/Sample_Data/test.xlsx"
#parser(dirin,dirout)
#print('---------------------------------------------------------------------')
#dirin = "/Users/yuwang/Documents/PPI/Downloader_Git/Sample_Data/WTF.xlsx"
#parser(dirin,dirout)
#print('---------------------------------------------------------------------')
#dirin = "/Users/yuwang/Documents/PPI/Downloader_Git/Sample_Data/Regulations.xlsx"
#parser(dirin,dirout)













