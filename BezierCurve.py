import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, QRectF, QEvent


class MainWindow(QWidget):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setMouseTracking(True)
        self.installEventFilter(self)

        self.points = [(100, 400), (300, 200), (500, 200), (600, 400)]
        self.hand = -1
        self.press = False
        self.initUI()

    def initUI(self):
        self.resize(800, 800)
        self.show()

    def paintEvent(self, event):
        penter = QPainter()
        penter.begin(self)
        self.drawPoints(penter)
        self.drawline(penter)
        penter.end()

    def drawPoints(self, penter):
        pen = QPen(Qt.blue)
        pen.setWidth(2)
        penter.setPen(pen)
        for item in self.points:
            rect = QRectF(item[0] - 7, item[1] - 7, 10.0, 10.0)
            penter.drawEllipse(rect)

    def drawline(self, penter):
        pen = QPen(Qt.red)
        pen.setWidth(2)
        penter.setPen(pen)
        for item in range(1, 1000):
            p = item / 1000
            x = (-p ** 3 + 3 * p ** 2 - 3 * p + 1) * self.points[0][0] + (
            3 * p ** 3 - 6 * p ** 2 + 3 * p) * self.points[1][0] + (-3 * p ** 3 + 3 * p ** 2) *  self.points[2][0] + (
            p ** 3) * self.points[3][0]
            y = (-p ** 3 + 3 * p ** 2 - 3 * p + 1) * self.points[0][1] + (
            3 * p ** 3 - 6 * p ** 2 + 3 * p) * self.points[1][1] + (-3 * p ** 3 + 3 * p ** 2) *  self.points[2][1] + (
            p ** 3) * self.points[3][1]
            penter.drawPoint(x, y)

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseMove:
            if not self.press:
                if self.hand == -1:
                    for index, item in enumerate(self.points):
                        if abs(event.x() - item[0]) < 5 and abs(event.y() - item[1]) < 5:
                            self.setCursor(Qt.OpenHandCursor)
                            self.hand = index
                elif self.hand >= 0:
                    if abs(event.x() - self.points[self.hand][0]) > 5 or abs(event.y() - self.points[self.hand][1]) > 5:
                        self.setCursor(Qt.ArrowCursor)
                        self.hand = -1
            else:
                self.points[self.hand] = (event.x(), event.y())
                self.repaint()
        elif event.type() == QEvent.MouseButtonPress:
            if self.hand >= 0:
                self.setCursor(Qt.ClosedHandCursor)
                self.press = True
        elif event.type() == QEvent.MouseButtonRelease:
            if self.press:
                self.points[self.hand] = (event.x(), event.y())
                self.setCursor(Qt.OpenHandCursor)
                self.press = False
                self.repaint()

        return super(self.__class__, self).eventFilter(source, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    sys.exit(app.exec_())
