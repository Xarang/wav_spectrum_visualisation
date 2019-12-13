import matplotlib.pyplot as plt
import sys
import wave, csv
import numpy
from scipy import signal
from scipy.io import savemat

def get_output_name(filename):
    fields = filename.split('/')
    if len(fields) <= 1:
        return "output.wav.png"
    else:
        return "{s}.png".format(s=fields[len(fields) - 1])

program_name = sys.argv[0]
filename = sys.argv[1]
output_file = get_output_name(filename)

wr = wave.open(filename, 'rb')
n_frames = wr.getnframes()
sampling_rate = wr.getframerate()
frames = wr.readframes(n_frames)

count = 0
y = []
for frame in frames:
    y.append(int(frame))
#f, t, STFT = signal.stft(y)

ARR = numpy.array(y)

f, t, STFT = signal.spectrogram(ARR, sampling_rate)

plt.pcolormesh(t, f, STFT)
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')

plt.savefig(output_file)
print("{p}: outputted result in {s}".format(p=program_name, s=output_file))
