import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import scipy.signal as sig

# paths to files and dirs
folded_signal_path = "SIGA_PRA_02/Gefaltet/"
impulse_answer_path = "SIGA_PRA_02/Impulsantworten/"

signal_path = "SIGA_PRA_02/Signale/hochdeutsch.wav"

h_t_artificial = "Artificial"
h_t_discovery = "DiscoveryRoom"
h_t_yoga = "HaleHolisticYogaStudio"

# array of Impulsantworten
h_t = [h_t_artificial, h_t_discovery, h_t_yoga]

# read signal and store its data & samplerate
signal_data, signal_samplerate = sf.read(signal_path, always_2d=True, dtype="float64")

# iterate over Impulsantworten and convolve each one with signal_data
""" def conv(array):
    for i in array:
        data, samplerate = sf.read(f"{impulse_answer_path + i}.wav")
        answer = sig.convolve(signal_data, data)
        sf.write(f"{folded_signal_path + i}_gefaltet.wav", answer, samplerate) """
impulse_data, impulse_samplerate = sf.read(f"{impulse_answer_path + h_t_artificial}.wav")

answer = sig.convolve(signal_data, impulse_data)
max_answer = np.amax(answer)

# TODO how do i loop over every item in answer and scale it to fit between -1 & 1???
i = 0
for l in answer:
    i += 1
    for r in l:
        #answer[l] = answer[l] / max_answer
        print()

print(np.amax(answer))
print(answer.shape)

""" # --------------
# plot samples for the signal and its output after convolving
data, samplerate = sf.read(f"{impulse_answer_path + h_t[0]}.wav", dtype="float64")
answer = sig.convolve(signal_data, data)

x_1 = np.linspace(0, 1, len(answer))
x_2 = np.linspace(0, 1, len(signal_data))
y_signal = signal_data
y_impulse = data
y_conv = answer

print(f"Signal: {len(y_signal)}")
print(f"Impulse: {len(y_impulse)}")
print(f"Conv: {len(y_conv)}")

plt.plot(x_1, y_conv)
plt.plot(x_2, y_signal)
plt.show()
 """