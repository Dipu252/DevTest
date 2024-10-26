import pandas as pd
from django.shortcuts import render
from .forms import UploadFileForm
from django.core.files.storage import FileSystemStorage

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            file_path = fs.path(filename)
            
            # Process the uploaded file
            df = pd.read_excel(file_path) if file.name.endswith('.xlsx') else pd.read_csv(file_path)
            
            # Prepare summary
            summary = {
                "total_rows": df.shape[0],
                "total_columns": df.shape[1],
                "column_names": df.columns.tolist(),
                "sample_data": df.head().to_html(),
                "statistics": df.describe().to_html(),
            }
            
            fs.delete(filename)  # Optional: Delete file after processing

            return render(request, 'file_upload/summary.html', {'summary': summary})

    else:
        form = UploadFileForm()
    
    return render(request, 'file_upload/upload.html', {'form': form})
