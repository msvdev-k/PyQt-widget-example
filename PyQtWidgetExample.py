# -*- coding: utf-8 -*-


# Импортируем системный модуль и модули PyQt
import sys

from PyQt5.QtCore import QSize, QPoint, QRect, Qt
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QComboBox, QLabel, QSpinBox,
                             QCheckBox, QGridLayout)
from PyQt5.QtGui import (QPen, QBrush, QPalette, QPainter,
                         QPainterPath, QLinearGradient,
                         QRadialGradient, QConicalGradient)


class RenderArea(QWidget):

    def __init__(self, parent=None):

        QWidget.__init__(self, parent)

        self.shape = "Polygon"

        self.pen = QPen()
        self.brush = QBrush()

        self.antialiased = False
        self.transformed = False

        self.setBackgroundRole(QPalette.Base)
        self.setAutoFillBackground(True)

        print("logicalDpiX: ", self.logicalDpiX())
        print("logicalDpiY: ", self.logicalDpiY())

        print("physicalDpiX: ", self.physicalDpiX())
        print("physicalDpiY: ", self.physicalDpiY())

        print("devicePixelRatio: ", self.devicePixelRatio())
        print("devicePixelRatioF: ", self.devicePixelRatioF())

    def sizeHint(self):
        return QSize(400, 200)

    def minimumSizeHint(self):
        return QSize(100, 100)

    def setShape(self, shape):
        self.shape = shape
        self.update()

    def setPen(self, pen):
        self.pen = pen
        self.update()

    def setBrush(self, brush):
        self.brush = brush
        self.update()

    def setAntialiased(self, antialiased):
        self.antialiased = antialiased
        self.update()

    def setTransformed(self, transformed):
        self.transformed = transformed
        self.update()

    def paintEvent(self, event):

        points = (
            QPoint(10, 80),
            QPoint(20, 10),
            QPoint(80, 30),
            QPoint(90, 70)
        )

        lDpiX = self.logicalDpiX()
        lDpiY = self.logicalDpiY()

        pDpiX = self.physicalDpiX()
        pDpiY = self.physicalDpiY()

        rect = QRect(10, 20, int(2 * lDpiX / 2.54), int(1.5 * lDpiY / 2.54))

        path = QPainterPath()
        path.moveTo(20, 80)
        path.lineTo(20, 30)
        path.cubicTo(80, 0, 50, 50, 80, 80)

        startAngle = 20 * 16
        arcLength = 120 * 16

        painter = QPainter(self)

        painter.setPen(self.pen)
        painter.setBrush(self.brush)

        if self.antialiased:
            painter.setRenderHint(QPainter.Antialiasing, True)

        for x in range(0, self.width(), 100):
            for y in range(0, self.height(), 100):

                painter.save()
                painter.translate(x, y)

                if self.transformed:
                    painter.translate(50, 50)
                    painter.rotate(60.0)
                    painter.scale(0.6, 0.9)
                    painter.translate(-50, -50)

                if self.shape == "Line":
                    painter.drawLine(rect.bottomLeft(), rect.topRight())

                elif self.shape == "Points":
                    painter.drawPoints(*points)

                elif self.shape == "Polyline":
                    painter.drawPolyline(*points)

                elif self.shape == "Polygon":
                    painter.drawPolygon(*points)

                elif self.shape == "Rectangle":
                    painter.drawRect(rect)

                elif self.shape == "Rounded Rectangle":
                    painter.drawRoundedRect(rect, 25, 25, Qt.RelativeSize)

                elif self.shape == "Ellipse":
                    painter.drawEllipse(rect)

                elif self.shape == "Arc":
                    painter.drawArc(rect, startAngle, arcLength)

                elif self.shape == "Chord":
                    painter.drawChord(rect, startAngle, arcLength)

                elif self.shape == "Pie":
                    painter.drawPie(rect, startAngle, arcLength)

                elif self.shape == "Path":
                    painter.drawPath(path)

                elif self.shape == "Text":
                    painter.drawText(rect, Qt.AlignCenter, "Qt by\nThe Qt Company")

                painter.restore()

        painter.setRenderHint(QPainter.Antialiasing, False)
        painter.setPen(self.palette().dark().color())
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(QRect(0, 0, self.width() - 1, self.height() - 1))


class Window(QWidget):

    def __init__(self):

        QWidget.__init__(self)

        self.renderArea = RenderArea()

        self.shapeComboBox = QComboBox()
        self.shapeComboBox.addItem("Polygon")
        self.shapeComboBox.addItem("Rectangle")
        self.shapeComboBox.addItem("Rounded Rectangle")
        self.shapeComboBox.addItem("Ellipse")
        self.shapeComboBox.addItem("Pie")
        self.shapeComboBox.addItem("Chord")
        self.shapeComboBox.addItem("Path")
        self.shapeComboBox.addItem("Line")
        self.shapeComboBox.addItem("Polyline")
        self.shapeComboBox.addItem("Arc")
        self.shapeComboBox.addItem("Points")
        self.shapeComboBox.addItem("Text")

        shapeLabel = QLabel("&Shape:")
        shapeLabel.setBuddy(self.shapeComboBox)

        self.penWidthSpinBox = QSpinBox()
        self.penWidthSpinBox.setRange(0, 20)
        self.penWidthSpinBox.setSpecialValueText("0 (cosmetic pen)")

        penWidthLabel = QLabel("Pen &Width:")
        penWidthLabel.setBuddy(self.penWidthSpinBox)

        self.penStyleComboBox = QComboBox()
        self.penStyleComboBox.addItem("Solid", Qt.SolidLine)
        self.penStyleComboBox.addItem("Dash", Qt.DashLine)
        self.penStyleComboBox.addItem("Dot", Qt.DotLine)
        self.penStyleComboBox.addItem("Dash Dot", Qt.DashDotLine)
        self.penStyleComboBox.addItem("Dash Dot Dot", Qt.DashDotDotLine)
        self.penStyleComboBox.addItem("None", Qt.NoPen)

        penStyleLabel = QLabel("&Pen Style:")
        penStyleLabel.setBuddy(self.penStyleComboBox)

        self.penCapComboBox = QComboBox()
        self.penCapComboBox.addItem("Flat", Qt.FlatCap)
        self.penCapComboBox.addItem("Square", Qt.SquareCap)
        self.penCapComboBox.addItem("Round", Qt.RoundCap)

        penCapLabel = QLabel("Pen &Cap:")
        penCapLabel.setBuddy(self.penCapComboBox)

        self.penJoinComboBox = QComboBox()
        self.penJoinComboBox.addItem("Miter", Qt.MiterJoin)
        self.penJoinComboBox.addItem("Bevel", Qt.BevelJoin)
        self.penJoinComboBox.addItem("Round", Qt.RoundJoin)

        penJoinLabel = QLabel("Pen &Join:")
        penJoinLabel.setBuddy(self.penJoinComboBox)

        self.brushStyleComboBox = QComboBox()
        self.brushStyleComboBox.addItem("Linear Gradient", Qt.LinearGradientPattern)
        self.brushStyleComboBox.addItem("Radial Gradient", Qt.RadialGradientPattern)
        self.brushStyleComboBox.addItem("Conical Gradient", Qt.ConicalGradientPattern)
        self.brushStyleComboBox.addItem("Solid", Qt.SolidPattern)
        self.brushStyleComboBox.addItem("Horizontal", Qt.HorPattern)
        self.brushStyleComboBox.addItem("Vertical", Qt.VerPattern)
        self.brushStyleComboBox.addItem("Cross", Qt.CrossPattern)
        self.brushStyleComboBox.addItem("Backward Diagonal", Qt.BDiagPattern)
        self.brushStyleComboBox.addItem("Forward Diagonal", Qt.FDiagPattern)
        self.brushStyleComboBox.addItem("Diagonal Cross", Qt.DiagCrossPattern)
        self.brushStyleComboBox.addItem("Dense 1", Qt.Dense1Pattern)
        self.brushStyleComboBox.addItem("Dense 2", Qt.Dense2Pattern)
        self.brushStyleComboBox.addItem("Dense 3", Qt.Dense3Pattern)
        self.brushStyleComboBox.addItem("Dense 4", Qt.Dense4Pattern)
        self.brushStyleComboBox.addItem("Dense 5", Qt.Dense5Pattern)
        self.brushStyleComboBox.addItem("Dense 6", Qt.Dense6Pattern)
        self.brushStyleComboBox.addItem("Dense 7", Qt.Dense7Pattern)
        self.brushStyleComboBox.addItem("None", Qt.NoBrush)

        brushStyleLabel = QLabel("&Brush:")
        brushStyleLabel.setBuddy(self.brushStyleComboBox)

        otherOptionsLabel = QLabel("Options:")
        antialiasingCheckBox = QCheckBox("&Antialiasing")
        transformationsCheckBox = QCheckBox("&Transformations")

        self.shapeComboBox.activated.connect(self.shapeChanged)

        self.penWidthSpinBox.valueChanged.connect(self.penChanged)
        self.penStyleComboBox.activated.connect(self.penChanged)
        self.penCapComboBox.activated.connect(self.penChanged)
        self.penJoinComboBox.activated.connect(self.penChanged)

        self.brushStyleComboBox.activated.connect(self.brushChanged)

        antialiasingCheckBox.toggled.connect(self.renderArea.setAntialiased)
        transformationsCheckBox.toggled.connect(self.renderArea.setTransformed)

        mainLayout = QGridLayout()
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(3, 1)
        mainLayout.addWidget(self.renderArea, 0, 0, 1, 4)
        mainLayout.addWidget(shapeLabel, 2, 0, Qt.AlignRight)
        mainLayout.addWidget(self.shapeComboBox, 2, 1)
        mainLayout.addWidget(penWidthLabel, 3, 0, Qt.AlignRight)
        mainLayout.addWidget(self.penWidthSpinBox, 3, 1)
        mainLayout.addWidget(penStyleLabel, 4, 0, Qt.AlignRight)
        mainLayout.addWidget(self.penStyleComboBox, 4, 1)
        mainLayout.addWidget(penCapLabel, 3, 2, Qt.AlignRight)
        mainLayout.addWidget(self.penCapComboBox, 3, 3)
        mainLayout.addWidget(penJoinLabel, 2, 2, Qt.AlignRight)
        mainLayout.addWidget(self.penJoinComboBox, 2, 3)
        mainLayout.addWidget(brushStyleLabel, 4, 2, Qt.AlignRight)
        mainLayout.addWidget(self.brushStyleComboBox, 4, 3)
        mainLayout.addWidget(otherOptionsLabel, 5, 0, Qt.AlignRight)
        mainLayout.addWidget(antialiasingCheckBox, 5, 1, 1, 1, Qt.AlignRight)
        mainLayout.addWidget(transformationsCheckBox, 5, 2, 1, 2, Qt.AlignRight)
        self.setLayout(mainLayout)

        self.shapeChanged()
        self.penChanged()
        self.brushChanged()
        antialiasingCheckBox.setChecked(True)

        self.setWindowTitle("Basic Drawing")

    def shapeChanged(self):
        self.renderArea.setShape(self.shapeComboBox.currentText())

    def penChanged(self):

        brush = QBrush(Qt.blue)

        width = self.penWidthSpinBox.value()
        style = self.penStyleComboBox.currentData()
        cap = self.penCapComboBox.currentData()
        join = self.penJoinComboBox.currentData()

        self.renderArea.setPen(QPen(brush, width, style, cap, join))

    def brushChanged(self):

        style = self.brushStyleComboBox.currentData()

        if style == Qt.LinearGradientPattern:

            linearGradient = QLinearGradient(0, 0, 100, 100)
            linearGradient.setColorAt(0.0, Qt.white)
            linearGradient.setColorAt(0.2, Qt.green)
            linearGradient.setColorAt(1.0, Qt.black)
            self.renderArea.setBrush(linearGradient)


        elif style == Qt.RadialGradientPattern:

            radialGradient = QRadialGradient(50, 50, 50, 70, 70)
            radialGradient.setColorAt(0.0, Qt.white)
            radialGradient.setColorAt(0.2, Qt.green)
            radialGradient.setColorAt(1.0, Qt.black)
            self.renderArea.setBrush(radialGradient)


        elif style == Qt.ConicalGradientPattern:

            conicalGradient = QConicalGradient(50, 50, 150)
            conicalGradient.setColorAt(0.0, Qt.white)
            conicalGradient.setColorAt(0.2, Qt.green)
            conicalGradient.setColorAt(1.0, Qt.black)
            self.renderArea.setBrush(conicalGradient)


        else:
            self.renderArea.setBrush(QBrush(Qt.green, style))


if __name__ == "__main__":
    # Создаём объект приложения Qt
    app = QApplication(sys.argv)

    wind = Window()
    wind.show()

    # Запускаем цикл обработки событий
    sys.exit(app.exec())
