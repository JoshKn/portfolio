import matplotlib.pyplot as plt
import numpy as np
from pydub import AudioSegment
import scipy as sci

# 1. Audiosignal einlesen 
path_cuculus = "./SIGA_PRA_03/training_data/kuckuck/Cuculus canorus Call01.wav" # Call 1 bc min. amount of noise
path_fingilla = "./SIGA_PRA_03/training_data/singvogel/Fingilla Coelebs Call2_03.wav" # Call 3 works best
path_vulpes = "./SIGA_PRA_03/training_data/red_fox/Vulpes Vulpes Call_01.wav" # Call 1 bc. min amount background sounds

audio_cuculus = AudioSegment.from_file(path_cuculus)
audio_fingilla = AudioSegment.from_file(path_fingilla)
audio_vulpes = AudioSegment.from_file(path_vulpes)

cuculus_array = np.array(audio_cuculus.get_array_of_samples())
fingilla_array = np.array(audio_fingilla.get_array_of_samples())
vulpes_array = np.array(audio_vulpes.get_array_of_samples())

sample_rate = audio_cuculus.frame_rate # sample rate is the same for every item from training_data

# 1.1 Audiosignal sinnvoll darstellen
def plot_audio(audio):
    data = np.array(audio.get_array_of_samples())
    time = np.linspace(0, len(data)/sample_rate, num=len(data))

    plt.figure()
    plt.plot(time, data, "-")
    plt.legend()
    plt.xlabel("Time (s)")
    plt.ylabel("Signal")
    plt.show()

#plot_audio(audio_cuculus)
#plot_audio(audio_fingilla)
#plot_audio(audio_vulpes)

# 2.1 Betragsspektrum berechen
def calculate_fft(data):
    fft_result = sci.fft.fft(data)
    frequencies = sci.fft.fftfreq(len(data), d=1/sample_rate)

    signal = np.abs(fft_result)

    positive_freqs = frequencies[:len(frequencies)//2]
    positive_signal = signal[:len(signal)//2]

    return positive_freqs, positive_signal

# 2.2 Betragsspektrum darstellen
def plot_fft(data):
    freqs, signal = calculate_fft(data)

    plt.figure()
    plt.plot(freqs, signal, "-")
    plt.legend()
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Signal")
    plt.show()

#plot_fft(cuculus_array)
#plot_fft(fingilla_array)
#plot_fft(vulpes_array)


# 3. Tierstimmen & Tierarten zuordnen

# normalize array -> allows better comparison
def norm_arr(np_array):
    return (np_array - np.min(np_array)) / (np.max(np_array) - np.min(np_array))

def determine_animal(path):
    audio = AudioSegment.from_file(path)
    array = np.array(audio.get_array_of_samples())

    # calculate input fft
    input_freqs, input_signal = calculate_fft(array)

    # create animal list
    cuculus_freqs, cuculus_signal = calculate_fft(cuculus_array)
    fingilla_freqs, fingilla_signal = calculate_fft(fingilla_array)
    vulpes_freqs, vulpes_signal = calculate_fft(vulpes_array)
    
    animal_list = [["Cuculus Canorus", cuculus_freqs, cuculus_signal],
                   ["Fingilla Coelebs", fingilla_freqs, fingilla_signal],
                   ["Vulpes Vulpes", vulpes_freqs, vulpes_signal]]
    
    
    # compare input fft with fft of every animal in animal_list
    hit_list = []
    for i in range(len(animal_list)):
        input_signal = norm_arr(input_signal)
        animal = norm_arr(animal_list[i][2])

        # smooth both normed arrays => smoothing reduces sensitivity to small shifts in frequency
        smoothed_input = sci.ndimage.gaussian_filter1d(input_signal, sigma=5)
        smoothed_animal = sci.ndimage.gaussian_filter1d(animal, sigma=5)

        # fit both arrays to same length (fill shorter one with zeroes)
        if smoothed_input.size < smoothed_animal.size:
            smoothed_input = np.pad(smoothed_input, (0, smoothed_animal.size - smoothed_input.size), "constant", constant_values=0)
        else:
            smoothed_animal = np.pad(smoothed_animal, (0, smoothed_input.size - smoothed_animal.size), "constant", constant_values=0)

        # calculate difference
        smoothed_difference = np.abs(smoothed_input - smoothed_animal)
        difference = np.abs(smoothed_input - smoothed_animal)
        
        # 0=sum(smoothed_diff), 1=smoothed_diff, 2=diff, 3=name, 4=animal_signal, 5=smoothed_animal
        hit_list.append([np.sum(smoothed_difference), smoothed_difference, difference, animal_list[i][0], animal, smoothed_animal])

    hit_list.sort() # putting smallest smoothed_difference at [0]
    print(f"Your animal is a {hit_list[0][3]}!")

    fig, axis = plt.subplots(3)
    axis[0].plot(input_freqs[:len(input_freqs)//2], input_signal[:len(input_freqs)//2])
    axis[0].plot(input_freqs[:len(input_freqs)//2], smoothed_input[:len(input_freqs)//2], ":")
    axis[0].set_title("Input")
    axis[0].grid()
    axis[0].set_xlim([0, 500])

    axis[1].plot(input_freqs[:len(input_freqs)//2], hit_list[0][4][:len(input_freqs)//2]) # animal
    axis[1].plot(input_freqs[:len(input_freqs)//2], hit_list[0][5][:len(input_freqs)//2], ":") # smoothed_animal
    axis[1].set_title(f"{hit_list[0][3]}")
    axis[1].grid()
    axis[1].set_xlim([0, 500])

    axis[2].plot(input_freqs[:len(input_freqs)//2], hit_list[0][1][:len(input_freqs)//2]) # smoothed_difference
    axis[2].set_title("Difference")
    axis[2].grid()
    axis[2].set_xlim([0, 500])

    plt.xlabel("Frequency (Hz)") 
    plt.ylabel("Magnitude Difference")
    plt.show()



determine_animal("./SIGA_PRA_03/training_data/kuckuck/Cuculus canorus Call03.wav")