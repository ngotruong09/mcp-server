# file: file_writer.py
import os
import sys
from mcp.server.fastmcp import FastMCP

# 1. Khởi tạo MCP Server
mcp = FastMCP("My-File-Writer")

# CẤU HÌNH: Thư mục an toàn để lưu file (tránh ghi đè file hệ thống)
# File sẽ được lưu vào thư mục 'output' nằm cùng chỗ với script này
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# Tạo thư mục output nếu chưa có
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

@mcp.tool()
def write_to_file(filename: str, content: str) -> str:
    """
    Tạo hoặc ghi đè một file văn bản.
    
    Args:
        filename: Tên file muốn tạo (ví dụ: 'notes.txt', 'script.py').
        content: Nội dung văn bản sẽ ghi vào file.
    """
    try:
        # Loại bỏ ký tự đường dẫn nguy hiểm (như ../) để bảo mật
        safe_filename = os.path.basename(filename)
        full_path = os.path.join(OUTPUT_DIR, safe_filename)

        # Ghi file với encoding utf-8 để hỗ trợ tiếng Việt
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        return f"✅ Đã ghi thành công vào: {full_path}"

    except Exception as e:
        return f"❌ Lỗi khi ghi file: {str(e)}"

# Chạy server
if __name__ == "__main__":
    sys.stderr.write("File Writer MCP Server is running...\n")
    mcp.run()