import numpy as np
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.io import wavfile
print(os.getcwd())
os.chdir("../audio_samples")
print(os.getcwd())
fs, data = wavfile.read('Bigbang_theory.wav')
print(fs)
print(len(data))