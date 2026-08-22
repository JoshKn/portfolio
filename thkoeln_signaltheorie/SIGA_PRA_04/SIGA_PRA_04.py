import numpy.random as np
import numpy
import matplotlib.pyplot as plt
import seaborn as sns

""" 1.  Schreiben Sie eine Funktion, die n Würfe mit einem 6-seitigen Würfel simuliert und als
    Ergebnis die absoluten Häufigkeiten zurück gibt. Dabei soll n als Parameter übergeben
    werden. Ein weiterer optionaler Parameter sollen die Wahrscheinlichkeiten für die sechs
    Seiten sein, der Standard wäre hier jeweils 1/6 für einen fairen Würfel. Mit abweichenden
    Werten ließe sich aber auch ein gezinkter Würfel simulieren. """

def simulate_dice(n: int, loaded_probability = 1/6, side_affected = 1): 
    die = numpy.array([i for i in range(1, 7)])
    possibilities = numpy.array([1/6 for _ in range(6)]) # normal probabilities

    # if die is loaded
    if not loaded_probability == 1/6:
        possibilities = numpy.array([(1-loaded_probability)/5 for _ in range(6)]) # assign every side the reduced probability
        possibilities[side_affected - 1] = loaded_probability # assign the loaded side the loaded probability
    
    # throw die n times
    dice_throws = numpy.array([np.choice(die, p=possibilities) for _ in range(n)])

    # return absolute frequency
    abs_frequency = []
    for i in range(6):
        abs_frequency.append(numpy.count_nonzero(dice_throws == i+1))
    
    return abs_frequency

""" 2.  Schreiben Sie eine Funktion, die die absoluten Häufigkeiten Hi aus einer Simulation (s.o.)
    entgegennimmt und den folgenden Kennwert berechnet: V = Sum_(i=1)^6((H_i - E)^2 / E)
    dabei bezeichnet E die erwartete Häufigkeit jeder Zahl, also hier E = 1/6 n """

def calculate_v(absolute_frequencies):
    e = 1/6 * sum(absolute_frequencies) # E = erwartete Häufigkeit. hier (1/6)*n wg 6 Würfel Seiten
    
    v = 0
    for i in range(6):
        v += numpy.square(absolute_frequencies[i] - e) / e

    return v

""" 3.  Schreiben Sie eine Funktion, die nacheinander m Simulationen (wie in Aufgabenteil 1
    programmiert) mit jeweils n Würfen durchführt. Nach jeder Simulation soll der zugehörige
    Kennwert V (Aufgabenteil 2) berechnet und gespeichert werden. """

def m_sims_n_dice(m_sims:int, n_dice:int, loaded_probability = 1/6, side_affected = 1):
    v_values = []
    for die in range(n_dice): 
        v = calculate_v(simulate_dice(m_sims, loaded_probability, side_affected))
        v_values.append(v)

    return v_values


""" 4.  Plotten Sie ein Histogramm (mit sinnvoller Einteilung) über die Werte von V . In welchem
    Intervall bzgl. V liegen 95% Ihrer Simulationen? """
#! Im Intervall zwischen 2 und 4

def plot_v(v_values):
    print(f"Mean value of V: {numpy.mean(v_values)}")
    
    sns.histplot(v_values)
    plt.show()

""" 5.  Ändern Sie nun das Experiment so, dass mit einem gezinkten Würfel gewürfelt wird, der
    z.B. doppelt so häufig eine 6 würfelt, wie man eigentlich erwarten dürfte. Erklären Sie, wie
    Sie das mit einem Testverfahren basierend auf V erkennen könnten. Welche Zuverlässigkeit
    (oder umgekehrt: welche Fehler) hat Ihr Test? """

plot_v(m_sims_n_dice(1000, 1000, loaded_probability=1/3, side_affected=6))
#plot_v(m_sims_n_dice(1000, 1000))