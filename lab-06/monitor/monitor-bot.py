import psutil
import logging
import time
import asyncio
from telegram import Bot

# Thay thế 'YOUR_BOT_TOKEN' bằng mã truy cập API của bot bạn đã tạo
BOT_TOKEN = '8128024276:AAH2KadCrsBBiF7MhIIO1YzgBR2T-_ljx_c'

# Thay thế 'YOUR_CHAT_ID' bằng chat id của nhóm bạn muốn gửi thông báo tới
CHAT_ID = '-4791683262'  # Đảm bảo đây là dạng chuỗi (string)

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    filename="system_monitor_bot.log",
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()


# Hàm ghi log
def log_info(category, message):
    """Ghi thông tin vào log file và in ra console."""
    log_entry = f"{category}: {message}"
    logging.info(log_entry)
    print(log_entry)


# Hàm gửi tin nhắn qua Telegram (async)
async def send_telegram_message(message):
    """Gửi tin nhắn văn bản đến chat_id đã cấu hình."""
    try:
        bot = Bot(token=BOT_TOKEN)
        await bot.send_message(chat_id=CHAT_ID, text=message)
        log_info("Telegram", "Message sent successfully.")
    except Exception as e:
        log_info("Telegram Error", f"Failed to send message: {e}")


# Hàm giám sát CPU và bộ nhớ
def monitor_cpu_memory():
    """Lấy thông tin CPU, Memory và gửi cảnh báo nếu cần."""
    try:
        cpu_percent = psutil.cpu_percent(interval=1) # Thêm interval để có kết quả chính xác hơn
        memory_info = psutil.virtual_memory()

        log_info("CPU", f"Usage: {cpu_percent}%")
        log_info("Memory", f"Usage: {memory_info.percent}%")

        # Gửi thông báo qua Telegram
        # Thêm \n để xuống dòng trong tin nhắn Telegram cho dễ đọc
        message = f"CPU Usage: {cpu_percent}%\nMemory Usage: {memory_info.percent}%"

        # Chạy hàm async để gửi tin nhắn
        # Lưu ý: asyncio.run() tạo một event loop mới mỗi lần gọi.
        # Đối với script đơn giản này thì ổn, nhưng nếu phức tạp hơn,
        # nên có một event loop chính chạy toàn bộ phần async.
        asyncio.run(send_telegram_message(message))

    except Exception as e:
        log_info("Monitoring Error", f"Error in monitor_cpu_memory: {e}")


# Hàm thực hiện giám sát toàn bộ hệ thống
def monitor_system():
    """Vòng lặp chính để giám sát hệ thống liên tục."""
    log_info("System Monitor", "Starting system monitoring...")

    while True:
        try:
            monitor_cpu_memory()
            log_info("System Monitor", "---------------------------------------")
            # Chờ 60 giây trước khi kiểm tra lại
            time.sleep(60)
        except KeyboardInterrupt:
            log_info("System Monitor", "Monitoring stopped by user (Ctrl+C).")
            break
        except Exception as e:
            log_info("System Monitor Error", f"Unhandled error in main loop: {e}")
            # Chờ một chút trước khi thử lại nếu có lỗi không mong muốn
            time.sleep(30)


# Điểm bắt đầu thực thi chương trình
if __name__ == "__main__":
    monitor_system()