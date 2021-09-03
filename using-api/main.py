from PyQt5.QtCore import QAbstractTableModel, QObject, QSize, QVariant, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QListWidgetItem,
    QMainWindow,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QStackedWidget,
    QTableView,
    QTextEdit,
    QToolBar,
    QVBoxLayout,
    QWidget
)
import sys
import pandas
from PublicAPISDK import StidSDK

class TableModel(QAbstractTableModel):
    def __init__(self, data, headerdata: list):
        QAbstractTableModel.__init__(self)
        self._data = data
        self._headerdata = headerdata
    
    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]
    
    def rowCount(self, index):
        return len(self._data)
    
    def columnCount(self, index):
        return len(self._data[0])
    
    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self._headerdata[section])
        else:
            return super().headerData(section, orientation, role=role)
    
    def get_data(self):
        return self._data

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("KIHSR STUDENT ID MANAGER")
        self.setMinimumSize(750, 500)

        self.sdk = StidSDK("c68aeb8f9d542f5ea683cacfd6fff4dec4610ee2")

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        #toobar
        self.toolBar = QToolBar()
        self.addToolBar(self.toolBar)
        self.toolBar.setIconSize(QSize(16,16))
        self.toolBar.addAction("Open file").triggered.connect(self.open_file_dlg)

        #Stacked pages
        self.table = QTableView()
        self.read_page = QWidget()
        self.central_widget.addWidget(self.read_page)
        self.read_page_ui()
        
        self.response_page = QWidget()
        self.central_widget.addWidget(self.response_page)
        self.response_page_layout = QVBoxLayout()
        self.response_page.setLayout(self.response_page_layout)
        self.message_log = QTextEdit()
        self.response_page_layout.addWidget(self.message_log)
        self.message_log.setReadOnly(True)
    
    def open_file_dlg(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Excel Sheets (*.xlsx);;" "All files (*.*)")
        if filename:
            pd = pandas.read_excel(filename)
            data = list()
            for stid in pd.values:
                row = list(stid)
                row[1] = str(stid[1])
                row[3] = str(stid[3])
                row[4] = stid[4].date().strftime('%Y/%m/%d')
                row[5] = stid[5].date().strftime('%Y/%m/%d')
                data.append(row)
            tableModel = TableModel(data, ['Name', 'NRC', 'Program', 'STID', 'Valid from', 'Valid to'])
            self.table.setModel(tableModel)
        
            self.central_widget.setCurrentIndex(0)
    
    def submit_data(self):
        data = self.table.model().get_data()
        if data:
            html = str()
            for item in data:
                form = {
                    "name": item[0],
                    "nrc": item[1],
                    "program": item[2],
                    "stid": item[3],
                    "valid_from": item[4],
                    "valid_to": item[5]
                }
                self.statusBar().showMessage(f"Submitting {form['name']}:{form['stid']}")
                response = self.sdk.add_stid(form)
                if response != None:
                    self.statusBar().showMessage(response['message'])
                    if response["success"]:
                        html += f"<p style='color: green;'>{response['message']}</p>"
                    else:
                        html += f"<p style='color: red;'>{response['message']}</p>"
                else:
                    print(self.sdk.messages)
            
            self.message_log.setHtml(html)
            self.central_widget.setCurrentIndex(1)
                
    def read_page_ui(self):
        layout = QVBoxLayout()
        self.read_page.setLayout(layout)
        layout.addWidget(self.table)

        submit_btn = QPushButton(text="Submit")
        layout.addWidget(submit_btn)
        submit_btn.clicked.connect(self.submit_data)

if __name__== "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())