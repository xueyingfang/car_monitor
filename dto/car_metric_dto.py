from dataclasses import dataclass
from datetime import datetime

@dataclass
class CarMetricDTO:
    """车辆实时指标DTO"""
    car_id: str          # 车辆编号
    timestamp: datetime   # 上报时间
    speed: float         # 车速 km/h
    temperature: float   # 电机温度
    voltage: float       # 电池电压
    mileage: float       # 里程
    alarm_status: bool   # 是否异常 True=有问题数据

    def to_table_row(self):
        """转为GUI表格一行数据"""
        return (
            self.car_id,
            self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            f"{self.speed:.1f}",
            f"{self.temperature:.1f}",
            f"{self.voltage:.2f}",
            f"{self.mileage:.1f}",
            "异常" if self.alarm_status else "正常"
        )
