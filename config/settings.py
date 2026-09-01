"""系统配置，统一管理阈值、文件、接口地址"""

# 异常阈值
THRESHOLD = {
    "battery_voltage_min": 320,
    "battery_voltage_max": 420,
    "motor_temp_max": 85,
    "car_speed_max": 120,
}

# 文件输出
ERROR_DATA_FILE = "car_error_data.json"

# 上报接口
REPORT_URL = "http://127.0.0.1:8000/report"

# GUI刷新间隔 ms
GUI_REFRESH_INTERVAL = 1000
