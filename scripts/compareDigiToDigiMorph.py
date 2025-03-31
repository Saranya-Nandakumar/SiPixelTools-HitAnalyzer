import ROOT
import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

def get_histograms(file_path):
    file = ROOT.TFile.Open(file_path)
    if not file or file.IsZombie():
        print(f"Failed to open file: {file_path}")
        return {}
    directory = file.Get("a")
    keys = directory.GetListOfKeys()
    
    histograms = {}
    
    for key in keys:
        name = key.GetName()
        obj = directory.Get(name)
        if obj:
            print(f"Found object: {obj.GetName()} of type {obj.ClassName()}")
            histograms[name] = obj
            histograms[name].SetDirectory(0)
        else:
            print(f"Skipping {key.GetName()}: Object is None")

    return histograms

def save_plot(plt, filename):
    if not os.path.exists("./plots"):
        os.makedirs("./plots")
    plt.savefig(f"./plots/{filename}.png")
    plt.close()

def plot(histograms1, histograms2, file1_label, file2_label):
    for name in histograms1.keys():
        if name in histograms2:
            h1 = histograms1[name]
            h2 = histograms2[name]


            if not h1 or not h2:
                print(f"Skipping {name}: One or both histograms are missing")
                continue

            hists_to_plot = {"hpixDetMap18", "hpixDetMap19"}

            if name not in hists_to_plot:
                continue

            if isinstance(h1, ROOT.TH1F) and isinstance(h2, ROOT.TH1F):

                bins = h1.GetNbinsX()
                x_vals = [h1.GetBinCenter(i) for i in range(1, bins + 1)]
                y_vals1 = [h1.GetBinContent(i) for i in range(1, bins + 1)]
                y_vals2 = [h2.GetBinContent(i) for i in range(1, bins + 1)]

                plt.figure(figsize=(8, 6))
                plt.plot(x_vals, y_vals1, label=file1_label, drawstyle="steps-mid")
                plt.plot(x_vals, y_vals2, label=file2_label, drawstyle="steps-mid", linestyle="dashed")
                plt.xlabel(name)
                plt.ylabel("Entries")
                plt.title(f"{name}")
                plt.legend()
                plt.grid(False)
                save_plot(plt, f"{name}")
                
            elif isinstance(h1, ROOT.TProfile) and isinstance(h2, ROOT.TProfile):
                bins = h1.GetNbinsX()
                x_vals = [h1.GetBinCenter(i) for i in range(1, bins + 1)]
                y_vals1 = [h1.GetBinContent(i) for i in range(1, bins + 1)]
                y_vals2 = [h2.GetBinContent(i) for i in range(1, bins + 1)]
                
                fig, axs = plt.subplots(1, 2, figsize=(12, 6))
                axs[0].plot(x_vals, y_vals1, drawstyle="steps-mid")
                axs[0].set_title(f"{file1_label}: {name}")
                axs[1].plot(x_vals, y_vals2, drawstyle="steps-mid")
                axs[1].set_title(f"{file2_label}: {name}")
                for ax in axs:
                    ax.set_xlabel(name)
                    ax.set_ylabel("Mean Value")
                    ax.grid(False)
                save_plot(plt, f"{name}")
                
            elif isinstance(h1, ROOT.TH2F) and isinstance(h2, ROOT.TH2F) :
                bins_x = h1.GetNbinsX()
                bins_y = h1.GetNbinsY()

                data1 = np.array([[h1.GetBinContent(i, j) for j in range(1, bins_y + 1)] for i in range(1, bins_x + 1)])
                data2 = np.array([[h2.GetBinContent(i, j) for j in range(1, bins_y + 1)] for i in range(1, bins_x + 1)])

                white_viridis = LinearSegmentedColormap.from_list('white_viridis', [
                    (0, '#ffffff'),
                    (1e-20, '#440053'),
                    (0.2, '#404388'),
                    (0.4, '#2a788e'),
                    (0.6, '#21a784'),
                    (0.8, '#78d151'),
                    (1, '#fde624'),
                ], N=256)

                fig, axs = plt.subplots(1, 2, figsize=(12, 6))
                im1 = axs[0].imshow(data1, aspect='auto', origin="lower", cmap=white_viridis)
                axs[0].set_title(f"{file1_label}: {name}")
                fig.colorbar(im1, ax=axs[0])
            
                im2 = axs[1].imshow(data2, aspect='auto', origin="lower", cmap=white_viridis)
                axs[1].set_title(f"{file2_label}: {name}")
                fig.colorbar(im2, ax=axs[1])
            
                save_plot(plt, f"{name}")

# Example usage
file1 = "./digis_histos.root"
file2 = "./digis_histos_morph.root"

histograms1 = get_histograms(file1)
histograms2 = get_histograms(file2)


plot(histograms1, histograms2, "Original", "Morphed")
