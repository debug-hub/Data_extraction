import re
import pdfplumber
import os, shutil
from pdf_parser import data_extractor_numbers,data_extractor_alphanumeric,data_extractor_string
import sys
sys.path.append(r'C:\Users\acer\AppData\Local\Programs\Python\Python39\Lib\site-packages\aws_lib_')#AWSPATH

##import psycopg2
##conn= psycopg2.connect(database="lohia", user='postgres',password='1234',host='localhost',port='5432')
##cursor=conn.cursor()

from tabulate import tabulate
from aws_lib_.aws_ocr_main import main_call
import sys
import os
import openpyxl
from openpyxl import load_workbook
import os


def Trigger(input_path):
    output_path=r"D:\SequelString\SAP\NON_ASN_Extraction\output"     #WHERE TEXT FILE WILL BE SAVED output
    text=''
    os.chdir(output_path)
    print(input_path)
    main_call(input_path)
    
    text_all=''
    for file in os.listdir(r"D:\SequelString\SAP\NON_ASN_Extraction\output"): #output
        if file.endswith('text.txt'):
            print(file)
            text_=open(r"D:\SequelString\SAP\NON_ASN_Extraction\output\\"+file,'r')
            text_=text_.readlines()
            text_=' '.join(text_)
            text_all = text_all + text_

    for file in os.listdir(r"D:\SequelString\SAP\NON_ASN_Extraction\output"):
        os.remove(r"D:\SequelString\SAP\NON_ASN_Extraction\output\\"+file)

    return text_all

def extract_all(file_name):
    new_data=Trigger(file_name)
    new_data = ' '.join(new_data.split('\n'))
    print(new_data)
    data_dict = {}
    l = ['(', ')', '.', '/', '-']
    #Vendor_Name ,Invoice_Number , Invoice_Date , Po_Number ,Po_Date ,Lohia_Pan_Number ,Gstin_client ,Gstin_Lohia , Item_code ,Hsn_Sac_code ,Quantity ,
    #Rate_per_unit ,Total_value ,Grand_Total ,Vehicle_Number

    Invoice = data_extractor_alphanumeric(new_data,'TRACTOR PARTS',1,data_dict,'DATE.','Invoice No',l,'[A-Z]+/\d+\-\d+\/\d+', 0)
##    if Invoice == 0:
##        Invoice = data_extractor_alphanumeric(new_data,'Rajkot~Gondal',1,data_dict,'Delivery Note','Invoice No',l,'\w\d+', 1)
##    if Invoice == 0:
##        Invoice = data_extractor_alphanumeric(new_data,'Invoice No',1,data_dict,'Date','Invoice No',l,'\d+', 0)
##    if Invoice == 0:
##        Invoice = data_extractor_alphanumeric(new_data,'Invoice No.',1,data_dict,'Address','Invoice No',l,'\d+\/\d+', 0)(',ansc,jnsac')
##    if Invoice == 0:
##        Invoice = data_extractor_alphanumeric(new_data,'Invoice No',1,data_dict,'Invoice Dt','Invoice No',l,'\d+', 0)
    print('Invoice : ',Invoice)
    print('#######################  INVOICE  #####################')


##    Date = data_extractor_alphanumeric(new_data,'Dated ',1,data_dict,'Party GST','Date',l,'\d+/\d+/\d+', 0)
##    if Date == 0:
##        Date = data_extractor_alphanumeric(new_data,'Date',1,data_dict,'SYNNOVA GEARS','Date',l,'\d+\D+\d+', 0)
##    if Date == 0:
##        Date = data_extractor_alphanumeric(new_data,'Date',1,data_dict,'CHACK GUJRAN','Date',l,'\d+\/\d+\/\d+', 0)
##    if Date == 0:
##        Date = data_extractor_alphanumeric(new_data,'Invoice Date',1,data_dict,'Mode Of','Date',l,'\d+\-\d+\-\d+', 0)
##    if Date == 0:
##        Date = data_extractor_alphanumeric(new_data,'Invoice Dt ',1,data_dict,'Details of Receiver','Date',l,'\d+\-\D+\d+', 0)
##    print('Date : ',Date)    
##    print('#######################  DATE  #####################')
##
##
##
##    Amount = data_extractor_alphanumeric(new_data,'Total Amount',1,data_dict,'E  Bill Amount in Words','Amount',l,"\d+\,\d+\.\d+", 0)
##    if Amount == 0:
##        Amount = data_extractor_alphanumeric(new_data,'Total',1,data_dict,'Amount','Amount',l,'\d+\,\d+\.\d+', 0)
##    if Amount == 0:
##        Amount = data_extractor_alphanumeric(new_data,'GRAND TOTAL',1,data_dict,'Terms & Conditions','Amount',l,'\d+\.\d+', 0)
##    if Amount == 0:
##        Amount = data_extractor_alphanumeric(new_data,'GRAND TOTAL',1,data_dict,'I/We Certify','Amount',l,'\d+\,\d+\.\d+', 0)
##    if Amount == 0:
##        Amount = data_extractor_alphanumeric(new_data,'Grand Total :',1,data_dict,'Company Bank','Amount',l,'\d+\,\d+\,\d+\.\d+', 0)
##    print('Amount : ',Amount)    
##    print('#######################  Amount  #####################')
##
##
##    Vehicle = data_extractor_alphanumeric(new_data,' ',1,data_dict,'','Vehicle',l,'', 0)
##    if Vehicle == 0:
##        Vehicle = data_extractor_alphanumeric(new_data,'Date',1,data_dict,'SYNNOVA GEARS','Vehicle',l,'\d+\D+\d+', 0)
##    if Vehicle == 0:
##        Vehicle = data_extractor_alphanumeric(new_data,'Date',1,data_dict,'CHACK GUJRAN','Vehicle',l,'\d+\/\d+\/\d+', 0)
##    if Vehicle == 0:
##        Vehicle = data_extractor_alphanumeric(new_data,'Invoice Date',1,data_dict,'Mode Of','Vehicle',l,'\d+\-\d+\-\d+', 0)
##    if Vehicle == 0:
##        Vehicle = data_extractor_alphanumeric(new_data,'Invoice Dt ',1,data_dict,'Details of Receiver','Vehicle',l,'\d+\-\D+\d+', 0)
##    print('Vehicle : ',Vehicle)    
##    print('#######################  Vehicle  #####################')

##
##
##    Description = data_extractor_alphanumeric(new_data,'Dated ',1,data_dict,'Party GST','Description',l,'\d+/\d+/\d+', 0)
##    if Description == 0:
##        Description = data_extractor_alphanumeric(new_data,'Date',1,data_dict,'SYNNOVA GEARS','Description',l,'\d+\D+\d+', 0)
##    if Description == 0:
##        Description = data_extractor_alphanumeric(new_data,'Date',1,data_dict,'CHACK GUJRAN','Description',l,'\d+\/\d+\/\d+', 0)
##    if Description == 0:
##        Description = data_extractor_alphanumeric(new_data,'Invoice Date',1,data_dict,'Mode Of','Description',l,'\d+\-\d+\-\d+', 0)
##    if Description == 0:
##        Description = data_extractor_alphanumeric(new_data,'Invoice Dt ',1,data_dict,'Details of Receiver','Description',l,'\d+\-\D+\d+', 0)
##    print('Date : ',Date)    
##    print('#######################  Description  #####################')






for file in os.listdir(r'D:\SequelString\SAP\NON_ASN_Extraction\NON_ASN'):     #PATH OF THE FOLDER CONTAINING PDFS
    extract_all(r"D:\SequelString\SAP\NON_ASN_Extraction\NON_ASN\{}".format(file))    

