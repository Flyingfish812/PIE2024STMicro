# Reference to notebook/241118/not_found.ipynb
import pandas as pd
import os
    
home = os.path.abspath(os.getcwd())

def clear_not_found(xref_file, features_file, output_file):
    xref_data = pd.read_csv(xref_file)
    features_data = pd.read_csv(features_file)

    not_found = []

    for index, row in xref_data.iterrows():
        st_mpn = row['STMicro MPN']
        st_name = row['STMicro Name']
        competitor_mpn = row['Competitor MPN']
        competitor_name = row['Competitor Name']
        
        st_match = features_data[
            (features_data['MPN'] == st_mpn) & 
            (features_data['MANUFACTURER'] == st_name)
        ]
        if st_match.empty:
            not_found.append({'MPN': st_mpn, 'MANUFACTURER': st_name})
        
        competitor_match = features_data[
            (features_data['MPN'] == competitor_mpn) & 
            (features_data['MANUFACTURER'] == competitor_name)
        ]
        if competitor_match.empty:
            not_found.append({'MPN': competitor_mpn, 'MANUFACTURER': competitor_name})

    # if not not_found:
    #     print("All components have corresponding features.")
    # else:
    #     print("The following components do not have corresponding features:")
    #     for item in not_found:
    #         print(f"MPN: {item['MPN']}, MANUFACTURER: {item['MANUFACTURER']}")

    unique_not_found = [dict(t) for t in {tuple(d.items()) for d in not_found}]
    not_found_set = {(d["MPN"], d["MANUFACTURER"]) for d in unique_not_found}

    cleaned_data = xref_data[
        ~xref_data.apply(
            lambda row: (
                (row["STMicro MPN"], row["STMicro Name"]) in not_found_set or
                (row["Competitor MPN"], row["Competitor Name"]) in not_found_set
            ), axis=1
        )
    ]

    cleaned_data.to_csv(output_file, index=False)

# If already have the not_found.csv file, use this function
def clear_not_found_with_file(xref_file, not_found_file, output_file):
    xref_data = pd.read_csv(xref_file)
    not_found_data = pd.read_csv(not_found_file)

    not_found_set = set(
        zip(not_found_data["MPN"], not_found_data["MANUFACTURER"])
    )

    cleaned_data = xref_data[
        ~xref_data.apply(
            lambda row: (
                (row["STMicro MPN"], row["STMicro Name"]) in not_found_set or
                (row["Competitor MPN"], row["Competitor Name"]) in not_found_set
            ), axis=1
        )
    ]

    cleaned_data.to_csv(output_file, index=False)

xref_file = f'{home}\\encoded data\\opamps-xref.csv'
features_file = f'{home}\\encoded data\\opamps-features.csv'
not_found_file = f'{home}\\encoded data\\not_found.csv'
output_file = f'{home}\\encoded data\\opamps-xref-cleaned.csv'
clear_not_found_with_file(xref_file, not_found_file, output_file)