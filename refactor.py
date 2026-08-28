import os
import re

ROUTERS_DIR = "backend/app/api/v1/routers"

for file_name in os.listdir(ROUTERS_DIR):
    if not file_name.endswith(".py"):
        continue
        
    file_path = os.path.join(ROUTERS_DIR, file_name)
    with open(file_path, "r") as f:
        content = f.read()

    # Imports change
    content = content.replace("from app.api.v1.schemas.common import Meta", "from app.api.v1.schemas.response import ApiMeta")

    # SuccessResponse replacements
    content = re.sub(
        r'SuccessResponse\(\s*data=(.*?),?\s*meta=Meta\(request_id=meta\["request_id"\]\)\s*\)',
        r'SuccessResponse(data=\1, request_id=meta["request_id"])',
        content,
        flags=re.DOTALL
    )

    # PaginatedResponse replacements
    content = re.sub(
        r'PaginatedResponse\(\s*data=(.*?),?\s*pagination=(.*?),?\s*meta=Meta\(request_id=meta\["request_id"\]\)\s*\)',
        r'PaginatedResponse(data=\1, meta=ApiMeta(pagination=\2), request_id=meta["request_id"])',
        content,
        flags=re.DOTALL
    )

    with open(file_path, "w") as f:
        f.write(content)

print("Router refactoring complete.")
