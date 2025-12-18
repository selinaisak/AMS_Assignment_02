import json
import matplotlib.pyplot as plt
from pathlib import Path
import sys
import numpy as np   # NEW: needed for grouped bar plots

LOG_DIR = Path("logs")
HAR_PLOT_DIR = Path("har_plots")

def load_har(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_video_chunks(har):
    chunks = []

    # Go through each entry (contains both request + response + etc.)
    for entry in har['log']['entries']:
        # Only care about entries about video data
        if entry.get('_resourceType') != 'media':
            continue

        # Grab the requested url + the response 
        url = entry['request']['url']
        response = entry['response']

        # This size includes both headers + body
        size = response.get('_transferSize') or 0  # In case it does not exist

        # This time includes all timings (send, wait, receive, etc.)
        duration = entry['time']  # in ms!!!

        # Calculate throughput in kilobits per second (size is in bytes!)
        if duration > 0:
            throughput_kbps = ((size * 8)/1024) / (duration/1000)
        else:
            throughput_kbps = 0

        chunks.append({
            'url': url,
            'size_MB': size / (1024*1024),
            'duration_ms': duration,
            'throughput_kbps': throughput_kbps
        })

    return chunks

def plot_chunks(chunks_per_network, title):
    # chunks_per_network is a dict: {network: [chunks]}
    networks = list(chunks_per_network.keys())

    # Determine how many chunks we need to display
    max_chunks = max(len(chunks) for chunks in chunks_per_network.values())

    x = np.arange(max_chunks)
    width = 0.8 / len(networks)

    fig, ax = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle(title)

    for i, network in enumerate(networks):
        chunks = chunks_per_network[network]

        # Display "missing" chunks as 0, in case there are less chunks than max_chunks
        while len(chunks) < max_chunks:
            chunks.append({
                'size_MB': 0,
                'duration_ms': 0,
                'throughput_kbps': 0
            })

        # Get size, duration and throughput per chunk
        sizes = [c['size_MB'] for c in chunks]
        durations = [c['duration_ms'] for c in chunks]
        throughput = [c['throughput_kbps'] for c in chunks]

        ax[0].bar(x + i * width, sizes, width, label=network)
        ax[1].bar(x + i * width, durations, width, label=network)
        ax[2].bar(x + i * width, throughput, width, label=network)

    labels = [f'Chunk {i+1}' for i in range(max_chunks)]

    # Center x-ticks under the group of bars
    group_centers = x + width * (len(networks)-1) / 2
    labels = [f'Chunk {i+1}' for i in range(max_chunks)]
    
    for axis in ax:
        axis.set_xticks(group_centers)
        # Tilt labels, so they do not overlap
        axis.set_xticklabels(labels, rotation=45, ha='right')
        axis.grid(axis="y", linestyle="--", alpha=0.6)
        
        # Add vertical lines between chunks (center of bar group)
        for i in range(len(group_centers) - 1):
            midpoint = (group_centers[i] + group_centers[i + 1]) / 2  # find middle between 2 centers
            axis.axvline(
                x=midpoint,
                color='gray',
                linestyle='-',
                alpha=0.6
            )

    ax[0].set_ylabel('Size (MB)')
    ax[0].set_title('Chunk Sizes')

    ax[1].set_ylabel('Time (ms)')
    ax[1].set_title('Download Time')

    ax[2].set_ylabel('Throughput (kbps)')
    ax[2].set_title('Throughput')

    ax[0].legend()

    plt.tight_layout()
    video = title.split('.')[0]
    plt.savefig(HAR_PLOT_DIR / f"{video}.png")
    plt.show()

def analyze_har_files(video):
    video_log_path = LOG_DIR / video
    chunks_per_network = {}   # Store chunks per network in a dictionary!

    for network in ["3G", "Slow_4G", "Fast_4G", "NT"]:
        har_path = str(video_log_path) + f"_{network}.har"
        print(har_path)

        har = load_har(har_path)
        chunks_per_network[network] = extract_video_chunks(har)

    title = f"{video}.mp4"

    plot_chunks(chunks_per_network, title)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        analyze_har_files(sys.argv[1])
    else:
        print(
            f"Wrong number of arguments.\n"
            f"Usage: python {Path(sys.argv[0]).name} <video number>\n"
        )
