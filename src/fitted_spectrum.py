from . import filter as f
from . import model
import os
import xml.etree.ElementTree as ET
import numpy as np
import warnings

warnings.simplefilter('ignore', np.RankWarning)
import matplotlib.pyplot as plt


def fitSpec(directory, index):
    # Spectrum (Processed interference spectrum)

    path = os.path.basename(directory)
    root = ET.parse(directory).getroot()

    v = []
    for waveLengthSweep in root.findall('.//WavelengthSweep'):
        waveValues = []
        for child in waveLengthSweep:
            waveValues.append(list(map(float, child.text.split(','))))

        waveValues.append(waveLengthSweep.attrib['DCBias'])
        v.append(waveValues)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        y_values = np.asarray(np.poly1d(np.polyfit(v[6][0], v[6][1], 6))(v[6][0]))

    variableValues = []
    for i in range(2, 8, 1):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            values = np.asarray(np.poly1d(np.polyfit(v[6][0], v[6][1], i))(v[6][0]))
        tempValue = []
        tempValue.append(v[6][0][values.argmax()])
        tempValue.append(v[6][1][values.argmax()])
        tempValue.append(v[6][0][values.argmin()])
        tempValue.append(v[6][1][values.argmin()])
        variableValues.append(tempValue)

    model.appendmaxRef(v[6][1][y_values.argmax()])

    y_values_new = v[6][1] - y_values

    plt.subplot(2, 3, 3)
    plt.title("REF fitting")
    plt.xlabel('Wavelength [nm]')
    plt.ylabel('Measured transmission [dB]')
    for i in range(len(v) - 1):
        array1 = np.array(v[i][1])
        array2 = np.array(y_values)
        if len(array1) == len(array2):
            subtracted_array = np.subtract(array1, array2)
            subtracted = list(subtracted_array)
        else:
            n = len(array1) - len(array2) if len(array1) > len(array2) else len(array2) - len(array1)
            v[i][0] = v[i][0][:-n]
            array1 = np.array(v[i][1][:-n])
            subtracted_array = np.subtract(array1, array2)
            subtracted = list(subtracted_array)
        plt.plot(v[i][0], subtracted, label="DCBias=\"" + str(v[i][2]) + "\"")

    line, = plt.plot(v[6][0], y_values_new, color='#3d3d3d', label="fitted REF")
    plt.title("Fitted Spectrum", fontsize=12)
    plt.xlabel('Wavelength [nm]', fontsize=12)
    plt.ylabel('Measured transmission [dB]', fontsize=12)
    plt.legend(handles=model.handle[index][0], ncol=2, loc="lower center")
