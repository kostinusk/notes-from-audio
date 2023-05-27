import math
import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
from math import log

# plt.rcParams['figure.dpi'] = 100
# plt.rcParams['figure.figsize'] = (9, 7)

change = (880.4 / 440) ** (1 / 12)

def Note_ofhz(Hz):
    return int((math.log(Hz, change)-55.80727485095236) // 1)


def Check4Sim(mass):
    Lenn = len(mass)
    k = 0
    i = 1
    while k < Lenn and i < len(mass) - 1:
        while mass[i][0] == mass[i - 1][0] and i < len(mass) - 1:
            mass[i - 1][1] += mass[i][1]
            mass.remove(mass[i])
            k += 1
        i += 1
        k += 1

    if Lenn > 1 and mass[-1][0] == mass[-2][0]:
        mass[-2][1] += mass[-1][1]
        mass.remove(mass[-1])
    return mass


def SubFFTPicks(fft_spec, freq):
    k = 0
    mass = []
    for i, f in enumerate(fft_spec):
        if f > 80 and freq[i] > 27:  # looking at amplitudes of the spikes higher than 350
            OneNoteTuple = [Note_ofhz(freq[i]), int(np.round(f))]
            # print('note = {} Hz; ampl = {} '.format(OneNoteTuple[0], OneNoteTuple[1]))
            mass.append(OneNoteTuple)
            k += 1

    mass = Check4Sim(mass)
    # print("----Всего пиков:" + str(len(mass)))
    return mass


smpFreq, sound = wavfile.read('C:\\Users\\Константин\\Downloads\\Calling-Home.wav')

sound = sound / 2.0 ** 15

signal = sound[:, 0]

signal = signal[:]
length_in_s = signal.shape[0] / smpFreq
print(signal.shape[0])
print(length_in_s)
# plt.subplot(2, 1, 1)
# plt.plot(signal, 'r')
# plt.xlabel("left channel, sample #")
# plt.tight_layout()
# plt.show()

Time_arr = np.arange(sound.shape[0]) / sound.shape[0] * length_in_s

fft_spectrum = np.fft.rfft(signal)
freq = np.fft.rfftfreq(signal.size, d=1. / smpFreq)

fft_spectrum_abs = np.abs(fft_spectrum)

# plt.plot(freq[:], fft_spectrum_abs[:])
# plt.xlabel("frequency, Hz")
# plt.ylabel("Amplitude, units")
# plt.show()

Discr_nums = int((length_in_s // 1 + 1) * 10)
print(type(Discr_nums))
Change_of_mass = signal.size // Discr_nums

BigMass = []

for i in range(Discr_nums):
    fft_spectrum = np.fft.rfft(signal[i * Change_of_mass:(i + 1) * Change_of_mass])
    freq = np.fft.rfftfreq(signal[i * Change_of_mass:(i + 1) * Change_of_mass].size, d=1. / smpFreq)
    fft_spectrum_abs = np.abs(fft_spectrum)

    # if i==64:
    #     plt.plot(freq[:], fft_spectrum_abs[:])
    #     plt.xlabel("frequency, Hz")
    #     plt.ylabel("Amplitude, units")
    #     plt.show()
    #     time.sleep(0.4)
    #     plt.close()

    mass = SubFFTPicks(fft_spectrum_abs, freq)

    print(' ╩ ' + 7 * ' ╩ ╩  ╩ ╩ ╩ ')
    str1 = '░'*(4+12*7)
    for Small_mas in mass:
        str1 = str1[:Small_mas[0]-1] + '█' + str1[Small_mas[0]:]
    print(str1)
    # print(f"{i}: {mass}")

    time.sleep(0.1)

    BigMass.append(mass)
