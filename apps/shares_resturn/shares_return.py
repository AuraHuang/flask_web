ALLOWED_EXTENSIONS = {'csv', 'txt', 'xls', 'xlsx'}

def allowed_file(file):
    
    if '.' in file.filename:
        ext = file.filename.split('.', 1)[1].lower()
        if ext in ALLOWED_EXTENSIONS:
            return True
    else:
        return False
