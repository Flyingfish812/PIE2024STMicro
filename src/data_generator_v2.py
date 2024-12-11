import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler
from scipy.stats import norm

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

def preprocess(file_1, file_2, output_file):
    df_feat = pd.read_csv(file_1) # features
    df_ref = pd.read_csv(file_2) # xref

    categorical_columns = ["Supplier_Package"]
    numerical_columns = ["Maximum Input Offset Voltage","Maximum Single Supply Voltage","Minimum Single Supply Voltage","Number of Channels per Chip","Typical Gain Bandwidth Product"]
    scaler = MinMaxScaler()
    df_feat[numerical_columns] = scaler.fit_transform(df_feat[numerical_columns] )

    df_stm = df_ref.merge(df_feat , left_on=["STMicro MPN","STMicro Name"], right_on=["MPN", "MANUFACTURER"])
    df_merged = df_stm.merge(df_feat , left_on=["Competitor MPN","Competitor Name"], right_on=["MPN", "MANUFACTURER"], suffixes = ("","_comp") )
    df_merged.drop(columns=["STMicro MPN","STMicro Name", "Competitor MPN","Competitor Name"],inplace = True)

    df_merged["Cross Reference Type"] = df_merged["Cross Reference Type"].replace("B/Downgrade","B")
    df_merged["Cross Reference Type"] = df_merged["Cross Reference Type"].replace("B/Upgrade","B")
    df_merged["Cross Reference Type"] = df_merged["Cross Reference Type"].replace("C/Downgrade","C")
    df_merged["Cross Reference Type"] = df_merged["Cross Reference Type"].replace("C/Upgrade","C")
    df_filtered = df_merged[~df_merged["Cross Reference Type"].isin(["SF"])]

    class_A = df_filtered[df_filtered["Cross Reference Type"] == "A"]
    class_B = df_filtered[df_filtered["Cross Reference Type"].isin(["B"])]
    class_C = df_filtered[df_filtered["Cross Reference Type"].isin(["C"])]
    class_D = df_filtered[df_filtered["Cross Reference Type"].isin(["D"])]
    n = 36926
    random_state = 42

    class_B_downsampled = class_B.sample(n=n, random_state=random_state)
    class_C_downsampled = class_C.sample(n=n, random_state=random_state)
    class_A_oversampled = class_A.sample(n=n, random_state=random_state, replace = True)
    class_D_downsampled = class_D.sample(n=n, random_state=random_state)

    df_sampled = pd.concat([class_A_oversampled, class_B_downsampled, class_C_downsampled, class_D_downsampled], axis=0)

    df_sampled["Mean"] , df_sampled["Std"] = zip(*df_sampled["Cross Reference Type"].map(get_params))
    df_sampled['Closeness'] = df_sampled.apply(lambda row: norm.rvs(loc=row['Mean'], scale=row['Std']), axis=1)
    df_sampled['Closeness'] = df_sampled['Closeness'].clip(0, 1)

    interval= {
        "A":(0.93,1),
        "B": (0.77,0.92),
        "C":(0.66,0.76),
        "D":(0.55,0.65)
    }

    for classe in interval:
        df_sampled.loc[df_sampled["Cross Reference Type"]==classe, "Closeness"] = df_sampled.loc[df_sampled["Cross Reference Type"]==classe, "Closeness"].clip(*interval[classe])

    for col in numerical_columns: 
        name = col+"_diff"
        df_sampled[name] = np.abs(df_sampled[col]-df_sampled[col+"_comp"])
    categorical_columns = ["Supplier_Package"]
    for col in categorical_columns: 
        name = col+"_diff"
        df_sampled[name] = np.where(df_sampled[col] == df_sampled[col+"_comp"], 1, 0)

    df_sampled.to_csv(output_file, index=False)
    print(f"Combined table data saved to {output_file}")

def run():
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    home = os.path.dirname(current_dir)

    file1 = f'{home}\encoded data\opamps-features.csv'
    file2 = f'{home}\encoded data\opamps-xref-cleaned.csv'
    output = f'{home}\encoded data\input-data.csv'
    preprocess(file1, file2, output)

if __name__ == "__main__":
    run()