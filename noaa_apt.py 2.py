import scipy.io.wavfile as wav
import scipy.signal as signal
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def decode(filename="NOAA-apt-sample3m.wav"):

    print("Importing wav file:",filename)
    fs,data = wav.read(filename)
    print("Freq of sampling:",fs)
    fs, data = resample_data(data,fs,2) 
    print("Demodulating signal using Hilbert transform...")
    data_am = hilbert(data)
    print("Demodulating done.")
    # plot_wav(data_am)
    print("Displaying image...")
    display_image(data_am,fs)


def plot_wav(datap):

    plt.figure(figsize=(12,4))
    plt.plot(datap)
    plt.xlabel("Samples")
    plt.ylabel("Amplitude")
    plt.title("Signal")
    plt.show()


def resample_data(data,fs,resample):
    # plot_wav(data)
    print("Resampling...")
    data = data[::resample]
    fs = fs//resample
    print("Resampling done.")
    return fs, data

def hilbert(data):

    analytical_signal = signal.hilbert(data)
    amplitude_envelope = np.abs(analytical_signal)
    return amplitude_envelope

def display_image(data_am,fs):

    print("Creating image...")
    frame_width = int(0.5 * fs)
    print("Frame width  = ", frame_width)
    w, h = frame_width, data_am.shape[0]//frame_width
    print("Width, Height:", w, h)
    image = Image.new('RGB', (w, h))
    px, py = 0, 0
    for p in range(7220,data_am.shape[0]): #Adjusted to start on data pixel 7220 in order to match the beginning of the Sync A block.
        lum = int(2* data_am[p]//127) # Quantization happens here.
        if lum < 0   : lum = 0
        if lum > 255 : lum = 255
        #print("p, lum:",p,lum)
        #print("px, Height:", w, h)
        image.putpixel((px, py), (lum, lum, lum))
        px += 1
        if px >= w:
            if (py % 10) == 0:
                print(f"Line saved {py} of {h}")
            px = 0
            py += 1
            if py >= h:
                break
    print("Image created.")
    image = image.resize((w, 4*h))
    print("Saving image...")
    image.save("decoded_NOAA_image.png")
    print("Image saved.")
    print("Showing image...")
    plt.imshow(image)
    plt.show()

    
