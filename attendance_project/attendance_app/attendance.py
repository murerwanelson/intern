import pandas as pd
from attendance_app.models import Employee  # Import Employee model

def process_attendance(file_path):
    """
    Process attendance CSV and mark employees absent if no records exist.
    
    Args:
        file_path (str): Path to the CSV file.
    
    Returns:
        pd.DataFrame: Processed attendance data with 'Time In', 'Time Out', and 'Attendance' status.
    """
    # Load employee names from the database
    employees = list(Employee.objects.values_list('name', flat=True))  # Get all employees from DB

    # Load the CSV file
    df = pd.read_csv(file_path)

    # Drop unnecessary columns (if they exist)
    columns_to_drop = ['Department', 'No.', 'Location ID', 'ID Number', 'VerifyCode', 'CardNo']
    df = df.drop(columns=[col for col in columns_to_drop if col in df.columns], errors='ignore')

    # Extract Date and Time from 'Date/Time'
    df['Date'] = pd.to_datetime(df['Date/Time']).dt.date
    df['Time'] = pd.to_datetime(df['Date/Time']).dt.time
    df = df.drop(columns=['Date/Time'])

    # Group by Name and Date to get first (Time In) and last (Time Out)
    time_in_out = df.groupby(['Name', 'Date'])['Time'].agg(['min', 'max']).reset_index()
    time_in_out.rename(columns={'min': 'Time In', 'max': 'Time Out'}, inplace=True)

    # Get unique dates from CSV
    unique_dates = df['Date'].unique()

    # Generate a full attendance list for all employees
    all_attendance = [{'Name': name, 'Date': date} for name in employees for date in unique_dates]
    all_attendance_df = pd.DataFrame(all_attendance)

    # Merge full attendance with actual clock-in/out records
    attendance_df = pd.merge(all_attendance_df, time_in_out, on=['Name', 'Date'], how='left')

    # Mark as 'Absent' by default, update to 'Present' if Time In exists
    attendance_df['Attendance'] = 'Absent'
    attendance_df.loc[attendance_df['Time In'].notnull(), 'Attendance'] = 'Present'

    return attendance_df
