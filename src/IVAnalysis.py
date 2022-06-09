from . import model
import os
import numpy as np
import matplotlib.pyplot as plt
from lmfit import Parameters, minimize
from sklearn.metrics import r2_score
import xml.etree.ElementTree as ET


def showPara(directory):

    path = os.path.basename(directory)
    root = ET.parse(directory).getroot()

    v = []
    for child in root.find('.//IVMeasurement'):
        v.append(list(map(float, child.text.split(','))))

    V1 = np.array(v[0][0:9])
    I1 = np.array(np.abs(v[1])[0:9])
    V2 = np.array(v[0][10:])
    I2 = np.array(np.abs(v[1][10:]))

    model1 = np.poly1d(np.polyfit(V1, I1, 6))
    polyline = np.linspace(-2.0, 0.25, 10)


    def ivFit(params, V2, I2):
        I_S = params['I_S']
        VT = params['VT']
        model = I_S * (np.exp(V2 / VT))
        return model - I2

    params = Parameters()
    params.add('I_S', value=1e-15)
    params.add('VT', value=0.026)

    fitted_params = minimize(ivFit, params, args=(V2, I2,), method='leastsq')

    VT = fitted_params.params['VT'].value
    I_S = fitted_params.params['I_S'].value

    fittedDiagram = np.abs(I_S * (np.exp(V2 / VT) - 1))

    RI = np.concatenate((model1(polyline), np.abs(I_S * (np.exp(V2 / VT) - 1))))
    R2 = r2_score(np.abs(v[1]), RI)


    flag = False
    if R2 < 0.99:
        model1 = np.poly1d(np.polyfit(v[0], np.abs(v[1]), 6))
        polyline = np.linspace(-2.0, 1.0, 13)
        flag = True
        R2 = r2_score(np.abs(v[1]), model1(polyline))
    model.appendRsqIV(R2)


    plt.subplot(2, 3, 4)
    plt.plot(polyline, np.abs(model1(polyline)), color='red', label="fitted graph")
    plt.scatter(v[0], np.abs(v[1]), s=50, c='red', lw=2, label="IV data")
    if flag == False:
        plt.plot(v[0][9:11], np.abs(v[1][9:11]), c='red', lw=2, label=R2)
        plt.plot(V2, fittedDiagram, c='red', lw=2)
    plt.title("IV-Analysis", size=12)
    plt.xlabel('Voltage [V]', size=12)
    plt.ylabel('Current [A]', size=12)
    if flag == False:
        plt.yscale('logit')
    plt.legend()
    plt.grid(True)
    plt.suptitle('[Graph of analyzed data]', fontsize=20)
