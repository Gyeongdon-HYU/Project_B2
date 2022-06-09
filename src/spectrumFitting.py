from . import filter as f
from . import model as m
import os
import numpy as np
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import warnings

warnings.simplefilter('ignore', np.RankWarning)


def specFitting(directory, index):
    # Spectrum (Ref. - Raw data & fitting data)

    path = os.path.basename(directory)
    root = ET.parse(directory).getroot()

    v = []
    for waveLengthSweep in root.findall('.//WavelengthSweep'):
        waveValues = []
        for child in waveLengthSweep:
            waveValues.append(list(map(float, child.text.split(','))))

        waveValues.append(waveLengthSweep.attrib['DCBias'])
        v.append(waveValues)

    plt.subplot(2, 3, 2)
    plt.plot(v[6][0], v[6][1], color='black', label="Fit ref polynomial O3")

    handle = []

    x = v[6][0]
    y = v[6][1]
    degree = 7
    model = np.poly1d(np.polyfit(x, y, degree))

    y2 = model(x)
    l, = plt.plot(x, y2, '--', color='red', label='degree 7')
    plt.title("Fitted ref. spec", fontsize=12)
    plt.xlabel('Wavelength [nm]', fontsize=12)
    plt.ylabel('Measured transmission [dB]', fontsize=12)
    plt.legend(ncol=2, loc="lower center")

    handle.append(l)
    r_fitting = r2_score(y, y2)
    m.appendresSpec(r_fitting)

    m.storeHandle(handle, index)