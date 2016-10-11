# -*- coding: utf-8 -*-
#
# @author: Daemon Wang
# Created on 2016-06-12
#
import os
from cStringIO import StringIO
from PyPDF2 import PdfFileReader, PdfFileWriter
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument, PDFNoOutlines
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage, LTChar
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
import dxb.libs.utils as utils


def pdf_splite(source_file,filename,path):

    in_pdf = PdfFileReader(StringIO(source_file))
    counti = 0
    file_list = []
    num_list = []
    for page in in_pdf.pages:
        counti = counti + 1
        out_splited = PdfFileWriter()
        out_splited.addPage(page)
        name = str(utils.get_local_timestamp()) + '_' + filename.split(".")[0] + '_' + str(counti) + '.pdf'
        _path = os.path.join(path,name)
        ous = open(_path, 'wb')
        out_splited.write(ous)
        ous.close()
        file_list.append(name)
        num = get_num(_path)
        num_list.append(num)

    return file_list,num_list

def get_num(source_file):
    fp = open(source_file,'rb')
    # fp = StringIO(source_file)
    #创建一个PDF文档解析器对象
    parser = PDFParser(fp)
    #创建一个PDF文档对象存储文档结构
    #提供密码初始化，没有就不用传该参数
    document = PDFDocument(parser)
    #检查文件是否允许文本提取
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    #创建一个PDF资源管理器对象来存储共享资源
    rsrcmgr = PDFResourceManager()
    #创建一个pdf设备对象
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    #创建一个PDF解析器对象
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    #处理文档当中的每个页面
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layout = device.get_result()

        for n,l in enumerate(layout):
            if isinstance(l,LTTextBox):
                text = l.get_text()

                if n == 0:
                    pass

                elif n == 1:
                    num = text.split("：")[1].replace("\n",'')
                    return num
                else:
                    break