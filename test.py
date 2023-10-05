import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

# Modulation parameters
amplitude = 1.0                    # Amplitude of the carrier signal
carrier_frequency = 100.0         # Frequency of the carrier signal

# Time parameters
duration = 1.0                     # Duration of the signal in seconds
sampling_rate = 10000.0            # Sampling rate in Hz
time = np.linspace(0, duration, int(duration * sampling_rate), endpoint=False)

# Generate the modulating signal (meander)
modulating_signal = np.sign(np.sin(2 * np.pi * 2 * time))

# Generate the carrier signal
carrier_signal = amplitude * np.sin(2 * np.pi * carrier_frequency * time)

# Generate the modulated signal
modulated_signal = carrier_signal * modulating_signal

# Design a digital Butterworth low-pass filter
cutoff_frequency = 500.0  # Cut-off frequency in Hz
nyquist_frequency = 0.5 * sampling_rate
normalized_cutoff = cutoff_frequency / nyquist_frequency
b, a = butter(4, normalized_cutoff, btype='low', analog=False)

# Apply the low-pass filter to the modulated signal
filtered_signal = filtfilt(b, a, modulated_signal)

# Plot the modulating signal, modulated signal, and filtered signal
plt.figure(figsize=(10, 8))
plt.subplot(3, 1, 1)
plt.plot(time, modulating_signal, label='Modulating Signal (Meander)')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Modulating Signal')
plt.grid(True)
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(time, modulated_signal, label='Modulated Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Modulated Signal')
plt.grid(True)
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(time, filtered_signal, label='Filtered Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Filtered Signal (Low-Pass Filter)')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()