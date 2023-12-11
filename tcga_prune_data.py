
import pandas as pd

import os


def prune_all_files(folder):

    final_folder = './tcga_data/' + folder
    output_folder = './pruned_tcga_data/' + folder
    info_files = os.listdir(final_folder)
    target_df = pd.DataFrame()
    first = 1
    for file in info_files:
        full_file = final_folder + '/' + file
        patient_id = file.split(".")

        colnames=['gene_id', 'gene_name', 'gene_type', 'unstranded', 'stranded_first', 'stranded_second', 'tpm_unstranded', 'fpkm_unstranded', 'fpkm_uq_unstranded'] 
        df = pd.read_csv(full_file, sep='\t', skiprows=6, names=colnames)
        df = df[df['gene_type'] == 'protein_coding']
        df = df.drop(['gene_id', 'gene_type', 'stranded_first', 'stranded_second', 'tpm_unstranded', 'fpkm_unstranded', 'fpkm_uq_unstranded'], axis=1)
        df = df.rename(columns={"unstranded": patient_id[0]})
        out_file = output_folder + '/' + file
        df.to_csv(out_file)

        print('file:{} pruned!'.format(file))

prune_all_files("Primary Tumor")
prune_all_files("Recurrent Tumor")
prune_all_files("Solid Tissue Normal")










