from typing import Optional
from config.settings import THRESHOLD
from dto.car_data_dto import CarDataDTO
from dto.error_record_dto import ErrorRecordDTO
from utils.file_util import read_json_file, write_json_file
from config.settings import ERROR_DATA_FILE


class AbnormalService:
    """异常判断、异常数据持久化存储"""

    @staticmethod
    def check_abnormal(dto: CarDataDTO) -> Optional[str]:
        """校验数据，返回异常描述；正常返回None"""
        err_list = []
        if not (THRESHOLD["battery_voltage_min"] <= dto.battery_voltage <= THRESHOLD["battery_voltage_max"]):
            err_list.append(f"电池电压异常:{dto.battery_voltage}")
        if dto.motor_temp > THRESHOLD["motor_temp_max"]:
            err_list.append(f"电机温度过高:{dto.motor_temp}")
        if dto.car_speed > THRESHOLD["car_speed_max"]:
            err_list.append(f"车速超限:{dto.car_speed}")
        if dto.fault_code != "":
            err_list.append(f"存在故障码:{dto.fault_code}")

        if len(err_list) > 0:
            return ";".join(err_list)
        return None

    @staticmethod
    def save_error_record(dto: CarDataDTO, error_msg: str) -> ErrorRecordDTO:
        """保存异常记录到本地json文件"""
        record = ErrorRecordDTO(
            car_id=dto.car_id,
            collect_time=dto.timestamp,
            raw_data=dto,
            error_reason=error_msg
        )
        arr = read_json_file(ERROR_DATA_FILE)
        arr.append(record.to_dict())
        write_json_file(ERROR_DATA_FILE, arr)
        return record
