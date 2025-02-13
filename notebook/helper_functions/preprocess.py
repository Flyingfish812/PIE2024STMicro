from sklearn.preprocessing import MinMaxScaler ,  StandardScaler, OneHotEncoder
import pandas as pd
from scipy.stats import norm
from sklearn.model_selection import train_test_split

def scale(df,columns, Scaler=None):
  """Normalize the columns of df"""
  if Scaler == None:
    Scaler = MinMaxScaler()
  df[columns] = Scaler.fit_transform(df[columns])
  return df,Scaler

def merge_datasets(df_feat,df_ref):
  """Merge the 2 datasets , repalce classes B+- C+- etc with B and C et filtre SF """
  df_stm = df_ref.merge(df_feat , left_on=["STMicro MPN","STMicro Name"], right_on=["MPN",	"MANUFACTURER"	])
  df_merged = df_stm.merge(df_feat , left_on=["Competitor MPN","Competitor Name"], right_on=["MPN",	"MANUFACTURER"	], suffixes = ("","_comp") )
  df_merged.drop(columns=["STMicro MPN","STMicro Name", "Competitor MPN","Competitor Name"],inplace = True)
  test  = df_feat.merge(df_feat, on=["MPN",	"MANUFACTURER"],suffixes = ("","_comp"))
  test["MPN_comp"]= test["MPN"]
  test["MANUFACTURER_comp"]= test["MANUFACTURER"]
  test["Cross Reference Type"] = "A"
  test = test.reindex(['Cross Reference Type', 'MPN', 'MANUFACTURER',
        'Maximum Input Offset Voltage', 'Maximum Single Supply Voltage',
        'Minimum Single Supply Voltage', 'Number of Channels per Chip',
        'Supplier_Package', 'Typical Gain Bandwidth Product', 'MPN_comp',
        'MANUFACTURER_comp', 'Maximum Input Offset Voltage_comp',
        'Maximum Single Supply Voltage_comp',
        'Minimum Single Supply Voltage_comp',
        'Number of Channels per Chip_comp', 'Supplier_Package_comp',
        'Typical Gain Bandwidth Product_comp'],axis=1)
  df_merged = pd.concat([df_merged,test])

  df_merged["Cross Reference Type"] = df_merged["Cross Reference Type"].replace("B/Downgrade","B")
  df_merged["Cross Reference Type"] = df_merged["Cross Reference Type"].replace("B/Upgrade","B")
  df_merged["Cross Reference Type"] = df_merged["Cross Reference Type"].replace("C/Downgrade","C")
  df_merged["Cross Reference Type"] = df_merged["Cross Reference Type"].replace("C/Upgrade","C")
  
  df_filtered = df_merged[~df_merged["Cross Reference Type"].isin(["SF"])] 

  return df_filtered


def generate_closeness(df, means, stds, distribution=norm, n_std=2, **dist_kwargs):
  """
  Generate 'Closeness' values based on the specified distribution and parameters.
  
  Parameters:
  - df: DataFrame containing the data.
  - means: Dictionary of means for each category.
  - stds: Dictionary of standard deviations for each category.
  - distribution: Distribution to use (default is normal distribution).
  - n_std: Number of standard deviations to use for interval calculation.
  - dist_kwargs: Additional keyword arguments for the distribution.
  
  Returns:
  - DataFrame with 'Mean', 'Std', and 'Closeness' columns added.
  """
  intervals = calculate_intervals(means, stds, n_std)
  lower_bounds = {k: interval[0] for k, interval in intervals.items()}
  upper_bounds = {k: interval[1] for k, interval in intervals.items()}
  
  # Map means and standard deviations
  df["Mean"] = df['Cross Reference Type'].map(means).fillna(0.0)
  df["Std"] = df['Cross Reference Type'].map(stds).fillna(0.0)
  
  # Vectorized generation of Closeness using the distribution
  df['Closeness'] = distribution.rvs(
      loc=df['Mean'],
      scale=df['Std'],
      size=len(df),
      **dist_kwargs
  )
  
  # Vectorized clipping using precomputed bounds
  df['lower'] = df['Cross Reference Type'].map(lower_bounds).fillna(0.0)
  df['upper'] = df['Cross Reference Type'].map(upper_bounds).fillna(1.0)
  df['Closeness'] = df['Closeness'].clip(lower=df['lower'], upper=df['upper'])
  
  # Remove temporary columns
  df.drop(columns=['lower', 'upper'], inplace=True)
  
  return df

def calculate_intervals(means, stds, n_std=2):
  """Calculate intervals based on mean and standard deviation."""
  return {
      key: (
          max(0, means[key] - n_std * stds[key]),
          min(1, means[key] + n_std * stds[key])
      )
      for key in means
  }

def split_dataframe(df, train_percent=0.8, validate_percent=0.05, test_percent=0.15, 
                    random_state=42, stratify_col="Cross Reference Type"):
  """
  Optimized stratified split of DataFrame into train/validate/test sets.
  Preserves class distribution in all splits using a single stratification step.
  """
  # Validate input percentages
  assert abs(train_percent + validate_percent + test_percent - 1) < 1e-9, "Percentages must sum to 1"

  # Create temporary stratified split to preserve distributions
  stratify = df[stratify_col] if stratify_col else None
  
  # Split into train and temp (validate + test) using exact integer sizes
  train_size = int(len(df) * train_percent)
  temp_size = len(df) - train_size
  
  train_df, temp_df = train_test_split(
      df,
      train_size=train_size,
      stratify=stratify,
      random_state=random_state
  )
  
  # Split temp into validate and test using relative percentages
  validate_ratio = validate_percent / (validate_percent + test_percent)
  validate_size = int(temp_size * validate_ratio)
  
  validate_df, test_df = train_test_split(
      temp_df,
      train_size=validate_size,
      stratify=temp_df[stratify_col] if stratify_col else None,
      random_state=random_state  # Maintain reproducibility
  )
  
  return train_df, validate_df, test_df

def balance_training_data(df_train,target_col="Cross Reference Type",
    ratios={"A": 4, "B": 3, "C": 1, "D": 1/3},random_state=42
):
  """
  Resamples training data using df.sample() for both upsampling and downsampling.
  
  Parameters:
  - df_train: Training DataFrame
  - target_col: Name of class column
  - ratios: Dictionary with class:multiplier pairs
  - random_state: For reproducibility
  
  Returns:
  - Resampled DataFrame with balanced classes
  """
  
  resampled = []
  
  for cls, ratio in ratios.items():
      class_data = df_train[df_train[target_col] == cls]
      target_size = int(len(class_data) * ratio)
      
      # Use df.sample() for both upsampling and downsampling
      resampled.append(
          class_data.sample(n=target_size, replace=(ratio > 1), random_state=random_state)
      )
  
  # Combine and shuffle
  balanced_df = pd.concat(resampled, ignore_index=True)
  return balanced_df.sample(frac=1, random_state=random_state).reset_index(drop=True)


if __name__=="__main__":
  print("Preprocess Module")
