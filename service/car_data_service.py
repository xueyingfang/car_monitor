from datetime import datetime
import random
import uuid
from dto.car_metric_dto import CarMetricDTO
from dto.error_dto import ErrorDTO
from service.report_service import ReportService

class CarDataService:
    def __init__(self):
        self.report_service = ReportService()
        # 异常判定阈值
        self.temp_high_threshold = 80.0
        self.voltage_low_threshold = 280.0

    def generate_mock_car_data(self) -> CarMetricDTO:
        """模拟生成车辆实时上报指标"""
        car_id_list = ["CAR-001", "CAR-002", "CAR-003", "CAR-004"]
        car_id = random.choice(car_id_list)
        speed = round(random.uniform(0, 120),1)
        temperature = round(random.uniform(40,95),1)
        voltage = round(random.uniform(260,400),2)
        mileage = round(random.uniform(1000,50000),1)
        alarm = temperature > self.temp_high_threshold or voltage < self.voltage_low_threshold

        dto = CarMetricDTO(
            car_id=car_id,
            timestamp=datetime.now(),
            speed=speed,
            temperature=temperature,
            voltage=voltage,
            mileage=mileage,
            alarm_status=alarm
        )
        return dto

    def filter_and_handle_data(self, dto: CarMetricDTO) -> CarMetricDTO:
        """过滤数据；异常构造ErrorDTO交给存储上报服务"""
        if dto.alarm_status:
            # 构造错误DTO
            err_code = ""
            err_msg = ""
            if dto.temperature > self.temp_high_threshold:
                err_code = "TEMP_HIGH"
                err_msg = f"电机温度过高：{dto.temperature}℃"
            if dto.voltage < self.voltage_low_threshold:
                err_code = "VOLT_LOW"
                err_msg = f"电池电压过低：{dto.voltage}V"

            error_dto = ErrorDTO(
                error_id=str(uuid.uuid4()),
                occur_time=datetime.now(),
                car_metric=dto,
                error_code=err_code,
                error_msg=err_msg
            )
            self.report_service.save_abnormal_data(error_dto)
            self.report_service.mock_report(error_dto)
        return dto
