from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import pymysql
from fpdf import FPDF
import os
import urllib.request
from decimal import Decimal
import datetime

app = Flask(__name__)
app.secret_key = "cimb_pdf_generator_secret_key"

# Setup folders
os.makedirs("pdfs", exist_ok=True)
os.makedirs("logs", exist_ok=True)
os.makedirs("fonts", exist_ok=True)
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)
os.makedirs("test_cases", exist_ok=True)  # Add test_cases directory
os.makedirs("sample_output", exist_ok=True)  # Add sample_output directory

# Font mapping for different languages with supported character sets
FONT_MAPPING = {
    "en": "NotoSans-Regular.ttf",    # English - Latin characters
    "vi": "NotoSans-Regular.ttf",    # Vietnamese - Latin with diacritics
    "tl": "NotoSans-Regular.ttf",    # Tagalog - Latin characters
    "en-gb": "NotoSans-Regular.ttf", # British English - Latin characters
    "ta": "NotoSansTamil-Regular.ttf", # Tamil
    "th": "NotoSansThai-Regular.ttf", # Thai
    "ms": "NotoSansMalayalam-Regular.ttf" # Malayalam
}

# Download required fonts
def download_fonts():
    """
    Downloads required Noto Sans fonts from Google's repository.
    Supports multiple languages and character sets.
    Creates fonts directory if it doesn't exist.
    
    Returns:
        None
    
    Logs errors to error log file if download fails.
    """
    print("[↓] Downloading required fonts...")
    base_url = "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/"
    fonts = {
        "NotoSans-Regular.ttf": "NotoSans/NotoSans-Regular.ttf",
        "NotoSans-Bold.ttf": "NotoSans/NotoSans-Bold.ttf",
        "NotoSans-Italic.ttf": "NotoSans/NotoSans-Italic.ttf",  # Add Italic font
        "NotoSansMalayalam-Regular.ttf": "NotoSansMalayalam/NotoSansMalayalam-Regular.ttf",
        "NotoSansThai-Regular.ttf": "NotoSansThai/NotoSansThai-Regular.ttf",
        "NotoSansTamil-Regular.ttf": "NotoSansTamil/NotoSansTamil-Regular.ttf",
        "NotoSansTamil-Bold.ttf": "NotoSansTamil/NotoSansTamil-Bold.ttf"
    }
    
    for font_file, font_path in fonts.items():
        font_full_path = f"fonts/{font_file}"
        if not os.path.exists(font_full_path):
            try:
                url = f"{base_url}{font_path}"
                urllib.request.urlretrieve(url, font_full_path)
                print(f"[✓] Downloaded {font_file}")
            except Exception as e:
                print(f"[✖] Error downloading {font_file}: {e}")
                log_error(f"Error downloading font {font_file}: {str(e)}")

# Call font download on startup
download_fonts()

def log_error(message):
    """
    Logs error messages with timestamp to the error log file.
    
    Args:
        message (str): Error message to be logged
        
    Creates logs directory and log file if they don't exist.
    Format: [YYYY-MM-DD HH:MM:SS] Error message
    """
    with open("logs/cimb_pdf_error_log.txt", "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {message}\n")

def get_db_connection():
    """
    Establishes connection to MySQL database with CIMB statement data.
    
    Returns:
        Connection: MySQL connection object if successful
        None: If connection fails
        
    Connection parameters:
        host: localhost
        user: root
        database: cimb_db
        
    Logs error if connection fails.
    """
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="2001",
            database="cimb_db",
            cursorclass=pymysql.cursors.Cursor
        )
        return conn
    except Exception as e:
        log_error(f"Database connection error: {str(e)}")
        return None

def fetch_customer_info(cursor, customer_id=None, customer_name=None):
    """
    Retrieves customer information from database.
    
    Args:
        cursor: Database cursor object
        customer_id (int, optional): Customer's unique identifier
        customer_name (str, optional): Customer's name for search
        
    Returns:
        tuple: Customer records if found
        None: If no customer found or error occurs
        
    At least one of customer_id or customer_name must be provided.
    """
    try:
        if customer_id:
            cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
        elif customer_name:
            cursor.execute("SELECT * FROM customers WHERE name LIKE %s", (f"%{customer_name}%",))
        else:
            return None
        return cursor.fetchall()
    except Exception as e:
        log_error(f"Error fetching customer info: {str(e)}")
        return None

def fetch_statements(cursor, customer_id):
    """
    Retrieves all statements for a given customer.
    
    Args:
        cursor: Database cursor object
        customer_id (int): Customer's unique identifier
        
    Returns:
        list: Statement records if found
        None: If no statements found or error occurs
    """
    try:
        cursor.execute("SELECT * FROM statements WHERE customer_id = %s", (customer_id,))
        return cursor.fetchall()
    except Exception as e:
        log_error(f"Error fetching statements: {str(e)}")
        return None

def fetch_transactions(cursor, statement_id):
    """
    Retrieves all transactions for a given statement.
    
    Args:
        cursor: Database cursor object
        statement_id (int): Statement's unique identifier
        
    Returns:
        list: Transaction records (date, description, amount, type)
        None: If no transactions found or error occurs
    """
    try:
        cursor.execute("SELECT txn_date, description, amount, txn_type FROM transactions WHERE statement_id = %s", (statement_id,))
        return cursor.fetchall()
    except Exception as e:
        log_error(f"Error fetching transactions: {str(e)}")
        return None

# Translation dictionary
translations = {
    "en": {
        "CIMB": "CIMB",
        "STATEMENT DATE": "STATEMENT DATE",
        "STATEMENT PERIOD": "STATEMENT PERIOD",
        "Credit Card eStatement Campaign 2024": "Credit Card eStatement Campaign 2024",
        "Switch to eStatements...": "Switch to eStatements now and stand a chance to win exciting prizes! Go paperless to reduce your carbon footprint and enjoy hassle-free banking.",
        "ACCOUNT SUMMARY": "ACCOUNT SUMMARY",
        "TOTAL OUTSTANDING BALANCE": "TOTAL OUTSTANDING BALANCE",
        "MINIMUM PAYMENT DUE": "MINIMUM PAYMENT DUE",
        "PAYMENT DUE DATE": "PAYMENT DUE DATE",
        "REWARDS POINTS BALANCE": "REWARDS POINTS BALANCE",
        "PAYMENT & TRANSACTIONS SUMMARY": "PAYMENT & TRANSACTIONS SUMMARY",
        "TRANSACTION DETAILS": "TRANSACTION DETAILS",
        "Date": "Date",
        "Description": "Description",
        "Amount": "Amount",
        "Credit Limit": "Credit Limit",
        "Available Credit": "Available Credit",
        "Previous Balance": "Previous Balance",
        "Payments": "Payments",
        "Purchases": "Purchases",
        "Cash Advances": "Cash Advances",
        "Fees and Charges": "Fees and Charges",
        "Interest Charges": "Interest Charges",
        "Current Balance": "Current Balance"
    },
    "ta": {
        "CIMB": "CIMB",
        "STATEMENT DATE": "அறிக்கை தேதி",
        "STATEMENT PERIOD": "அறிக்கை காலம்",
        "Credit Card eStatement Campaign 2024": "கிரெடிட் கார்டு மின்-அறிக்கை பிரச்சாரம் 2024",
        "Switch to eStatements...": "மின்-அறிக்கைகளுக்கு மாறி பரிசுகளை வெல்லுங்கள்! காகிதமில்லா வங்கி சேவையை அனுபவியுங்கள்.",
        "ACCOUNT SUMMARY": "கணக்கு சுருக்கம்",
        "TOTAL OUTSTANDING BALANCE": "மொத்த நிலுவை இருப்பு",
        "MINIMUM PAYMENT DUE": "குறைந்தபட்ச செலுத்த வேண்டிய தொகை",
        "PAYMENT DUE DATE": "பணம் செலுத்த வேண்டிய தேதி",
        "REWARDS POINTS BALANCE": "ரிவார்ட்ஸ் பாயிண்ட்ஸ் இருப்பு",
        "PAYMENT & TRANSACTIONS SUMMARY": "பணம் செலுத்துதல் & பரிவர்த்தனை சுருக்கம்",
        "TRANSACTION DETAILS": "பரிவர்த்தனை விவரங்கள்",
        "Date": "தேதி",
        "Description": "விவரம்",
        "Amount": "தொகை",
        "Credit Limit": "கடன் வரம்பு",
        "Available Credit": "கிடைக்கக்கூடிய கடன்",
        "Previous Balance": "முந்தைய இருப்பு",
        "Payments": "செலுத்திய தொகைகள்",
        "Purchases": "கொள்முதல்கள்",
        "Cash Advances": "பண முன்பணம்",
        "Fees and Charges": "கட்டணங்கள்",
        "Interest Charges": "வட்டி கட்டணங்கள்",
        "Current Balance": "தற்போதைய இருப்பு"
    },
    "th": {
        "CIMB": "CIMB",
        "STATEMENT DATE": "วันที่ออกใบแจ้งยอด",
        "STATEMENT PERIOD": "ระยะเวลาใบแจ้งยอด",
        "Credit Card eStatement Campaign 2024": "แคมเปญ eStatement บัตรเครดิต 2024",
        "Switch to eStatements...": "เปลี่ยนมาใช้ eStatement ลุ้นรับของรางวัล! ลดคาร์บอนฟุตพริ้นท์และทำธุรกรรมง่ายขึ้น",
        "ACCOUNT SUMMARY": "สรุปบัญชี",
        "TOTAL OUTSTANDING BALANCE": "ยอดค้างชำระทั้งหมด",
        "MINIMUM PAYMENT DUE": "ยอดชำระขั้นต่ำ",
        "PAYMENT DUE DATE": "วันครบกำหนดชำระเงิน",
        "REWARDS POINTS BALANCE": "ยอดคะแนนสะสม",
        "PAYMENT & TRANSACTIONS SUMMARY": "สรุปการชำระเงินและรายการ",
        "TRANSACTION DETAILS": "รายละเอียดรายการ",
        "Date": "วันที่",
        "Description": "รายละเอียด",
        "Amount": "จำนวนเงิน",
        "Credit Limit": "วงเงินเครดิต",
        "Available Credit": "เครดิตคงเหลือ",
        "Previous Balance": "ยอดคงเหลือก่อนหน้า",
        "Payments": "การชำระเงิน",
        "Purchases": "ยอดใช้จ่าย",
        "Cash Advances": "เบิกเงินสดล่วงหน้า",
        "Fees and Charges": "ค่าธรรมเนียมและค่าใช้จ่าย",
        "Interest Charges": "ดอกเบี้ย",
        "Current Balance": "ยอดปัจจุบัน"
    },
    
    "vi": {
        "CIMB": "CIMB",
        "STATEMENT DATE": "NGÀY SAO KÊ",
        "STATEMENT PERIOD": "KỲ SAO KÊ",
        "Credit Card eStatement Campaign 2024": "Chiến dịch Sao kê điện tử Thẻ tín dụng 2024",
        "Switch to eStatements...": "Chuyển sang sao kê điện tử để có cơ hội nhận giải thưởng! Giảm thiểu dấu chân carbon và trải nghiệm ngân hàng tiện lợi.",
        "ACCOUNT SUMMARY": "TÓM TẮT TÀI KHOẢN",
        "TOTAL OUTSTANDING BALANCE": "TỔNG SỐ DƯ NỢ",
        "MINIMUM PAYMENT DUE": "SỐ TIỀN THANH TOÁN TỐI THIỂU",
        "PAYMENT DUE DATE": "NGÀY HẾT HẠN THANH TOÁN",
        "REWARDS POINTS BALANCE": "SỐ DƯ ĐIỂM THƯỞNG",
        "PAYMENT & TRANSACTIONS SUMMARY": "TÓM TẮT GIAO DỊCH VÀ THANH TOÁN",
        "TRANSACTION DETAILS": "CHI TIẾT GIAO DỊCH",
        "Date": "Ngày",
        "Description": "Mô tả",
        "Amount": "Số tiền",
        "Credit Limit": "Hạn mức tín dụng",
        "Available Credit": "Tín dụng còn lại"
    },
    "tl": {
        "CIMB": "CIMB",
        "STATEMENT DATE": "PETSA NG PAHAYAG",
        "STATEMENT PERIOD": "PANAHON NG PAHAYAG",
        "Credit Card eStatement Campaign 2024": "Kampanya ng eStatement ng Credit Card 2024",
        "Switch to eStatements...": "Lumipat sa eStatements at magkaroon ng pagkakataong manalo ng magagandang premyo! Mag-go green at gawing madali ang pagbabangko.",
        "ACCOUNT SUMMARY": "BUOD NG ACCOUNT",
        "TOTAL OUTSTANDING BALANCE": "KABUUANG BALANSENG NATITIRA",
        "MINIMUM PAYMENT DUE": "MINIMUM NA BAYAD",
        "PAYMENT DUE DATE": "PETSANG HULING BAYAD",
        "REWARDS POINTS BALANCE": "BALANSENG PUNTOS NG GANTIMPALA",
        "PAYMENT & TRANSACTIONS SUMMARY": "BUOD NG BAYAD AT TRANSAKSYON",
        "TRANSACTION DETAILS": "DETALYE NG TRANSAKSYON",
        "Date": "Petsa",
        "Description": "Paglalarawan",
        "Amount": "Halaga",
        "Credit Limit": "Limitasyon ng Credit",
        "Available Credit": "Magagamit na Credit"
    },
    "en-gb": {
        "CIMB": "CIMB",
        "STATEMENT DATE": "STATEMENT DATE",
        "STATEMENT PERIOD": "STATEMENT PERIOD",
        "Credit Card eStatement Campaign 2024": "Credit Card eStatement Campaign 2024",
        "Switch to eStatements...": "Switch to eStatements now and stand a chance to win exciting prizes! Go paperless to reduce your carbon footprint and enjoy hassle-free banking.",
        "ACCOUNT SUMMARY": "ACCOUNT SUMMARY",
        "TOTAL OUTSTANDING BALANCE": "TOTAL OUTSTANDING BALANCE",
        "MINIMUM PAYMENT DUE": "MINIMUM PAYMENT DUE",
        "PAYMENT DUE DATE": "PAYMENT DUE DATE",
        "REWARDS POINTS BALANCE": "REWARDS POINTS BALANCE",
        "PAYMENT & TRANSACTIONS SUMMARY": "PAYMENT & TRANSACTIONS SUMMARY",
        "TRANSACTION DETAILS": "TRANSACTION DETAILS",
        "Date": "Date",
        "Description": "Description",
        "Amount": "Amount",
        "Credit Limit": "Credit Limit",
        "Available Credit": "Available Credit"
    },
    "th": {
        "CIMB": "CIMB",
        "STATEMENT DATE": "วันที่ออกใบแจ้งยอด",
        "STATEMENT PERIOD": "ระยะเวลาใบแจ้งยอด",
        "Credit Card eStatement Campaign 2024": "แคมเปญ eStatement บัตรเครดิต 2024",
        "Switch to eStatements...": "เปลี่ยนมาใช้ eStatement ลุ้นรับของรางวัล! ลดคาร์บอนฟุตพริ้นท์และทำธุรกรรมง่ายขึ้น",
        "ACCOUNT SUMMARY": "สรุปบัญชี",
        "TOTAL OUTSTANDING BALANCE": "ยอดค้างชำระทั้งหมด",
        "MINIMUM PAYMENT DUE": "ยอดชำระขั้นต่ำ",
        "PAYMENT DUE DATE": "วันครบกำหนดชำระเงิน",
        "REWARDS POINTS BALANCE": "ยอดคะแนนสะสม",
        "PAYMENT & TRANSACTIONS SUMMARY": "สรุปการชำระเงินและรายการ",
        "TRANSACTION DETAILS": "รายละเอียดรายการ",
        "Date": "วันที่",
        "Description": "รายละเอียด",
        "Amount": "จำนวนเงิน",
        "Credit Limit": "วงเงินเครดิต",
        "Available Credit": "เครดิตคงเหลือ"
    },
    "ta": {
        "CIMB": "CIMB",
        "STATEMENT DATE": "அறிக்கை தேதி",
        "STATEMENT PERIOD": "அறிக்கை காலம்",
        "Credit Card eStatement Campaign 2024": "கிரெடிட் கார்டு மின்-அறிக்கை பிரச்சாரம் 2024",
        "Switch to eStatements...": "மின்-அறிக்கைகளுக்கு மாறி பரிசுகளை வெல்லுங்கள்! காகிதமில்லா வங்கி சேவையை அனுபவியுங்கள்.",
        "ACCOUNT SUMMARY": "கணக்கு சுருக்கம்",
        "TOTAL OUTSTANDING BALANCE": "மொத்த நிலுவை இருப்பு",
        "MINIMUM PAYMENT DUE": "குறைந்தபட்ச செலுத்த வேண்டிய தொகை",
        "PAYMENT DUE DATE": "பணம் செலுத்த வேண்டிய தேதி",
        "REWARDS POINTS BALANCE": "ரிவார்ட்ஸ் பாயிண்ட்ஸ் இருப்பு",
        "PAYMENT & TRANSACTIONS SUMMARY": "பணம் செலுத்துதல் & பரிவர்த்தனை சுருக்கம்",
        "TRANSACTION DETAILS": "பரிவர்த்தனை விவரங்கள்",
        "Date": "தேதி",
        "Description": "விவரம்",
        "Amount": "தொகை",
        "Credit Limit": "கடன் வரம்பு",
        "Available Credit": "கிடைக்கக்கூடிய கடன்",
        "Previous Balance": "முந்தைய இருப்பு",
        "Payments": "செலுத்திய தொகைகள்",
        "Purchases": "கொள்முதல்கள்",
        "Cash Advances": "பண முன்பணம்",
        "Fees and Charges": "கட்டணங்கள்",
        "Interest Charges": "வட்டி கட்டணங்கள்",
        "Current Balance": "தற்போதைய இருப்பு"
    },
}

def tr(key, lang):
    return translations.get(lang, translations["en"]).get(key, key)

def generate_pdf(customer, statement, transactions, lang="en"):
    try:
        # Get appropriate font for the language
        font_file = FONT_MAPPING.get(lang, "NotoSans-Regular.ttf")
        font_path = f"fonts/{font_file}"
        
        # Get bold font path based on language
        if lang == "ta":
            bold_font_path = "fonts/NotoSansTamil-Bold.ttf"
        elif lang == "th":
            bold_font_path = "fonts/NotoSansThai-Bold.ttf"
        else:
            bold_font_path = "fonts/NotoSans-Bold.ttf"
        
        # Check if fonts exist
        if not os.path.exists(font_path) or not os.path.exists(bold_font_path):
            log_error(f"Font files not found. Regular: {font_path}, Bold: {bold_font_path}")
            return None
        
        pdf = FPDF()
        
        # Function to add borders to any page
        def add_page_borders(pdf_obj):
            pdf_obj.set_draw_color(0, 0, 0)  # Black color for border
            pdf_obj.rect(5, 5, pdf_obj.w - 10, pdf_obj.h - 10)  # Outer border
            pdf_obj.rect(7, 7, pdf_obj.w - 14, pdf_obj.h - 14)  # Inner border
        
        # Override the add_page method to always include borders
        original_add_page = pdf.add_page
        def new_add_page(*args, **kwargs):
            original_add_page(*args, **kwargs)
            add_page_borders(pdf)
        pdf.add_page = new_add_page
        
        pdf.add_page()
        pdf.add_font("Noto", "", font_path, uni=True)
        pdf.add_font("Noto", "B", bold_font_path, uni=True)
        
        # Remove the original border code since it's now handled automatically
        # Get customer and statement info
        name, address, card_no, acc_no, credit_limit, available_credit = customer[1:7]
        stmt_date, period_start, period_end, out_bal, min_due, due_date, points = statement[2:]

        # Convert dates to strings before using in PDF
        stmt_date_str = stmt_date.strftime('%d-%m-%Y') if isinstance(stmt_date, datetime.date) else str(stmt_date)
        period_start_str = period_start.strftime('%d-%m-%Y') if isinstance(period_start, datetime.date) else str(period_start)
        period_end_str = period_end.strftime('%d-%m-%Y') if isinstance(period_end, datetime.date) else str(period_end)
        due_date_str = due_date.strftime('%d-%m-%Y') if isinstance(due_date, datetime.date) else str(due_date)

        # Add logo and title
        logo_path = "static/images/cimb_logo.png"
        if os.path.exists(logo_path):
            pdf.image(logo_path, x=10, y=10, w=30)
            pdf.ln(10)
        else:
            log_error("CIMB logo not found")
            pdf.ln(5)
        
        # Centered title with less spacing
        pdf.set_font("Noto", "B", 14)
        pdf.set_text_color(128, 0, 0)
        pdf.cell(0, 10, "Credit Card Statement CIMB Bank", align='C', ln=True)
        
        # Statement date with centered format
        pdf.set_font("Noto", "", 10)
        pdf.set_text_color(0, 0, 0)
        #pdf.cell(0, 6, f"{tr('STATEMENT DATE', lang)}: {stmt_date_str}          {tr('STATEMENT', lang)}: {period_start_str} - {period_end_str}", align='C', ln=True)
        pdf.cell(120, 6, f"{tr('STATEMENT DATE', lang)}: {stmt_date_str}", ln=False)
        #pdf.cell(0, 6, f"Page 1/1", align='R', ln=True)  # Changed format and alignment
        pdf.cell(0, 6, f"{tr('      STATEMENT ', lang)}: {period_start_str} - {period_end_str}", ln=True)
        # Continue with customer info
        pdf.ln(5)
        pdf.set_font("Noto", "B", 12)
        pdf.cell(120, 8, name.upper(), ln=False)
        pdf.set_font("Noto", "", 10)
        pdf.cell(0, 8, "CIMB VISA PLATINUM", align='R', ln=True)

        # Address and card details
        for line in address.split('\n'):
            pdf.cell(120, 6, line, ln=False)
            if line == address.split('\n')[0]:  # First line
                pdf.cell(0, 6, f"{tr('Credit Limit', lang)}: RM {float(credit_limit):,.2f}", align='R', ln=True)
            elif line == address.split('\n')[1]:  # Second line
                pdf.cell(0, 6, f"{tr('Available Credit', lang)}: RM {float(available_credit):,.2f}", align='R', ln=True)
            else:
                pdf.ln()

        pdf.cell(0, 6, f"Card No: {card_no}", ln=True)
        pdf.cell(0, 6, f"Account No: {acc_no}", ln=True)

        # Campaign Banner with improved spacing
        '''
        pdf.ln(8)
        pdf.set_fill_color(255, 230, 230)
        pdf.set_text_color(128, 0, 0)
        pdf.set_font("Noto", "B", 11)
        pdf.rect(10, pdf.get_y(), pdf.w - 20, 20, 'F')
        pdf.set_xy(15, pdf.get_y() + 2)
        pdf.cell(0, 8, tr("Credit Card eStatement Campaign 2024", lang), ln=True)
        pdf.set_font("Noto", "", 9)
        pdf.set_xy(15, pdf.get_y())
        pdf.multi_cell(pdf.w - 30, 4, tr("Switch to eStatements...", lang))
        '''
        # Account Summary with grid layout
        pdf.ln(8)
        pdf.set_font("Noto", "B", 12)
        pdf.set_text_color(128, 0, 0)
        pdf.cell(0, 8, tr("ACCOUNT SUMMARY", lang), ln=True)

        # Create a grid for account summary
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Noto", "", 10)
        grid_width = (pdf.w - 20) / 2
        
        # Row 1
        pdf.set_fill_color(245, 245, 245)
        pdf.rect(10, pdf.get_y(), grid_width, 20, 'F')
        pdf.rect(10 + grid_width, pdf.get_y(), grid_width, 20, 'F')
        
        pdf.set_xy(15, pdf.get_y() + 2)
        pdf.set_font("Noto", "B", 9)
        pdf.cell(grid_width - 10, 5, tr("TOTAL OUTSTANDING BALANCE", lang), ln=False)
        pdf.cell(grid_width - 10, 5, tr("MINIMUM PAYMENT DUE", lang), ln=True)
        
        pdf.set_xy(15, pdf.get_y() + 2)
        pdf.set_font("Noto", "", 11)
        pdf.cell(grid_width - 10, 5, f"RM {float(out_bal):,.2f}", ln=False)
        pdf.cell(grid_width - 10, 5, f"RM {float(min_due):,.2f}", ln=True)

        # Row 2
        pdf.ln(8)
        pdf.set_fill_color(245, 245, 245)
        pdf.rect(10, pdf.get_y(), grid_width, 20, 'F')
        pdf.rect(10 + grid_width, pdf.get_y(), grid_width, 20, 'F')
        
        pdf.set_xy(15, pdf.get_y() + 2)
        pdf.set_font("Noto", "B", 9)
        pdf.cell(grid_width - 10, 5, tr("PAYMENT DUE DATE", lang), ln=False)
        pdf.cell(grid_width - 10, 5, tr("REWARDS POINTS BALANCE", lang), ln=True)
        
        pdf.set_xy(15, pdf.get_y() + 2)
        pdf.set_font("Noto", "", 11)
        pdf.cell(grid_width - 10, 5, due_date_str, ln=False)
        pdf.cell(grid_width - 10, 5, f"{int(points):,} pts", ln=True)

        # Transaction Summary
        pdf.ln(4)
        pdf.set_font("Noto", "B", 12)
        pdf.set_text_color(128, 0, 0)  # Set color to red
        pdf.cell(0, 8, tr("PAYMENT & TRANSACTIONS SUMMARY", lang), ln=True)
        pdf.set_text_color(0, 0, 0)  # Reset color back to black
        pdf.ln(4)
        categories = {
            "Previous Balance": 0.00,
            "Payments": 0.00,
            "Purchases": 0.00,
            "Cash Advances": 0.00,
            "Fees and Charges": 0.00,
            "Interest Charges": 0.00,
            "Current Balance": float(out_bal)
        }

        for txn in transactions:
            amount = float(txn[2])
            ttype = txn[3]
            if "Payment" in ttype:
                categories["Payments"] += amount
            elif "Purchase" in ttype:
                categories["Purchases"] += amount
            elif "Cash Advance" in ttype:
                categories["Cash Advances"] += amount
            elif "Fee" in ttype:
                categories["Fees and Charges"] += amount
            elif "Interest" in ttype:
                categories["Interest Charges"] += amount

        pdf.set_font("Noto", "", 10)
        for k, v in categories.items():
            sign = "+" if v > 0 and k != "Payments" else ""
            pdf.cell(120, 6, k)
            pdf.cell(0, 6, f"{sign} RM {abs(v):,.2f}", ln=True)

        # Transaction Details
        pdf.ln(4)
        pdf.set_font("Noto", "B", 12)  # Changed to bold
        pdf.set_text_color(128, 0, 0)
        pdf.cell(0, 8, tr("TRANSACTION DETAILS", lang), ln=True)

        # Current Account Transaction Details header with underline
        pdf.ln(5)
        pdf.set_draw_color(200, 200, 200)  # Light gray for underline
        pdf.line(10, pdf.get_y(), pdf.w - 10, pdf.get_y())  # Add underline
        pdf.set_font("Noto", "", 10)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(2)
        pdf.cell(0, 6, "Current Account Transaction Details / Butir-butir Transaksi Akaun Semasa", ln=True)

        # Account number with protection notice - better aligned
        pdf.ln(2)
        pdf.set_font("Noto", "", 9)
        pdf.cell(60, 6, "Account No / No Akaun", ln=False)
        pdf.cell(40, 6, "80-0024165-6", ln=False)
        pdf.set_font("Noto", "", 8)  # Changed from "I" to ""
        pdf.cell(0, 6, "(Eligible for Protection by PIDM)", ln=True)
        

        # Table with improved styling
        pdf.ln(2)
        
        def draw_table_header(pdf):
            # Column headers with proper width and alignment
            col_widths = [25, 90, 30, 30, 0]  # Adjusted width distribution
            headers = ["Date", "Description", "Withdrawal", "Deposits", "Balance"]
            
            pdf.set_fill_color(235, 235, 235)  # Lighter gray for better readability
            pdf.set_draw_color(100, 100, 100)  # Darker border for contrast
            pdf.set_font("Noto", "B", 9)  # Slightly larger font for headers
            
            for i, (width, header) in enumerate(zip(col_widths, headers)):
                pdf.cell(width, 12, header, border=1, fill=True, align='C')
            pdf.ln()
            return col_widths

        # Initial table header
        col_widths = draw_table_header(pdf)

        # Data rows with improved styling
        pdf.set_font("Noto", "B", 8)  # Set all table data to bold
        pdf.set_fill_color(245, 245, 245)
        pdf.set_draw_color(180, 180, 180)
        row_height = 7
        alternate = False
        running_balance = 0.00

        # Transaction rows with page break handling
        for txn in transactions:
            # Check if we need a new page
            if pdf.get_y() + row_height > pdf.h - 35:  # Leave space for footer
                pdf.add_page()
                # Redraw table header on new page
                col_widths = draw_table_header(pdf)
            
            alternate = not alternate
            date, desc, amount, _ = txn
            date_str = date.strftime('%d-%m-%Y') if isinstance(date, datetime.date) else str(date)
            amount_float = float(amount)
            running_balance += amount_float
            withdrawal = f"{abs(amount_float):,.2f}" if amount_float < 0 else ""
            deposit = f"{amount_float:,.2f}" if amount_float > 0 else ""
            
            # All cells now use bold font
            pdf.cell(col_widths[0], row_height, " " + date_str, border=1, fill=alternate, align='L')
            pdf.cell(col_widths[1], row_height, " " + str(desc), border=1, fill=alternate, align='L')
            pdf.cell(col_widths[2], row_height, withdrawal + " ", border=1, align='R', fill=alternate)
            pdf.cell(col_widths[3], row_height, deposit + " ", border=1, align='R', fill=alternate)
            pdf.cell(col_widths[4], row_height, f"{running_balance:,.2f} ", border=1, align='R', fill=alternate, ln=True)

        # Closing balance row with enhanced styling
        pdf.set_font("Noto", "B", 8)
        pdf.set_draw_color(100, 100, 100)  # Darker border for closing balance
        pdf.cell(115, row_height, " CLOSING BALANCE", border=1, ln=False, fill=True)
        pdf.cell(30, row_height, "", border=1, fill=True)
        pdf.cell(30, row_height, "", border=1, fill=True)
        pdf.cell(0, row_height, f"{running_balance:,.2f} ", border=1, align='R', fill=True, ln=True)

        # Add End of Statement text
        pdf.ln(4)
        pdf.set_font("Noto", "", 8)
        #pdf.cell(0, 6, "*** End of Statement / Penyata Tamat ***", align='C', ln=True)

        # Add SAMPLE ONLY watermark
        pdf.set_font("Noto", "B", 48)
        pdf.set_text_color(200, 200, 200)
        pdf.set_xy(0, pdf.get_y() + 10)
        #pdf.cell(pdf.w, 20, "SAMPLE ONLY", align='C', ln=True)

        # Add Important Notice section with border
        pdf.ln(4)
        pdf.set_draw_color(0, 0, 0)  # Black border
        pdf.rect(10, pdf.get_y(), pdf.w - 20, 35)  # Adjusted height for content
        
        # Add Important Notice title
        pdf.set_font("Noto", "B", 8)
        pdf.set_text_color(0, 0, 0)
        pdf.set_xy(12, pdf.get_y() + 2)
        pdf.cell(0, 3, "Important Notice / Notis Penting", ln=True)
        
        # Add GENERIC MESSAGES
        pdf.set_font("Noto", "B", 8)
        pdf.set_xy(12, pdf.get_y() + 1)
        pdf.cell(0, 3, "GENERIC MESSAGES", ln=True)
        
        # Add main notice text in box
        pdf.set_font("Noto", "", 7)
        pdf.set_xy(12, pdf.get_y() + 2)
        pdf.multi_cell(pdf.w - 24, 3, 
            "The Bank must be informed of any error, irregularities or discrepancies in this statement within 14 days from the date of the statement, " +
            "failing which the information reflected in this statement is deemed to be correct and accurate. Please log into CIMB Bank or CIMB Islamic Bank " +
            "website at www.cimbbank.com.my or www.cimbislamic.com.my for the statement's explanatory notes.")

        # Add second paragraph outside the box
        pdf.ln(1)
        pdf.set_xy(12, pdf.get_y() + 2)
        pdf.multi_cell(pdf.w - 24, 3, 
            "You can perform fund transfers, account enquiries, bill payments, payroll or supplier payments and more via www.cimb-bizchannel.com.my. " +
            "For more information, call our Business Call Center at 1300 888 828 Monday to Friday (7am - 7pm) and Saturday (8am - 5pm) excluding public " +
            "holidays or email us at mybusinesscare@cimb.com")

        # Add reference number with proper alignment
        pdf.ln(1)
        pdf.set_font("Noto", "", 6)
        pdf.set_x(pdf.w - 70)
        pdf.cell(0, 3, "COMSNIS/BS/CCMSNICAI31072017/0108001700003", ln=True)

        # Add End of Statement text
        pdf.ln(4)
        pdf.set_font("Noto", "", 8)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 6, "*** End of Statement / Penyata Tamat ***", align='C', ln=True)

        # Add SAMPLE ONLY watermark
        pdf.set_font("Noto", "B", 48)
        pdf.set_text_color(200, 200, 200)  # Light gray color
        pdf.set_xy(0, pdf.get_y() + 10)
        #pdf.cell(pdf.w, 20, "SAMPLE ONLY", align='C', ln=True)

        filename = f"pdfs/{name.replace(' ', '_')}_Statement_{stmt_date_str}.pdf"
        pdf.output(filename)
        print(f"[✓] Generated: {filename}")
        return filename
    except Exception as e:
        log_error(f"Error generating PDF: {str(e)}")
        return None

@app.route('/')
def index():
    languages = {
        "en": "English",
        "vi": "Vietnamese",
        "tl": "Tagalog",
        "en-gb": "English (UK)"
    }
    return render_template('index.html', languages=languages)

@app.route('/search', methods=['POST'])
def search():
    lang_code = request.form.get('language', 'en')
    search_type = request.form.get('search_type')
    search_value = request.form.get('search_value')
    
    conn = get_db_connection()
    if not conn:
        flash("Database connection error. Please try again.", "error")
        return redirect(url_for('index'))
    
    cursor = conn.cursor()
    
    if search_type == "id":
        customers = fetch_customer_info(cursor, customer_id=search_value)
    else:
        customers = fetch_customer_info(cursor, customer_name=search_value)
    
    conn.close()
    
    if not customers:
        flash("No customers found.", "error")
        return redirect(url_for('index'))
    
    return render_template('customer_list.html', customers=customers, lang_code=lang_code)

@app.route('/statements/<customer_id>/<lang_code>')
def show_statements(customer_id, lang_code):
    conn = get_db_connection()
    if not conn:
        flash("Database connection error. Please try again.", "error")
        return redirect(url_for('index'))
    
    cursor = conn.cursor()
    
    customer = fetch_customer_info(cursor, customer_id=customer_id)
    if not customer or len(customer) == 0:
        conn.close()
        flash("Customer not found.", "error")
        return redirect(url_for('index'))
    
    statements = fetch_statements(cursor, customer_id)
    conn.close()
    
    if not statements:
        flash("No statements found for this customer.", "error")
        return redirect(url_for('index'))
    
    return render_template('statements.html', customer=customer[0], statements=statements, lang_code=lang_code)

@app.route('/generate/<customer_id>/<statement_id>/<lang_code>')
def generate_statement(customer_id, statement_id, lang_code):
    conn = get_db_connection()
    if not conn:
        flash("Database connection error. Please try again.", "error")
        return redirect(url_for('index'))
    
    cursor = conn.cursor()
    
    customer = fetch_customer_info(cursor, customer_id=customer_id)
    if not customer or len(customer) == 0:
        conn.close()
        flash("Customer not found.", "error")
        return redirect(url_for('index'))
    
    statement = None
    statements = fetch_statements(cursor, customer_id)
    if statements:
        for stmt in statements:
            if str(stmt[0]) == statement_id:
                statement = stmt
                break
    
    if not statement:
        conn.close()
        flash("Statement not found.", "error")
        return redirect(url_for('index'))
    
    transactions = fetch_transactions(cursor, statement_id)
    conn.close()
    
    if not transactions:
        flash("No transactions found for this statement.", "warning")
    
    filename = generate_pdf(customer[0], statement, transactions, lang=lang_code)
    
    if not filename:
        flash("Error generating PDF. Check logs for details.", "error")
        return redirect(url_for('index'))
    
    flash(f"PDF generated successfully: {filename}", "success")
    return redirect(url_for('download_pdf', filename=os.path.basename(filename)))

@app.route('/download/<filename>')
def download_pdf(filename):
    return send_from_directory('pdfs', filename, as_attachment=True)

@app.route('/view_customers')
def view_customers():
    conn = get_db_connection()
    if not conn:
        flash("Database connection error. Please try again.", "error")
        return redirect(url_for('index'))
    
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM customers")
        customers = cursor.fetchall()
    except Exception as e:
        log_error(f"Error fetching all customers: {str(e)}")
        customers = []
    
    conn.close()
    
    return render_template('all_customers.html', customers=customers)

if __name__ == "__main__":
    app.run(debug=True)