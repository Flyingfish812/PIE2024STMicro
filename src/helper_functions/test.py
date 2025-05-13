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
def create_closeness_matrix_nomodel(df_feat_scaled, df, closeness_column="Closeness", output_path="closeness_matrix.npy"):
    """
    Creates a closeness matrix (18k x 18k) using the comparisons DataFrame.
    If a comparison exists, the closeness value is used; otherwise, -1 is used.
    
    Parameters:
    - df_feat_scaled: DataFrame with all products (18k rows)
    - df: DataFrame with comparisons (1,023,192 rows) containing "MPN", "MPN_comp", and "Closeness"
    - closeness_column: Name of the column containing the closeness values
    - output_path: Path to save the resulting matrix
    
    Returns:
    - Path to saved numpy file
    """
    
    n = len(df_feat_scaled)  # Number of products (18k)
    matrix = np.full((n, n), 0, dtype=np.float32)  # Initialize matrix with -1
    
    # Create a mapping from product identifier (MPN) to matrix index
    product_to_index = {mpn: idx for idx, mpn in enumerate(df_feat_scaled["MPN"])}
    
    # Iterate through the comparisons DataFrame
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Building closeness matrix"):
        product_a = row["MPN"]
        product_b = row["MPN_comp"]
        closeness = row[closeness_column]
        
        # Get the indices of the products in the matrix
        idx_a = product_to_index.get(product_a)
        idx_b = product_to_index.get(product_b)
        
        # If both products exist in the mapping, populate the matrix
        if idx_a is not None and idx_b is not None:
            matrix[idx_a, idx_b] = closeness
            matrix[idx_b, idx_a] = closeness  # Assuming closeness is symmetric
    
    # Save the matrix
    np.save(output_path, matrix)
    return output_path
if __name__ == "__main__":
  print("test module")

