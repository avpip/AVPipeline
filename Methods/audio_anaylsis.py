import numpy as np
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import os
import subprocess
from scipy.io import wavfile

file_name = "tamil_song_unbadhil.wav"
prefix = file_name[:-4]
intervals = 5 #edit this
os.chdir("../audio_samples")
print(os.getcwd() + "/" + prefix)
if not os.path.exists(os.getcwd() + "/" + prefix):
    print(os.getcwd())
    print(os.mkdir(prefix))

    cmd = "ffmpeg -i " + file_name + " -f segment -segment_time " + str(
        intervals) + " -c copy " + prefix + "/" + prefix + "_out%03d.wav"

    subprocess.call(cmd, shell=True)
fs, data = wavfile.read(prefix + "/" + prefix + '_out029.wav')
print(len(data))
frequencies, times, spectrogram = signal.spectrogram(data[:, 1], fs)

plt.pcolormesh(times, frequencies, spectrogram)
#plt.imshow(spectrogram)
plt.ylabel('Frequency [Hz]')
plt.axis(ymin=0, ymax=3000)
plt.xlabel('Time ')

plt.show()
