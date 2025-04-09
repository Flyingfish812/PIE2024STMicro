
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def visualize(df,numerical_columns ):
  fig, axes = plt.subplots(3, 2, figsize=(12, 18))  # 12" wide, 18" tall
  axes = axes.flatten()  # Flatten for easy iteration

  # Plot each numerical feature in a subplot
  for i, col in enumerate(numerical_columns):
      ax = axes[i]
      # Get unique Cross Reference Types for coloring
      unique_types = df['Cross Reference Type'].unique()
      
      # Plot scatter points for each Cross Reference Type with transparency and contour
      for type_val in unique_types:
          mask = df['Cross Reference Type'] == type_val
          ax.scatter(
              df.loc[mask, col], 
              df.loc[mask, col + '_comp'], 
              label=type_val,
              alpha=0.5,           # Transparency to handle overlapping points
              edgecolor='0.5',     # Light black (medium gray) contour
              linewidth=0.5,       # Thin contour line
              s=20                 # Smaller marker size to reduce overlap
          )
      
      # Set title and labels
      ax.set_title(col, fontsize=10)
      ax.set_xlabel('Base Product', fontsize=9)
      ax.set_ylabel('Compared Product', fontsize=9)
      
      # Ensure equal scaling for x and y axes
      xlim = ax.get_xlim()
      ylim = ax.get_ylim()
      overall_min = min(xlim[0], ylim[0])
      overall_max = max(xlim[1], ylim[1])
      ax.set_xlim(overall_min, overall_max)
      ax.set_ylim(overall_min, overall_max)
      
      # Add diagonal reference line (y = x)
      ax.plot([overall_min, overall_max], [overall_min, overall_max], 'k--', alpha=0.5)

  # Hide the sixth subplot and use it for the legend
  axes[5].axis('off')
  handles, labels = axes[0].get_legend_handles_labels()  # Get legend from first subplot
  axes[5].legend(handles, labels, loc='center', title='Cross Reference Type')

  # Adjust layout to prevent overlap
  fig.tight_layout()

  # Display the plot
  plt.show()
def export_matrix(data, name="Closeness_Matrix.png" ):
  data = np.clip(data, 0, 1)
  plt.imshow(data, cmap='viridis', interpolation='nearest')
  plt.colorbar(label="Value")
  plt.title(name)
  plt.savefig(name, dpi=1835)
  plt.close()  # Free memory
if __name__=="__main__":
  print("Visualize library")