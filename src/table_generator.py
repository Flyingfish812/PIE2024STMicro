# Reference to notebook/EDA-Adam.csv
import pandas as pd
import os
from scipy.stats import norm
    
home = os.path.abspath(os.getcwd())

def get_params(category):
    base_means = {
        'A': 0.96,
        'B': 0.85,
        'C': 0.72
    }
    base_std={
        'A': 0.0107,
        'B': 0.0249,
        'C': 0.01779
    }
    parts = category.split('/')
    mean = base_means.get(parts[0], 0.0)
    std = base_std.get(parts[0], 0.0)
    for part in parts[1:]:
        if part == 'Upgrade':
            mean += 0.04
        elif part == 'Downgrade':
            mean -= 0.04
    return mean, std

def preprocess(file_1, file_2, output_file, with_gower = False):
    df1 = pd.read_csv(file_1)
    df2 = pd.read_csv(file_2)

    df_stm = df2.merge(df1, left_on='STMicro MPN', right_on='MPN', suffixes=('_ref', '_stm'))
    df_merged = df_stm.merge(df1, left_on='Competitor MPN', right_on='MPN', suffixes=('', '_comp'))

    removed_categories = ["SF","D"]
    df_filtered = df_merged[~df_merged["Cross Reference Type"].isin(removed_categories)]

    class_A = df_filtered[df_filtered["Cross Reference Type"] == "A"]
    class_B = df_filtered[df_filtered["Cross Reference Type"].isin(["B","B/Upgrade","B/Downgrade"])]
    class_C = df_filtered[df_filtered["Cross Reference Type"].isin(["C","C/Upgrade","C/Downgrade"])]
    n=20000
    random_state = 42
    class_B_downsampled = class_B.sample(n=n, random_state=random_state)
    class_C_downsampled = class_C.sample(n=n,random_state=random_state)
    class_A_oversample = class_A.sample(n=n,random_state=random_state, replace= True)
    df_sampled = pd.concat([class_A_oversample, class_B_downsampled, class_C_downsampled],axis=  0)

    df_sampled["Mean"] , df_sampled["Std"] = zip(*df_sampled["Cross Reference Type"].map(get_params))
    df_sampled['Closeness'] = df_sampled.apply(lambda row: norm.rvs(loc=row['Mean'], scale=row['Std']), axis=1)
    df_sampled['Closeness'] = df_sampled['Closeness'].clip(0, 1)

    # Gower Score Part
    if with_gower:
        categorical_descriptors = ['MANUFACTURER', 'Supplier_Package']
        numerical_descriptors = [
            'Maximum Input Offset Voltage',
            'Maximum Single Supply Voltage',
            'Minimum Single Supply Voltage',
            'Number of Channels per Chip',
            'Typical Gain Bandwidth Product'
        ]

        for desc in categorical_descriptors:
            comp_desc = f"{desc}_comp"
            similarity_col = f"{desc}_similarity"
            df_sampled[similarity_col] = (df_sampled[desc] == df_sampled[comp_desc]).astype(int)

        for desc in numerical_descriptors:
            comp_desc = f"{desc}_comp"
            similarity_col = f"{desc}_similarity"
            
            combined = pd.concat([df_sampled[desc], df_sampled[comp_desc]])
            desc_range = combined.max() - combined.min()
            
            if desc_range == 0:
                df_sampled[similarity_col] = 1
            else:
                df_sampled[similarity_col] = 1 - (df_sampled[desc] - df_sampled[comp_desc]).abs() / desc_range
                df_sampled[similarity_col] = df_sampled[similarity_col].clip(0, 1)  # Clip to [0, 1]

    df_sampled.to_csv(output_file, index=False)
    print(f"Combined table saved to {output_file}")

file1 = f'{home}\encoded data\opamps-features.csv'
file2 = f'{home}\encoded data\opamps-xref.csv'
output = f'{home}\encoded data\output-data.csv'
preprocess(file1, file2, output, with_gower=False)