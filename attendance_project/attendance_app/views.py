import io
import os
import tempfile
import pandas as pd

from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadCSVForm
from .attendance import process_attendance  # Import the function
from .models import Employee

def process_csv(request):
    if request.method == "POST":
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']

            try:
                # Read the uploaded file into memory
                file_data = csv_file.read()

                # Save to a temporary file so it can be processed
                with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
                    tmp.write(file_data)
                    tmp_path = tmp.name

                # Process the CSV using the function
                processed_df = process_attendance(tmp_path)

                # Remove the temporary file
                os.remove(tmp_path)

                # Convert the processed DataFrame to CSV
                csv_buffer = io.StringIO()
                processed_df.to_csv(csv_buffer, index=False)

                # Return the processed CSV as a download
                response = HttpResponse(csv_buffer.getvalue(), content_type="text/csv")
                response['Content-Disposition'] = 'attachment; filename="processed_attendance.csv"'
                return response

            except Exception as e:
                return render(request, 'attendance_app/upload.html', {
                    'form': form,
                    'error': f"Error processing file: {e}"
                })

    else:
        form = UploadCSVForm()

    return render(request, 'attendance_app/upload.html', {'form': form})
