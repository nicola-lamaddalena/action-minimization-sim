import sys
import numpy as np
import numpy.typing as npt
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt, QTimer
import pyqtgraph as pg

def total_action(points: npt.NDArray[np.float64], dt: float, m: float, k: float) -> float:
    x_left, x_right = points[:-1], points[1:]
    v = (x_right - x_left) / dt
    x_mean = 0.5 * (x_left + x_right)
    lag = 0.5 * (m * v**2 - k * x_mean ** 2)

    return dt * np.sum(lag)

def minimum(m: float, k: float, dt: float, xa: npt.NDArray[np.float64], xb: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
    return 0.5 * (xa + xb) * ((4*m + k*dt**2) / (4*m - k*dt**2))
# ...

class Simulation(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Real-Time action minimization")
        self.resize(800, 600)

        self.m = 1
        self.k = 2
        self.x0, self.xf = 0, 1
        self.t0 = 0
        self.tf = np.floor(2 * np.pi * np.sqrt(self.m / self.k)) / 2
        self.N = 100
        self.dt = (self.tf - self.t0) / (self.N - 1)
        self.eps = 10e-9
        
        self.time_array = np.linspace(self.t0, self.tf, self.N)
        self.points = np.linspace(self.x0, self.xf, self.N) 
        self.S_old = total_action(self.points, self.dt, self.m, self.k)
        self.diff = 1.0

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)
        self.graphWidget.setTitle("Trajectory evolution")
        self.graphWidget.addLegend()
        self.graphWidget.setLabel('bottom', "Time", units='s')
        self.graphWidget.setLabel('left', "Position", units='m')
        

        self.points_initial = np.linspace(self.x0, self.xf, self.N)

        omega = np.sqrt(self.k / self.m)
        A = self.x0
        B = (self.xf - self.x0 * np.cos(omega * self.tf)) / np.sin(omega * self.tf)
        self.x_analytic = A * np.cos(omega * self.time_array) + B * np.sin(omega * self.time_array)

        self.graphWidget.plot(
            self.time_array, 
            self.points_initial, 
            pen=pg.mkPen(color=(150, 150, 150), width=1, style=Qt.PenStyle.DashLine), 
            name="Initial hypotesis"
        )

        self.graphWidget.plot(
            self.time_array, 
            self.x_analytic, 
            pen=pg.mkPen(color=(0, 255, 0), width=2), 
            name="Analytic solution"
        )

        self.linea_plot = self.graphWidget.plot(
            self.time_array, 
            self.points, 
            pen=pg.mkPen(color=(255, 0, 0), width=2), 
            symbol='o', 
            symbolSize=6,
            symbolBrush=(255, 0, 0),
            symbolPen=(255, 0, 0),
            name="Numeric Simulation"
        )

        self.timer = QTimer()
        self.timer.timeout.connect(self.step_and_draw)
        self.timer.start(16) 

        self.text_info = pg.TextItem(anchor=(1, 0))
        self.text_info.setParentItem(self.graphWidget.getViewBox())
        self.graphWidget.getViewBox().sigResized.connect(self.reposition_info_text)
        self.reposition_info_text()

        self.update_info_text(is_converged=False)

    def reposition_info_text(self):
        width = self.graphWidget.getViewBox().rect().width()
        self.text_info.setPos(width - 15, 15)

    def update_info_text(self, is_converged=False):
        diff_color = "#00ff00" if is_converged else "#ffffff"
        html_code = (
            f'<div style="font-family: monospace; font-size: 11pt; color: #ffffff;">'
            f'Action : {self.S_old:.6f}<br>'
            f'Diff   : <span style="color: {diff_color};">{self.diff:.2e}</span>'
            f'</div>'
        )
        self.text_info.setHtml(html_code)

    def step_and_draw(self):
        
        if self.diff > self.eps:
            for _ in range(75):
                self.points[1:-1] = minimum(self.m, self.k, self.dt, self.points[:-2], self.points[2:])
                self.S_new = total_action(self.points, self.dt, self.m, self.k)
                self.diff = np.abs(self.S_new - self.S_old)
                self.S_old = self.S_new
                
                if self.diff <= self.eps:
                    break

            self.linea_plot.setData(self.time_array, self.points)
            self.update_info_text(is_converged=False)
            
        else:
            self.timer.stop()
            self.update_info_text(is_converged=True)
            print("Convergenza raggiunta!")


app = QApplication(sys.argv)
window = Simulation()
window.show()
sys.exit(app.exec())
