import pandas as pd

import os

'''
clinical_file = './clinical_data/clinical.tsv'

clinical_df = pd.read_csv(clinical_file, sep='\t')

clinical_df.head(5)
'''

full_file = './pruned_tcga_data/Primary Tumor/'
file1 = full_file+'00d461ae-a1d8-42f2-abd8-5e159363d857.rna_seq.augmented_star_gene_counts.tsv'

df_original = pd.read_csv(file1)

'''
file2 = full_file+'00fabec9-d311-4994-a7e5-eb91178d14f2.rna_seq.augmented_star_gene_counts.tsv'
test_df = pd.DataFrame()
df1 = pd.read_csv(file1)
df1 = df1.drop(['Unnamed: 0'], axis=1, inplace=False)
test_df = df1
df2 = pd.read_csv(file2)
df2 = df2.drop(['Unnamed: 0'], axis=1, inplace=False)
x = df2['gene_name'].isin(df_original['gene_name']).value_counts()
print(x.index)
if (x.index != True):
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
else:
    print('ok')
    cols = df2.columns
    extracted_col = df2[cols[1]]
    test_df.insert(1, cols[1], extracted_col)
'''

def new_get_all_files(folder):

    final_folder = './pruned_tcga_data/' + folder
    info_files = os.listdir(final_folder)
    target_df = pd.DataFrame()
    first = 1
    labels = []
    for file in info_files:
        full_file = final_folder + '/' + file
        df = pd.read_csv(full_file)
        df = df.drop(['Unnamed: 0'], axis=1, inplace=False)

        print('shape: ', df.shape)
        cols = df.columns
        labels.append(cols[1])

        if (first ==1):
            target_df = df
            first = 0
        else:
            print('target_df shape: ', target_df.shape)
            x = df['gene_name'].isin(df_original['gene_name']).value_counts()
            print(x.index)
            if (x.index != True):
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print('file:{} merge done'.format(file))
            else:
                print('ok')
                extracted_col = df[cols[1]]
                target_df.insert(1, cols[1], extracted_col)
        #print('file:{} merge done'.format(file))
    return target_df, labels, 

tumor_labels = []

# Primary Tumor

primary_tumor_df, labels = new_get_all_files("Primary Tumor")
tumor_labels = labels
#final_primary_tumor_df = primary_tumor_df.T
#final_primary_tumor_df['patient_id'] = final_primary_tumor_df.index
#final_primary_tumor_df['label'] = 1
#print("TUMOR SHAPE:", final_primary_tumor_df.shape)


#Recurrent Tumor

resurrent_tumor_df, labels = new_get_all_files("Recurrent Tumor")
tumor_labels = tumor_labels + labels
#final_resurrent_tumor_df = resurrent_tumor_df.T
#final_resurrent_tumor_df['patient_id'] = final_resurrent_tumor_df.index
#final_resurrent_tumor_df['label'] = 1
#print(final_resurrent_tumor_df.shape)


# Solid Tissue Normal
normal_df, labels = new_get_all_files("Solid Tissue Normal")
normal_labels = labels
#final_normal_df = normal_df.T
#final_normal_df['patient_id'] = final_normal_df.index
#final_normal_df['label'] = 0
#final_normal_df

combined_df = pd.concat([normal_df, resurrent_tumor_df, primary_tumor_df], axis=1)
combined_df = combined_df.loc[:,~combined_df.columns.duplicated()].copy()
combined_df = combined_df.T
combined_df['patient_id'] = combined_df.index

combined_df['label'] = [0 if x in normal_labels else 1 for x in combined_df.index]
combined_df.to_csv("my_full_data.csv")










