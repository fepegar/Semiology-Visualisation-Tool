import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from ..semiology_all_localisations import all_localisations
from ..semiology_lateralisation_localisation import semiology_lateralisation_localisation
from .cleaning import cleaning
from .missing_columns import missing_columns
from .progress_stats import progress_stats, progress_venn
from .progress_study_type import progress_study_type, progress_venn_2
from .exclusions import exclusions



def MEGA_ANALYSIS(
    excel_data,
    n_rows = 2500,
    usecols = "A:DG",
    header = 1,
    exclude_data=False,
    plot=True,
    **kwargs,
    ):

    """
    import excel, clean data, print checks, melt and pivot_table.
    exclude_data > see exclusions.
    kwargs can be one of the exclusion keywords to pass on to exclusions.
        POST_ictals=True,
        PET_hypermetabolism=True,
        SPECT_PET=False,
        CONCORDANCE=False

    method to lookup specific semiology with no specific index:
    df.loc[df['Semiology Category'] =='Aphasia']

    method to lookup specific semiology and paper using multiIndex: change pd.read_excel below first
    df.loc[df.loc[('Aphasia')].index.str.contains('Afif') ]

    Ali Alim-Marvasti July Aug 2019
    """
    df = pd.read_excel(
        excel_data,
        nrows = n_rows,
        usecols = usecols,
        header=header,
    )

    # 0. CLEANUPS: remove empty rows and columns
    logging.debug('\n0. DataFrame pre-processing and cleaning:')
    df = cleaning(df)

    # 1. Exclusions
    if exclude_data:
        logging.debug('\n\n1. Excluding some data based on ground truths')
        if not kwargs:
            df = exclusions(df,
                POST_ictals=True,
                PET_hypermetabolism=True,
                SPECT_PET=False,
                CONCORDANCE=False)
        elif kwargs:
            df = exclusions(df,
                POST_ictals=kwargs['POST_ictals'],
                PET_hypermetabolism=kwargs['PET_hypermetabolism'],
                SPECT_PET=kwargs['SPECT_PET'],
                CONCORDANCE=kwargs['CONCORDANCE'])

        print('\ndf.shape after exclusions: ', df.shape)
    else:
        logging.debug('1. No Exclusions.')

    # 2. checking for missing labels e.g. Semiology Categories Labels:
    logging.debug('\n2. Checking for missing values for columns')
    missing_columns(df)

    logging.debug(f'\n Checking for dtypes: first localisation_labels column is: {df.columns[17]} ...last one is {df.columns[88]}')
    # localisation_labels = df.columns[17:72]  # old July 2019
    localisation_labels = df.columns[17:88]  # news March 2020
    for col in df[localisation_labels]:
        for val in df[col]:
            if ( type(val) != (np.float) ) & ( type(val) != (np.int) ):
                logging.debug(f'{type(val)} {col} {val}')

    # 3 ffill References:
    df.Reference.fillna(method='ffill', inplace=True)
    logging.debug('\n3. forward filled references')

    # 4 check no other entries besides "ES" and "y" in list(df['sEEG and/or ES'].unique())
    # March 2020 updated for sEEG_ES = 'sEEG (y) and/or ES (ES)'  # March 2020 version
    sEEG_ES = 'sEEG (y) and/or ES (ES)'  # March 2020 version

    logging.debug("\n4. 'sEEG and/or ES' column only contains ['ES', nan, 'y']: ")
    logging.debug(str(list(df[sEEG_ES].unique()) == ['ES', np.nan, 'y']))
    if not (list(df[sEEG_ES].unique()) == ['ES', np.nan, 'y']):
        logging.debug(f'the set includes: {list(df["sEEG and/or ES"].unique())}')

    # 5. print some basic progress stats:
    logging.debug('\n\n 5. BASIC PROGRESS:')
    logging.debug(f'Number of articles included in this analysis: {int(df["Reference"].nunique())}')
    logging.debug(f'Number of patients: {int(df["Tot Pt included"].sum())}')
    logging.debug(f'Number of lateralising datapoints: {df.Lateralising.sum()}')
    logging.debug(f'Number of localising datapoints: {df.Localising.sum()}')

    df_ground_truth = progress_stats(df)

    # plot progress by ground truth
    if plot:
        progress_venn(df_ground_truth, method='Lateralising')
        progress_venn(df_ground_truth, method='Localising')

    # 6. plot progress by study type (CS, SS, ET, Other)
    if plot:
        logging.debug("6. Venn diagrams by patient selection priors (study type)")
        df_study_type = progress_study_type(df)
        progress_venn_2(df_study_type, method='Lateralising')
        progress_venn_2(df_study_type, method='Localising')

    logging.debug(f'Other criteria: {df.loc[df["Other (e.g. Abs)"].notnull()]["Other (e.g. Abs)"].unique()}')
    logging.debug(
        'Lateralising Other Total/Exclusives: '
        f'{df_study_type.loc["OTHER", ("Lateralising Datapoints","Total")]}'
        '/'
        f'{df_study_type.loc["OTHER", ("Lateralising Datapoints","Exclusive")]}'
    )
    logging.debug(
        'Localising Other Total/Exclusives: '
        f'{df_study_type.loc["OTHER", ("Localising Datapoints","Total")]}'
        '/'
        f'{df_study_type.loc["OTHER", ("Localising Datapoints","Exclusive")]}'
    )

    return df, df_ground_truth, df_study_type
