
import requests
import sys
from bs4 import BeautifulSoup
from datetime import datetime
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer
#import pyperclip
from tkinter import Tk

version = '1.0.0'

def make_APA_citation(url: str):
    try: 
        response = requests.get(url)
        status_code = response.status_code
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            title_ = soup.title.string.strip()

            date_now = datetime.now()
            citation = f"{title_}[웹사이트].({date_now.year}.{date_now.month}.{date_now.day}). URL: {url}"
            return citation, True
        else : 
            citation = f'[🫠Error: {status_code}] 입력된 url에 문제가 있어요.'
            return citation, False
    except Exception as e:
        citation = f"[🫠Error: {type(e).__name__}]"
        return citation, False
    
# def make_APA_citation_with_author(url: str):
#     '''짜다 만 코드'''
#     try: 
#         response = requests.get(url)
#         status_code = response.status_code
#         if response.status_code == 200:
#             html = response.text
#             soup = BeautifulSoup(html, 'html.parser')
#             title_ = soup.title.string.strip()

#             if url.split('/')[-2].split('.')[-2] == 'tistory':
#                 author_data = soup.find("meta", attrs={"property": "og.article.author"})
#                 date_data = soup.find("meta", attrs={"property": "article:published_time"})
#                 date_ = date_data["content"].strip().split('-')[0] if date_data else "연도미상"
#             elif url.split('/')[-2].split('.')[-3] == 'blog' and url.split('/')[-2].split('.')[-2] == 'naver':
#                 author_data = soup.find("meta", attrs={"property": "naverblog:nickname"})
#                 date_data = soup.find("meta", attrs={"name": "date"})
#                 date_= date_data["content"].strip() if date_data else "연도미상"
#             else:
#                 author_data = soup.find("meta", attrs={"name": "author"})
#                 date_data = soup.find("meta", attrs={"name": "date"})
#                 date_= date_data["content"].strip() if date_data else "연도미상"
#             author_= author_data["content"].strip() if author_data else "저자미상"

            

#             citation = f"{author_}. ({date_}). {title_}. {url}"
#             return citation
#         else : 
#             citation = f'[🫠Error: {status_code}] 입력된 url에 문제가 있어요.'
#             return citation
#     except Exception as e:
#         citation = f"[🫠Error: {type(e).__name__}]"
#         return citation

class APAGen(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('interface.ui', self)
        self.initUi()
        self.toCopy = ''
    
    def send_toCopy(self, text: str):
        self.toCopy = text

    def initUi(self):
        self.buttonCopy.setDisabled(True)
        self.textInput.textChanged.connect(self.update_line_count)
        self.buttonGo.clicked.connect(self.make_citation)
        self.buttonCopy.clicked.connect(self.copy_to_clipboard)
        self.labelCopyCompleted.hide()
        self.pBarGo.hide()

    def update_line_count(self):
        text = self.textInput.toPlainText()
        line_count = len(text.split())
        self.labelLineCount.setText(f'{line_count}')


    def make_citation(self):
        result_list = []
        progress_ok = False
        self.buttonCopy.setDisabled(True)
        self.textOutput.clear()
        input = self.textInput.toPlainText()
        urls = input.split()
        self.pBarGo.setValue(0)
        if len(urls) - 1 == -1:
            progress_ok = False
        else:
            progress_ok = True
            
        if progress_ok: 
            self.pBarGo.setMaximum(len(urls) - 1)
            self.pBarGo.show()
        else:
            self.pBarGo.hide()

        for i, url in enumerate(urls):
            if progress_ok:
                self.pBarGo.setValue(i)
                QApplication.processEvents()
                result_ = make_APA_citation(url)
            self.textOutput.append(result_[0])
            if result_[1]:
                result_list.append(result_[0])
            
        self.send_toCopy(f'\n'.join(result_list))

        if len(result_list) != 0:
            self.buttonCopy.setDisabled(False)
        self.pBarGo.hide()

    # def copy_to_clipboard(self):
    #     pyperclip.copy(self.toCopy)
    #     self.labelCopyCompleted.show()
    #     QTimer.singleShot(2100, self.labelCopyCompleted.hide)



    def copy_to_clipboard(self):
        r = Tk()
        r.withdraw()
        r.clipboard_clear()
        r.clipboard_append(self.toCopy)
        r.update()
        r.destroy()
        self.labelCopyCompleted.show()
        QTimer.singleShot(2100, self.labelCopyCompleted.hide)     

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = APAGen()

    icon = QIcon('icon.bmp')
    window.setWindowIcon(icon)
    window.setWindowTitle(f'출처생성기 - 웹사이트 APA 출처 생성기 v{version}')
    window.show()
    app.exec_()
    



