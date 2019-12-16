import matplotlib.pyplot as plt
import os
import sys
import wave
import numpy
from imageio import imwrite
from scipy import signal
from scipy.io import savemat
from PIL import Image

def get_output_name(filename):
    fields = filename.split('/')
    if len(fields) <= 1:
        return "output.wav.png"
    else:
        return "{s}.png".format(s=fields[len(fields) - 1])

# frames: frames read from wr over a 2 sec period (multiple channels)
# samples_in_frame: expected amount of samples to be found in 'frames'
# sampwidth: size (bytes) of each samples
# n_channels: amount of different channels in the audio
# TODO: figure out these args..
def get_sample_list(frames, samples_in_frames, sampwidth, n_channels):
    res = []
    it_frames = 0
    for i in range(samples_in_frames):
        for k in range(sampwidth):
            sum = 0
            sublist = []
            for j in range(n_channels):
                sublist.append(int(frames[it_frames + j * sampwidth]))
            it_frames += 1
            for sample in sublist:
                sum += sample
            sum /= len(sublist)
            res.append(sum)
    return numpy.array(res)

def binarize_image(filename):
    image_file = Image.open(filename)
    area = (80, 70, 577, 428)
    image = image_file.crop(area)
    image = image.convert('L')
    image = numpy.array(image)
    for i in range(len(image)):
        for j in range(len(image[0])):
            if (image[i][j] > 40): #THRESHOLD
                image[i][j] = 255
            else:
                image[i][j] = 0
    imwrite(filename, image)

program_name = sys.argv[0]
filename = sys.argv[1]
output_file = get_output_name(filename)

wr = wave.open(filename, 'rb')
n_frames = wr.getnframes()
sample_width = wr.getsampwidth()
n_channels = wr.getnchannels()
sampling_rate = wr.getframerate()
audio_length = 1 / sampling_rate * n_frames

print("wav audio infos:")
print("n_channels: {}".format(n_channels))
print("n_frames: {}".format(n_frames))
print("sample_width: {}".format(sample_width))
print("sampling_rate: {}".format(sampling_rate))
print("expected audio length (s): {}".format(audio_length))

# we will process the signal 2 sec by 2 sec
window_length = 2
samples_in_window_length = (sampling_rate) * window_length
frames_per_window_length = samples_in_window_length * sample_width * n_channels
if not os.path.isdir(output_file):
    os.mkdir(output_file)
for i in range (int(audio_length / window_length)):
    frames = wr.readframes(int(samples_in_window_length))
    if (len(frames) != frames_per_window_length):
        # dont treat final (incomplete) segment for now
        break
    ARR = get_sample_list(frames, samples_in_window_length, sample_width, n_channels)
    t, f, STFT = signal.spectrogram(ARR, sampling_rate)
    plt.pcolormesh(f, t, STFT)
    sample_name = "{dir}/{id}_{s}".format(dir = output_file, id = i, s = output_file)
    plt.savefig(sample_name)
    binarize_image(sample_name)

#print("{p}: outputted result in {s}".format(p=program_name, s=output_file))
