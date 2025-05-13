
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from skimage.transform import resize

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


def export_matrix_downscaled(
    data,
    name="test.png",
    max_dim=10000 ,
    dpi=500,
    colormap='viridis'
):
    """
    Plots a large matrix but downscales it first to avoid enormous memory usage.
    Keeps the usual Matplotlib layout (axes, colorbar on right, etc.).
    
    Parameters:
    -----------
    data     : 2D numpy array
               The matrix you want to visualize.
    name     : str
               Output PNG filename.
    max_dim  : int
               Max height or width (in pixels) for the downscaled matrix.
    dpi      : int
               Output DPI. If you set this too high, you might end up with a huge file.
    colormap : str
               Matplotlib colormap (e.g., 'viridis', 'plasma', etc.).
    """
    data = np.clip(data, 0, 1)  # ensure values in [0,1]

    h, w = data.shape
    largest_side = max(h, w)

    # If matrix is bigger than max_dim in either dimension, downscale
    if largest_side > max_dim:
        scale_factor = max_dim / float(largest_side)
        new_h = int(h * scale_factor)
        new_w = int(w * scale_factor)
        print(f"Downscaling from ({h}, {w}) to ({new_h}, {new_w}) ...")
        data = resize(data, (new_h, new_w), anti_aliasing=True)
    else:
        # Already small enough
        new_h, new_w = h, w
        print(f"Matrix is already within {max_dim}×{max_dim} bounds. Shape: ({h}, {w})")

    # --- Plot with Matplotlib ---
    fig, ax = plt.subplots(figsize=(8, 8), dpi=dpi)
    img_obj = ax.imshow(data, cmap=colormap, interpolation='nearest', origin='upper')
    
    # Add colorbar on the right
    cbar = plt.colorbar(img_obj, ax=ax)
    cbar.set_label("Value", rotation=90)
    # plt.colorbar(label="Value")
    # plt.title(name)
    ax.set_title(name)

    # Optional: set ticks to reflect original data indices if you want
    # Just be aware that for a large matrix the ticks might overlap
    # The code below sets 10 ticks (including 0 and max):
    
    tick_vals = np.arange(0, 17501, 2500)  # 0, 2500, ..., 17500

    # Rescale them to match the downscaled data shape
    xticks = (tick_vals / (w - 1)) * (new_w - 1)
    yticks = (tick_vals / (h - 1)) * (new_h - 1)

    # Apply ticks to axes
    ax.set_xticks(xticks)
    ax.set_xticklabels(tick_vals)

    ax.set_yticks(yticks)
    ax.set_yticklabels(tick_vals)

    plt.tight_layout()
    plt.savefig(name, dpi=dpi)
    plt.close()
    print(f"Saved {name} at ~({new_w}x{new_h}) px, dpi={dpi}.")





if __name__=="__main__":
  print("Visualize library")