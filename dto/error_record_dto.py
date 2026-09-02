from dataclasses import dataclass
from dto.car_data_dto import CarDataDTO

@dataclass
class ErrorRecordDTO:
    """异常记录，用于本地存储 + http上报"""
    car_id: str
    collect_time: str
    raw_data: CarDataDTO
    error_reason: str

    def to_dict(self):
        """序列化，CarDataDTO转为字典"""
        return {
            "car_id": self.car_id,
            "collect_time": self.collect_time,
            "raw_data": {
                "car_id": self.raw_data.car_id,
                "timestamp": self.raw_data.timestamp,
                "car_speed": self.raw_data.car_speed,
                "battery_voltage": self.raw_data.battery_voltage,
                "motor_temp": self.raw_data.motor_temp,
                "mileage": self.raw_data.mileage,
                "fault_code": self.raw_data.fault_code,
            },
            "error_reason": self.error_reason
        }
