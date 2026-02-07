import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from dotenv import load_dotenv
import os
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Dict, Any
from openai import OpenAI

# Load environment variables
load_dotenv()

# Cloudinary Configuration
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

from sheets_service import SheetsService

# Configuration
CREDENTIALS_PATH = os.getenv("CREDENTIALS_FILE", "ggsheet-key.json")
SHEET_URL = os.getenv("SHEET_URL")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# AI Client
ai_client = None
if DEEPSEEK_API_KEY:
    ai_client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

# Initialize Service
sheets_service = None
if os.path.exists(CREDENTIALS_PATH) and SHEET_URL:
    try:
        sheets_service = SheetsService(CREDENTIALS_PATH, SHEET_URL)
    except Exception as e:
        print(f"Error initializing sheets service: {e}")

# FastAPI App
app = FastAPI(title="SheetFlow Multi-Sheet CRUD")

# Static and Templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    if not sheets_service:
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "error": "Sheets service not initialized. Check your .env and credentials.",
            "sheet_names": [],
            "current_sheet": "",
            "data": [],
            "headers": []
        })
    
    try:
        sheet_names = sheets_service.get_all_sheet_names()
        default_sheet = sheet_names[0] if sheet_names else ""
        data = sheets_service.get_all_data(default_sheet) if default_sheet else []
        headers = sheets_service.get_headers(default_sheet) if default_sheet else []
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "sheet_names": sheet_names,
            "current_sheet": default_sheet,
            "data": data,
            "headers": headers
        })
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "error": str(e),
            "sheet_names": [],
            "current_sheet": "",
            "data": [],
            "headers": []
        })

@app.get("/sheet/{sheet_name}")
async def get_sheet_data(sheet_name: str):
    if not sheets_service:
        raise HTTPException(status_code=500, detail="Service not initialized")
    try:
        data = sheets_service.get_all_data(sheet_name)
        headers = sheets_service.get_headers(sheet_name)
        return {"status": "success", "headers": headers, "data": data}
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

@app.post("/sheet/{sheet_name}/add")
async def add_item(sheet_name: str, request: Request):
    if not sheets_service:
        raise HTTPException(status_code=500, detail="Sheets service not initialized")
    
    form_data = await request.form()
    data_dict = {key: value for key, value in form_data.items()}
    
    try:
        sheets_service.add_row(sheet_name, data_dict)
        return JSONResponse(content={"status": "success"})
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

@app.post("/sheet/{sheet_name}/update/{row_id}")
async def update_item(sheet_name: str, row_id: int, request: Request):
    if not sheets_service:
        raise HTTPException(status_code=500, detail="Sheets service not initialized")
    
    form_data = await request.form()
    data_dict = {key: value for key, value in form_data.items()}
    
    try:
        sheets_service.update_row(sheet_name, row_id, data_dict)
        return JSONResponse(content={"status": "success"})
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

@app.post("/sheet/{sheet_name}/delete/{row_id}")
async def delete_item(sheet_name: str, row_id: int):
    if not sheets_service:
        raise HTTPException(status_code=500, detail="Sheets service not initialized")
    
    try:
        # row_id is 1-based index (including header)
        sheets_service.delete_row(sheet_name, row_id)
        return JSONResponse(content={"status": "success"})
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

@app.post("/ai/generate-slogan")
async def generate_slogan(request: Request):
    if not ai_client:
        return JSONResponse(content={"status": "error", "message": "AI Client chưa được cấu hình (Thiếu DEEPSEEK_API_KEY trong .env)"}, status_code=500)
    
    try:
        data = await request.json()
        product_name = data.get("product_name", "").strip()
        if not product_name:
            return JSONResponse(content={"status": "error", "message": "Thiếu tên sản phẩm"}, status_code=400)
        
        response = ai_client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Bạn là chuyên gia marketing. Hãy viết 1 câu slogan ngắn gọn, chân phương, thu hút (dưới 15 từ) cho sản phẩm sau. Chỉ trả về duy nhất nội dung slogan, không kèm giải thích hay dấu ngoặc kép."},
                {"role": "user", "content": product_name}
            ],
            stream=False
        )
        slogan = response.choices[0].message.content.strip()
        return {"status": "success", "slogan": slogan}
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

@app.post("/ai/generate-slug")
async def generate_slug(request: Request):
    if not ai_client:
        return JSONResponse(content={"status": "error", "message": "AI Client chưa được cấu hình (Thiếu DEEPSEEK_API_KEY trong .env)"}, status_code=500)
    
    try:
        data = await request.json()
        product_name = data.get("product_name", "").strip()
        if not product_name:
            return JSONResponse(content={"status": "error", "message": "Thiếu tên sản phẩm"}, status_code=400)
        
        response = ai_client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Bạn là chuyên gia viết lách và marketing sáng tạo. Hãy viết 1 đoạn mô tả sản phẩm ngắn gọn nhưng cực kỳ thú vị và gây tò mò cho người đọc (khoảng 10-20 từ) dựa trên tên sản phẩm sau. Chỉ trả về duy nhất nội dung mô tả, không kèm dấu ngoặc kép hay lời dẫn."},
                {"role": "user", "content": product_name}
            ],
            stream=False
        )
        slug = response.choices[0].message.content.strip()
        return {"status": "success", "slug": slug}
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

@app.post("/catalog/create")
async def create_catalog(request: Request):
    """
    Tạo mục lục mới (sheet con) và cập nhật vào MỤC LỤC
    """
    if not sheets_service:
        return JSONResponse(content={"status": "error", "message": "Sheets service not initialized"}, status_code=500)
    
    try:
        data = await request.json()
        ten_muc_luc = data.get("ten_muc_luc", "").strip()
        link_zalo = data.get("link_zalo", "").strip()
        link_nv = data.get("link_nv", "").strip()
        
        # Validate input
        if not ten_muc_luc:
            return JSONResponse(content={"status": "error", "message": "Thiếu tên mục lục"}, status_code=400)
        if not link_zalo:
            return JSONResponse(content={"status": "error", "message": "Thiếu Link Zalo"}, status_code=400)
        if not link_nv:
            return JSONResponse(content={"status": "error", "message": "Thiếu Link Nhân Viên"}, status_code=400)
        
        # Lấy danh sách sheet hiện có để chọn template
        all_sheets = sheets_service.get_all_sheet_names()
        template_sheet = None
        for sheet_name in all_sheets:
            if sheet_name.lower() != "mục lục":
                template_sheet = sheet_name
                break
        
        if not template_sheet:
            return JSONResponse(content={"status": "error", "message": "Không tìm thấy sheet template để copy headers"}, status_code=500)
        
        # Tạo sheet con mới và lấy URL
        try:
            sheet_url = sheets_service.create_new_sheet_with_headers(ten_muc_luc, template_sheet)
        except Exception as e:
            return JSONResponse(content={"status": "error", "message": f"Lỗi tạo sheet: {str(e)}"}, status_code=500)
        
        
        # Cập nhật vào sheet MỤC LỤC
        catalog_data = {
            "TÊN SHEET": ten_muc_luc,
            "LINK TRUY CẬP TRỰC TIẾP": sheet_url,
            "LINK ZALO": link_zalo,
            "LINK NV": link_nv
        }
        
        # Debug: In ra headers của MỤC LỤC
        try:
            muc_luc_headers = sheets_service.get_headers("MỤC LỤC")
            print(f"DEBUG - MỤC LỤC Headers: {muc_luc_headers}")
            print(f"DEBUG - Catalog Data: {catalog_data}")
        except Exception as e:
            print(f"DEBUG - Error getting headers: {e}")
        
        try:
            sheets_service.add_row("MỤC LỤC", catalog_data)
            print(f"DEBUG - Successfully added row to MỤC LỤC")
        except Exception as e:
            print(f"DEBUG - Error adding row: {str(e)}")
            return JSONResponse(content={"status": "error", "message": f"Lỗi cập nhật MỤC LỤC: {str(e)}"}, status_code=500)
        
        return {
            "status": "success", 
            "sheet_name": ten_muc_luc, 
            "sheet_url": sheet_url,
            "message": f"Đã tạo mục lục '{ten_muc_luc}' thành công!"
        }
        
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

@app.get("/id-gen/non-dropbuy/{sheet_name}")
async def get_next_non_dropbuy_id(sheet_name: str):
    """
    Sinh mã ID tiếp theo cho sản phẩm Non-Dropbuy (Nxx)
    """
    if not sheets_service:
        return JSONResponse(content={"status": "error", "message": "Sheets service not initialized"}, status_code=500)
    
    try:
        data = sheets_service.get_all_data(sheet_name)
        max_id = 0
        for row in data:
            curr_id_val = row.get("ID Sản phẩm") or row.get("ID sản phẩm")
            if curr_id_val and str(curr_id_val).startswith("N"):
                try:
                    num_part = str(curr_id_val)[1:]
                    if num_part.isdigit():
                        num = int(num_part)
                        if num > max_id: max_id = num
                except: continue
        
        return {"status": "success", "next_id": f"N{max_id + 1}"}
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

@app.get("/id-gen/dropbuy/{sheet_name}")
async def get_next_dropbuy_id(sheet_name: str):
    """
    Sinh mã ID tiếp theo cho sản phẩm Dropbuy (dạng số nguyên)
    """
    if not sheets_service:
        return JSONResponse(content={"status": "error", "message": "Sheets service not initialized"}, status_code=500)
    
    try:
        data = sheets_service.get_all_data(sheet_name)
        max_id = 0
        for row in data:
            curr_id_val = row.get("ID Sản phẩm") or row.get("ID sản phẩm")
            if curr_id_val:
                try:
                    # Chỉ lấy các ID là số thuần túy
                    s_val = str(curr_id_val).strip()
                    if s_val.isdigit():
                        num = int(s_val)
                        if num > max_id: max_id = num
                except: continue
        
        # Nếu chưa có ID nào, bắt đầu từ một số mặc định lớn (vốn dĩ Dropbuy thường là số 6 chữ số)
        # Nhưng ở đây ta cứ lấy max + 1 cho an toàn. Nếu 0 thì bắt đầu từ 100001
        if max_id == 0: next_id = "100001"
        else: next_id = str(max_id + 1)
            
        return {"status": "success", "next_id": next_id}
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

@app.get("/api/defaults")
async def get_defaults():
    """
    Lấy giá trị mặc định cho các trường contact (Link Zalo, Link NV)
    """
    return {
        "link_zalo": os.getenv("DEFAULT_LINK_ZALO", ""),
        "link_nv": os.getenv("DEFAULT_LINK_NV", "")
    }

@app.get("/api/provinces")
async def get_provinces():
    """
    Lấy danh sách tất cả tỉnh/thành phố từ Vietnam Provinces API
    """
    try:
        import httpx
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get("https://provinces.open-api.vn/api/p/")
            if response.status_code == 200:
                return response.json()
            else:
                return JSONResponse(content={"status": "error", "message": "Failed to fetch provinces"}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

@app.get("/api/districts/{province_code}")
async def get_districts(province_code: int):
    """
    Lấy danh sách quận/huyện theo mã tỉnh
    """
    try:
        import httpx
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(f"https://provinces.open-api.vn/api/p/{province_code}?depth=2")
            if response.status_code == 200:
                data = response.json()
                return data.get("districts", [])
            else:
                return JSONResponse(content={"status": "error", "message": "Failed to fetch districts"}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

@app.get("/api/wards/{district_code}")
async def get_wards(district_code: int):
    """
    Lấy danh sách phường/xã theo mã quận/huyện
    """
    try:
        import httpx
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(f"https://provinces.open-api.vn/api/d/{district_code}?depth=2")
            if response.status_code == 200:
                data = response.json()
                return data.get("wards", [])
            else:
                return JSONResponse(content={"status": "error", "message": "Failed to fetch wards"}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """
    Upload ảnh lên Cloudinary
    """
    try:
        # Kiểm tra định dạng file
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in [".jpg", ".jpeg", ".png", ".webp", ".gif"]:
            return JSONResponse(content={"status": "error", "message": "Định dạng file không hỗ trợ"}, status_code=400)
        
        # Upload trực tiếp lên Cloudinary
        upload_result = cloudinary.uploader.upload(
            file.file,
            folder="sheetflow_products",
            resource_type="image"
        )
        
        # Trả về secure_url (HTTPS)
        return {
            "status": "success",
            "url": upload_result.get("secure_url")
        }
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": f"Lỗi Cloudinary: {str(e)}"}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
