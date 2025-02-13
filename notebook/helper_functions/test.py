import numpy as np
import pandas as pd
from tqdm import tqdm

def create_closeness_matrix(df_feat_scaled, model, output_path="closeness_matrix.npy"):
  """
  Creates a closeness matrix by performing a Cartesian product of df_feat_scaled with itself,
  predicting closeness for each pair, and storing results in a matrix.
  
  Parameters:
  - df_feat_scaled: DataFrame with scaled features (18,351 rows)
  - model: Trained model/pipeline to predict closeness
  - output_path: Path to save the resulting matrix
  
  Returns:
  - Path to saved numpy file
  """
  
  n = len(df_feat_scaled)  # Number of products
  matrix = np.zeros((n, n), dtype=np.float32)  # Initialize matrix
  
  # Convert DataFrame to numpy for faster operations
  df_f = df_feat_scaled.drop(columns=["MPN"])
  # features = df_f .values
  
  # Iterate over each product
  for i in tqdm(range(n), desc="Building closeness matrix"):
      # Get current product features
      product_i = df_f.iloc[i:i+1]
      merged_df = product_i.merge(df_f, how='cross',suffixes = ("","_comp"))
      # Create Cartesian product for current product
      # cartesian_features = np.hstack([
      #     np.repeat(product_i, n, axis=0),  # Repeat product i
      #     features  # Compare with all products
      # ])
      
      # Predict closeness for all pairs
      matrix[i, :] = model.predict(merged_df)
  
  # Save the matrix
  np.save(output_path, matrix)
  return output_path



if __name__ == "__main__":
  print("test module")

