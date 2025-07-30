
def clean_admission_data(input_file_path, output_csv_path):
    """
    Reads raw admission data from an Excel file, cleans it, combines minority and non-minority
    sanctioned/admitted numbers, calculates vacancies, and saves to a new CSV.

    Args:
        input_file_path (str): Path to the raw input Excel file (e.g., 'Admission 24-07-2025.xlsx').
        output_csv_path (str): Path where the cleaned CSV file will be saved.
    """
    try:
        # Read the raw Excel file, skipping the initial header rows.
        # Based on the file snippet, data starts from the 6th row (index 5).
        # Using pd.read_excel for .xlsx files.
        df_raw = pd.read_excel(input_file_path, skiprows=4)

        # Define the column names for the raw DataFrame after skipping rows.
        # This list must match the exact number of columns in your data (12 columns).
        # These names are derived from the structure of your input Excel snippet.
        df_raw.columns = [
            'S.No', 'District', 'Institution Name',
            'V Minorities Sanctioned', 'V Minorities Admitted',
            'V NonMinorities Sanctioned', 'V NonMinorities Admitted',
            'Course',
            'Inter Minorities Sanctioned', 'Inter Minorities Admitted',
            'Inter NonMinorities Sanctioned', 'Inter NonMinorities Admitted'
        ]

        # Clean 'Institution Name': remove text within brackets and replace 'Boys'/'Girls'.
        # Convert to string first to handle potential non-string types.
        #df_raw['Institution Name'] = df_raw['Institution Name'].astype(str).apply(
        #    lambda x: re.sub(r'\([^)]*\)', '', x).replace('Boys', 'B').replace('Girls', 'G').strip()
        #)


         # --- ADDON CODE: Remove the last row of the input data ---
        # This is useful if the last row contains summary statistics or unwanted data.
        if not df_raw.empty:
            df_raw = df_raw.iloc[:-1]
            print("Last row of the raw data has been removed.")
        else:
            print("Raw DataFrame is empty, no row to remove.")
        # --- END ADDON CODE ---



        numeric_cols = [
            'V Minorities Sanctioned', 'V Minorities Admitted',
            'V NonMinorities Sanctioned', 'V NonMinorities Admitted',
            'Inter Minorities Sanctioned', 'Inter Minorities Admitted',
            'Inter NonMinorities Sanctioned', 'Inter NonMinorities Admitted'
        ]

        for col in numeric_cols:
            df_raw[col] = pd.to_numeric(df_raw[col], errors='coerce').fillna(0).astype(int)

        # --- Process Class V data ---
        # Select relevant columns for Class V and create a copy to avoid SettingWithCopyWarning.
        df_v = df_raw[['S.No', 'District', 'Institution Name',
                       'V Minorities Sanctioned', 'V Minorities Admitted',
                       'V NonMinorities Sanctioned', 'V NonMinorities Admitted']].copy()
        df_v['Class'] = 'V' # Assign 'V' to the 'Class' column for these rows

        # Calculate combined 'Sanctioned' and 'Admitted' for Class V (Minorities + Non-Minorities)
        df_v['Sanctioned'] = df_v['V Minorities Sanctioned'] + df_v['V NonMinorities Sanctioned']
        df_v['Admitted'] = df_v['V Minorities Admitted'] + df_v['V NonMinorities Admitted']

        # --- Process Inter 1st Year data ---
        # Select relevant columns for Inter 1st Year and create a copy.
        df_inter = df_raw[['S.No', 'District', 'Institution Name',
                           'Inter Minorities Sanctioned', 'Inter Minorities Admitted',
                           'Inter NonMinorities Sanctioned', 'Inter NonMinorities Admitted']].copy()
        df_inter['Class'] = 'Inter 1st Year' # Assign 'Inter 1st Year' to the 'Class' column

        # Calculate combined 'Sanctioned' and 'Admitted' for Inter (Minorities + Non-Minorities)
        df_inter['Sanctioned'] = df_inter['Inter Minorities Sanctioned'] + df_inter['Inter NonMinorities Sanctioned']
        df_inter['Admitted'] = df_inter['Inter Minorities Admitted'] + df_inter['Inter NonMinorities Admitted']

        # Concatenate the Class V and Inter DataFrames to form the final DataFrame
        df_final = pd.concat([df_v, df_inter], ignore_index=True)

        # Calculate 'Vacancies'
        df_final['Vacancies'] = df_final['Sanctioned'] - df_final['Admitted']

        # Reorder and select final columns as per the desired output format
        # The 'S.No' from the raw data is kept as the final S.No.
        df_final = df_final[['S.No', 'District', 'Institution Name', 'Class', 'Sanctioned', 'Admitted', 'Vacancies']]

        # Rename 'Institution Name' to 'name of the tmr institute' to match the example output
        #df_final.rename(columns={'Institution Name': 'name of the tmr institute'}, inplace=True)

        # Save the cleaned DataFrame to a CSV file
        df_final.to_csv(output_csv_path, index=False)

       
    except FileNotFoundError:
        print(f"Error: The input file '{input_file_path}' was not found. Please ensure it's in the correct directory.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")