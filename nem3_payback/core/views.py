import pandas as pd
from django.shortcuts import render
from .forms import CSVUploadForm
from .models import HourlyReading
from django.utils import timezone

def upload_csv(request):
    if request.method == "POST" and request.FILES["csv_file"]:
        # Read the uploaded file into a string
        file = request.FILES["csv_file"]
        file_content = file.read().decode("utf-8")  # Decode the bytes to string

        # Initialize variables
        lines = file_content.splitlines()  # Split the content into individual lines
        data = []
        capture = False

        for line in lines:
            # Check if we're in the "Energy Received" section
            if "Delivered time period" in line:
                capture = True  # Start capturing data
                continue  # Skip the header line

            # Stop capturing when the next header is encountered
            if "Data for period starting" in line:
                capture = False

            # Capture rows only when within the relevant section
            if capture:
                # Split the line into columns based on commas
                parts = line.strip().split(",")  # split by commas
                if len(parts) >= 3:  # Ensure it has enough columns
                    data.append(parts)

        # Convert the captured data to a DataFrame
        columns = ["Time Period", "Usage Received (kWh)", "Reading Quality"]
        df = pd.DataFrame(data, columns=columns)
        df = df.drop(df.columns[2], axis=1)  # Drop the "Reading Quality" column

        # Clean the columns by removing unwanted quotes
        df['Time Period'] = df['Time Period'].str.replace('"', '')  # Remove quotes in the Time Period
        df['Usage Received (kWh)'] = df['Usage Received (kWh)'].str.replace('"', '')  # Remove quotes in Usage Received

        # Split the Time Period column into Start and End Timestamps
        df[['Start Timestamp', 'End Timestamp']] = df['Time Period'].str.split('to', expand=True)

        # Convert the Timestamps to datetime
        df['Start Timestamp'] = pd.to_datetime(df['Start Timestamp'].str.strip())
        df['End Timestamp'] = pd.to_datetime(df['End Timestamp'].str.strip())

        # Convert Usage Received to numeric
        df['Usage Received (kWh)'] = pd.to_numeric(df['Usage Received (kWh)'], errors='coerce')

        # Drop the original Time Period column
        df = df.drop(columns=['Time Period'])

        # Create the "Date Hour" column for grouping
        df['Date Hour'] = df['Start Timestamp'].dt.strftime('%Y-%m-%d %H:00:00')
        
        # Group by the Date Hour and sum the Usage Received (kWh)
        df_aggregated = df.groupby('Date Hour')['Usage Received (kWh)'].sum().reset_index()

        # Optionally, convert the Date Hour to datetime for better handling
        df_aggregated['Date Hour'] = pd.to_datetime(df_aggregated['Date Hour'])
        df_aggregated['Date Hour'] = df_aggregated['Date Hour'].apply(lambda x: timezone.make_aware(x) if x.tzinfo is None else x)

        # Save the cleaned data to the database
        for _, row in df_aggregated.iterrows():
            HourlyReading.objects.create(
                type="demand",
                start_interval=row["Date Hour"],
                reading_kwh=row["Usage Received (kWh)"]
            )

        return render(request, "upload_success.html")

    return render(request, "upload_form.html")
