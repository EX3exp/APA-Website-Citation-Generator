from requests import get, HTTPError, RequestException
from bs4 import BeautifulSoup
from datetime import datetime
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from json import loads as jsonloads
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
#from pyperclip import copy as clipcopy
from tkinter import Tk

version = '1.1.0'

def make_APA_citation(url: str):
    try: 
        response = get(url)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        title_ = soup.title.string.strip()

        date_now = datetime.now()
        citation = f"{title_}[웹사이트].({date_now.year}.{date_now.month}.{date_now.day}). URL: {url}"
        return citation, True
    except HTTPError as e:
        status_code = e.response.status_code
        error_message = "해당 URL에 접속하는 과정에서 오류가 발생했어요."
        if status_code == 404:
            error_message = "존재하지 않는 URL이에요."
        elif status_code == 500:
            error_message = "웹 서버에 문제가 있어요."
        elif status_code == 403:
            error_message = "이 URL에 대한 접근이 막혀 있어요."
        elif status_code == 400:
            error_message = "접근 요청 보내기에 실패했어요."
        elif status_code == 401:
            error_message = "접근 권한이 없어요."
        elif status_code == 410:
            error_message = "사용 불가능한 URL이에요."
        elif status_code == 414:
            error_message = "URL이 너무 길어서 서버가 거부했어요."
        elif status_code == 502:
            error_message = "게이트웨이 상태가 나빠요. 서버에 과부하가 걸렸을 수 있어요."
        elif status_code == 503:
            error_message = "서버가 멈췄어요. 서버가 터졌거나, 잠시 점검중인 것 같아요."

        citation = f'[🫠HTTPError {e.response.status_code}: {error_message}]'
        return citation, False
    except RequestException as e:
        citation = f"[🫠RequestException: {type(e).__name__}]"
        return citation, False
    except Exception as e:
        citation = f"[🫠{type(e).__name__}: {str(e)}]"
        return citation, False
    
# def make_APA_citation_with_author(url: str):
#     '''짜다 만 코드'''
#     try: 
#         response = get(url)
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
        self.actionUpdateCheck.triggered.connect(lambda: self.check_update(True))

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
    #     clipcopy(self.toCopy)
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
    
    def check_update(self, version_check: bool):
        owner = "EX3exp"
        repo = "APA-Website-Citation-Generator"

        api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
        response = get(api_url)

        if response.status_code == 200:
            response_text = response.text
            release_info = jsonloads(response_text)

            latest_version = release_info["tag_name"][1:]

            if latest_version != version:
                download_link = f"https://github.com/EX3exp/APA-Website-Citation-Generator/releases/download/v{latest_version}/APAGenerator{latest_version}.zip"
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setWindowIcon(icon)
                msg_box.setWindowTitle(f"v{version} → v{latest_version}")
                msg_box.setText(f"🤔출처생성기가 v{latest_version}으로 업데이트되었어요!")
                msg_box.setInformativeText("바로 다운로드 링크로 이동할까요?")
                msg_box.addButton("✔️다운받으러 가기", QMessageBox.AcceptRole)
                msg_box.addButton("❌그냥 이대로 쓸래요", QMessageBox.RejectRole)

                result = msg_box.exec_()

                if result == QMessageBox.AcceptRole:
                    QDesktopServices.openUrl(QUrl(download_link))
            elif version_check:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setWindowIcon(icon)
                msg_box.setWindowTitle(f"v{version}")
                msg_box.setText(f"😎출처생성기가 현재 최신 버전이에요.")
                msg_box.addButton("✔️알았어요", QMessageBox.RejectRole)

                result = msg_box.exec_()
            else:
                pass
        elif version_check:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowIcon(icon)
            msg_box.setWindowTitle(f"v{version}")
            msg_box.setText(f"🫠오, 이런. 오류가 발생해 업데이트 체킹에 실패했어요.")
            msg_box.addButton("🫠알았어요", QMessageBox.RejectRole)

            result = msg_box.exec_()
        else:
            pass


if __name__ == '__main__':
    app = QApplication([])
    app.setStyle('Fusion')
    window = APAGen()

    icon = QIcon('icon.bmp')
    window.setWindowIcon(icon)
    window.setWindowTitle(f'출처생성기 - 웹사이트 APA 출처 생성기 v{version}')
    window.show()
    window.check_update(False)
    app.exec_()
    
