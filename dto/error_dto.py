from dataclasses import dataclass
from datetime import datetime
from dto.car_metric_dto import CarMetricDTO

@dataclass
class ErrorDTO:
    """异常数据DTO：封装车辆原始指标 + 错误信息"""
    error_id: str               # 异常编号
    occur_time: datetime        # 异常发生时间
    car_metric: CarMetricDTO   # 完整车辆原始指标对象
    error_code: str             # 错误码，如 TEMP_HIGH / VOLT_LOW
    error_msg: str              # 错误描述文本

    def to_json_dict(self):
        """转用于持久化json字典"""
        return {
            "error_id": self.error_id,
            "occur_time": self.occur_time.strftime("%Y-%m-%d %H:%M:%S"),
            "car_id": self.car_metric.car_id,
            "speed": self.car_metric.speed,
            "temperature": self.car_metric.temperature,
            "voltage": self.car_metric.voltage,
            "mileage": self.car_metric.mileage,
            "error_code": self.error_code,
            "error_msg": self.error_msg
        }
