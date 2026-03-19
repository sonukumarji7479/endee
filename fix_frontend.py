import os
import re

pages_dir = r"c:\Users\sonuk\Desktop\ai boot\frontend\pages"
files = ["dashboard.js", "documents.js", "quiz.js", "translator.js", "upload.js", "chat.js"]

import_line = "import { BACKEND_URL } from '../config.js';\n"

for filename in files:
    path = os.path.join(pages_dir, filename)
    if not os.path.exists(path):
         print(f"Skipping {filename} (not found)")
         continue
         
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Add import at top if not present
    if "import { BACKEND_URL }" not in content:
        content = import_line + content
    
    # 2. Replace relative fetch urls
    content = re.sub(r"fetch\('/api", "fetch(BACKEND_URL + '/api", content)
    
    # 3. Special case for chat.js
    if filename == "chat.js":
        content = re.sub(r"const BACKEND_URL = window\.location\.origin;\s*", "", content)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Frontend pages updated with BACKEND_URL")
