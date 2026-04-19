import os
import matplotlib.pyplot as plt

def ensure_directories():
    folders = [
        "data/raw",
        "data/processed",
        "outputs/charts",
        "outputs/reports",
        "outputs/tables",
        "images"
    ]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

def save_line_chart(x, y, title, xlabel, ylabel, filepath):
    plt.figure(figsize=(10, 5))
    plt.plot(x, y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()