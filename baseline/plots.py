import matplotlib.pyplot as plt
import numpy as np
import os
from baseline.config import EXAMS

def plot_graphs(exam: str, model_perfomances: dict[str, dict[str, float]]) -> None:

    models = list(model_perfomances['all'].keys())
    tests = list(model_perfomances.keys())
    passing_threshold = EXAMS[exam]["passing_threshold"]

    colors = plt.cm.Set3(np.linspace(0, 1, len(models)))
    x = np.arange(len(models))
    y = np.arange(0, 101, 20)

    for i, test in enumerate(tests):
        performances = [100*model_perfomances[test][model] for model in models]

        fig, ax = plt.subplots(figsize=(12,8))
        ax.bar(x=x, height=performances, color=colors)

        if test == "all":
            ax.axhline(100*passing_threshold, color='red', linestyle='--', alpha=0.7, label='Passing threshold (70%)')
            plt.legend(loc='upper right', fontsize=18)
        
        plt.title(f"Test {test}" if test != 'all' else "Overall", fontsize=20)
        ax.set_yticks(y)
        ax.set_yticklabels(y, fontsize=16)
        ax.set_ylabel("Perfomance (%)", fontsize=20)
        ax.set_xticks(x)
        ax.set_xticklabels(models, rotation=35, ha='right', fontsize=18)
        plt.grid(True, axis='y', alpha=0.7)
        
        plt.tight_layout()
        plt.style.use('seaborn-v0_8-darkgrid')

        png_img_folder = "./reports/" + exam + "/figures/"
        if not os.path.exists(png_img_folder):
            os.makedirs(png_img_folder)
        eps_img_folder = png_img_folder + "eps_images/"
        if not os.path.exists(eps_img_folder):
            os.makedirs(eps_img_folder)
        plt.savefig(png_img_folder + f"test_{test}.png", format='png')
        plt.savefig(eps_img_folder + f"test_{test}.eps", format='eps')