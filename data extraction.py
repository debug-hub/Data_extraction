import re
import pdfplumber
import os, shutil
from pdf_parser import data_extractor_numbers,data_extractor_alphanumeric,data_extractor_string
import sys
sys.path.append(r"C:\Users\91969\AppData\Local\Programs\Python\Python39\Lib\site-packages\aws_lib_")#AWSPATH

import psycopg2
conn= psycopg2.connect(database="lohia", user='postgres',password='1234',host='localhost',port='5432')
cursor=conn.cursor()

from tabulate import tabulate
from aws_lib_.aws_ocr_main import main_call
import sys
import os
import openpyxl
from openpyxl import load_workbook
import os


def Trigger(input_path):
    output_path=r"C:\sequelstrings\lohiya\Lohia Invoices\Lohia Invoices\Shivam(S)\text"     #WHERE TEXT FILE WILL BE SAVED output
    text=''
    os.chdir(output_path)
    main_call(input_path)
    
    text_all=''
    for file in os.listdir(r"C:\sequelstrings\lohiya\Lohia Invoices\Lohia Invoices\Shivam(S)\text"): #output
        if file.endswith('text.txt'):
            print(file)
            text_=open(r"C:\sequelstrings\lohiya\Lohia Invoices\Lohia Invoices\Shivam(S)\text\\"+file,'r')
            text_=text_.readlines()
            text_=' '.join(text_)
            text_all = text_all + text_


    for file in os.listdir(r"C:\sequelstrings\lohiya\Lohia Invoices\Lohia Invoices\Shivam(S)\text"):
        os.remove(r"C:\sequelstrings\lohiya\Lohia Invoices\Lohia Invoices\Shivam(S)\text\\"+file)

    return text_all

def extract_all(file_name):
    new_data=Trigger(file_name)
    new_data = ' '.join(new_data.split('\n'))
    #print(new_data)
    data_dict = {}
    l = ['(', ')', '.', '/', '-']
    #Vendor_Name ,Invoice_Number , Invoice_Date , Po_Number ,Po_Date ,Lohia_Pan_Number ,Gstin_client ,Gstin_Lohia , Item_code ,Hsn_Sac_code ,Quantity ,
    #Rate_per_unit ,Total_value ,Grand_Total ,Vehicle_Number


    Vendor_Name = data_extractor_alphanumeric(new_data,'(ORIGINAL FOR RECIPIENT)  ',1,data_dict,'  Invoice No.','Vendor_Name',l,'\D+',0)
    print(Vendor_Name)

    Invoice_Number = data_extractor_alphanumeric(new_data,'Dated',1,data_dict,'LATOUCHE','Invoice_Number',l,'\d{4}',0)
    if Invoice_Number == 0:
        Invoice_Number = data_extractor_alphanumeric(new_data,' LATOUCHE ROAD',1,data_dict,'KANPUR','Invoice_Number',l,'\d{4}',0)
    print(Invoice_Number)

    Invoice_Date = data_extractor_alphanumeric(new_data,'Dated',1,data_dict,'LATOUCHE','Invoice_Date',l,'\d{1,2}\-[A-Za-z]+\-\d{4}',0)
    if Invoice_Date == 0:
        Invoice_Date = data_extractor_alphanumeric(new_data,' LATOUCHE ROAD',1,data_dict,'KANPUR','Invoice_Date',l,'\d{1,2}\-[A-Za-z]+\-\d{4}',0)
    print(Invoice_Date)

    Po_Number = data_extractor_alphanumeric(new_data,"Buyer's Order No.",1,data_dict,'Lohia Corp.','Po_Number',l,'\d{10}',0)
    print(Po_Number)

    Po_Date = data_extractor_alphanumeric(new_data,'Order',1,data_dict,'Despatch','Po_Date',l,'\d{1,2}\-[A-Za-z]+\-\d{4}',0)
    print(Po_Date)

    Gstin_Lohia = data_extractor_alphanumeric(new_data,'GSTIN/UIN  :',1,data_dict,'State Name','Gstin_Lohia',l,'\S+',0)
    print(Gstin_Lohia)

    Lohia_Pan_Number = data_extractor_alphanumeric(new_data,'GSTIN/UIN  :',1,data_dict,'State Name','Lohia_Pan_Number',l,'[A-Z]+[0-9]+[A-Z]',0)
    print(Lohia_Pan_Number)

    Gstin_client = data_extractor_alphanumeric(new_data,'GSTIN/UIN:',1,data_dict,"Supplier's Ref",'Gstin_client',l,'\S+',0)
    print(Gstin_client)

    Grand_Total = data_extractor_alphanumeric(new_data,'Round Off  ',1,data_dict,'Amount Chargeable','Grand_Total',l,'[0-9/,/.]+',-1)
    if Grand_Total==0:
        Grand_Total = data_extractor_alphanumeric(new_data,'Total  ',1,data_dict,'  Amount Chargeable','Grand_Total',l,'[0-9/,/.]+',-1)
    print(Grand_Total)

    text= re.search('(?s)Amount.*?CGST',new_data).group()
    x=re.findall("\d{10}",text)
    item=[]
    for y in x:
        line= y.split()
        #print(line)
        item_code=line[0]
        item.append(item_code)


    #text=re.search('(?s)(ORIGINAL FOR RECIPIENT).*?(DUPLICATE FOR TRANSPORTER)',new_data).group()
    text1= re.search('(?s)Amount  No..*?CGST',new_data).group()
    lines=re.findall("\s\d{8}\s+[0-9\.\,]+\D+[0-9\,\.]+\s+\D+[0-9]+\D+[0-9\,\.]+",text1)
    for li in range (len(lines)):
            line= lines[li].split()
            #print(line)
            Hsn_Sac_code=line[0]
            Quantity=line[1]
            Rate_per_unit=line[3]
            Total_value=line[-1]
            Vehicle_Number='N/A'
            data_dict['Hsn_Sac_code']=Hsn_Sac_code
            data_dict['Quantity']=Quantity
            data_dict['Rate_per_unit']=Rate_per_unit
            data_dict['Total_value']=Total_value
            data_dict['Item_code']=item[li]
            data_dict['Vehicle_Number']=Vehicle_Number
            print(data_dict)
            query = "insert into lohia values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            value=(data_dict['Vendor_Name'],data_dict['Invoice_Number'],data_dict['Invoice_Date'],data_dict['Po_Number'],data_dict['Po_Date'],data_dict['Lohia_Pan_Number'],
                   data_dict['Gstin_client'],data_dict['Gstin_Lohia'],data_dict['Item_code'],data_dict['Hsn_Sac_code'],data_dict['Quantity'],data_dict['Rate_per_unit'],
                   data_dict['Total_value'],data_dict['Grand_Total'],data_dict['Vehicle_Number'])
            cursor.execute(query,value)   
            conn.commit()
            print("record inserted")

    
    
for file in os.listdir(r"C:\sequelstrings\lohiya\Lohia Invoices\Lohia Invoices\Shivam(S)\pdf"):     #PATH OF THE FOLDER CONTAINING PDFS
    extract_all(r"C:\sequelstrings\lohiya\Lohia Invoices\Lohia Invoices\Shivam(S)\pdf\\"+file)
