import pandas as pd
import requests
import os

# scroll down to the bottom to implement your solution

if __name__ == '__main__':

    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if ('A_office_data.xml' not in os.listdir('../Data') and
        'B_office_data.xml' not in os.listdir('../Data') and
        'hr_data.xml' not in os.listdir('../Data')):
        print('A_office_data loading.')
        url = "https://www.dropbox.com/s/jpeknyzx57c4jb2/A_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/A_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('B_office_data loading.')
        url = "https://www.dropbox.com/s/hea0tbhir64u9t5/B_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/B_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('hr_data loading.')
        url = "https://www.dropbox.com/s/u6jzqqg1byajy0s/hr_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/hr_data.xml', 'wb').write(r.content)
        print('Loaded.')

        # All data in now loaded to the Data folder.

    # Load the Office A data from an XML file into a DataFrame
    A_df = pd.read_xml('../Data/A_office_data.xml')

    # Load the Office B data from an XML file into a DataFrame
    B_df = pd.read_xml('../Data/B_office_data.xml')

    # Load the HR data from an XML file into a DataFrame
    hr_df = pd.read_xml('../Data/hr_data.xml')

    # Create a new index for Office A data by concatenating 'A' with the Employee_office_id column
    A_df['index'] = 'A' + A_df['employee_office_id'].astype(str)

    # Set the newly created 'index' column as the index for Office A DataFrame
    # The drop=False parameter ensures that the 'index' column is retained in the DataFrame
    A_df.set_index('index', inplace=True, drop=False)

    # Create a new index for Office B data by concatenating 'A' with the Employee_office_id column
    # Note: There is an error here; it should concatenate 'B' instead of 'A' for Office B data
    B_df['index'] = 'B' + B_df['employee_office_id'].astype(str)

    # Set the newly created 'index' column as the index for Office B DataFrame
    # The drop=False parameter ensures that the 'index' column is retained in the DataFrame
    B_df.set_index('index', inplace=True, drop=False)

    # Set the 'employee_id' column as the index for HR DataFrame
    # The drop=False parameter ensures that the 'employee_id' column is retained in the DataFrame
    hr_df.set_index('employee_id', inplace=True, drop=False)

    # Print the list of indexes for Office A DataFrame
    # print(A_df.index.tolist())

    # Print the list of indexes for Office B DataFrame
    # print(B_df.index.tolist())

    # Print the list of indexes for HR DataFrame
    # print(hr_df.index.tolist())

    # Concatenate the Office A and Office B DataFrames into a unified office dataset
    AB_df = pd.concat([A_df, B_df])

    # Perform an inner merge of the unified office dataset with the HR dataset by index
    # The indicator=True parameter adds a column '_merge' that shows the source of each row
    Final_df = AB_df.merge(hr_df, how='inner', left_index=True, right_index=True, indicator=True)

    # Drop unnecessary columns: 'employee_office_id', 'employee_id', '_merge', and 'index'
    Final_df.drop(['employee_office_id', 'employee_id', '_merge', 'index'], axis=1, inplace=True)

    # Sort the final DataFrame by its index
    Final_df.sort_index(inplace=True)
    print(Final_df.columns)
    # What are the departments of the top ten employees in terms of working hours?
    # Final_df.sort_values('average_monthly_hours', inplace=True, ascending=False)
    # print(Final_df['Department'].head(10).tolist())

    # What is the total number of projects on which IT department employees with low salaries have worked?
    # print(Final_df.query('Department == "IT" & salary == "low"')['number_project'].sum())

    # What are the last evaluation scores and the satisfaction levels of the employees A4, B7064, and A3033?
    # employeesId = ['A4', 'B7064', 'A3033']
    # print(Final_df.loc[['A4', 'B7064', 'A3033'], ['last_evaluation','satisfaction_level']].values.tolist())

    # Group by 'left' column and calculate the required metrics
    def count_bigger_5(series):
        return (series > 5).sum()

    metrics = {
        'number_project': ['median', count_bigger_5],
        'time_spend_company': ['mean', 'median'],
        'Work_accident': 'mean',
        'last_evaluation': ['mean', 'std']
    }

    # Convert the resulting DataFrame to a dictionary
    print(Final_df.groupby('left').agg(metrics).round(2).to_dict())






