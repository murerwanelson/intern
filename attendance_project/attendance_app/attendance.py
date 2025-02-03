import pandas as pd

def process_attendance(file_path):
    """
    Process the attendance CSV file.
    
    Args:
        file_path (str): Path to the CSV file.
    
    Returns:
        pd.DataFrame: Processed attendance data with 'Time In', 'Time Out', and 'Attendance' status.
    """
    # Load the CSV file
    df = pd.read_csv(file_path)

    # Drop unnecessary columns
    columns_to_drop = ['Department', 'No.', 'Location ID', 'ID Number', 'VerifyCode', 'CardNo']
    df = df.drop(columns=[col for col in columns_to_drop if col in df.columns], errors='ignore')

    # Extract Date and Time from 'Date/Time' column
    df['Date'] = pd.to_datetime(df['Date/Time']).dt.date
    df['Time'] = pd.to_datetime(df['Date/Time']).dt.time
    df = df.drop(columns=['Date/Time'])  # Drop original column

    # Group by Name and Date to get first and last clock-in/out times
    time_in_out = df.groupby(['Name', 'Date'])['Time'].agg(['min', 'max']).reset_index()
    time_in_out.rename(columns={'min': 'Time In', 'max': 'Time Out'}, inplace=True)

    # Generate a full list of employees for all recorded dates
    unique_names = df['Name'].unique()
    unique_dates = df['Date'].unique()
    all_attendance = [{'Name': name, 'Date': date} for name in unique_names for date in unique_dates]
    all_attendance_df = pd.DataFrame(all_attendance)

    # Merge full attendance records with actual clock-in/out times
    attendance_df = pd.merge(all_attendance_df, time_in_out, on=['Name', 'Date'], how='left')

    # Mark employees as 'Absent' by default and update to 'Present' if they have clock-in data
    attendance_df['Attendance'] = 'Absent'
    attendance_df.loc[attendance_df['Time In'].notnull(), 'Attendance'] = 'Present'

    return attendance_df

