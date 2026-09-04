import json
import os
from datetime import datetime
from typing import List, Optional
from dto.error_dto import ErrorDTO
from dto.car_metric_dto import CarMetricDTO
from utils.log_util import log


class ErrorQueryService:
    """读取本地abnormal_car_data.json，解析还原为ErrorDTO对象"""
    def __init__(self, json_file_path: str = "abnormal_car_data.json"):
        self.json_file_path = json_file_path

    def load_all_error(self) -> List[ErrorDTO]:
        """加载全部异常记录，返回ErrorDTO对象列表"""
        if not os.path.exists(self.json_file_path):
            log.warn(f"异常文件不存在：{self.json_file_path}，返回空列表")
            return []
        try:
            with open(self.json_file_path, "r", encoding="utf-8") as f:
                json_list = json.load(f)
        except Exception as e:
            log.error(f"读取异常json文件失败: {str(e)}")
            return []

        result: List[ErrorDTO] = []
        for item in json_list:
            car_metric = CarMetricDTO(
                car_id=item["car_id"],
                timestamp=datetime.strptime(item["occur_time"], "%Y-%m-%d %H:%M:%S"),
                speed=item["speed"],
                temperature=item["temperature"],
                voltage=item["voltage"],
                mileage=item["mileage"],
                alarm_status=True
            )
            err_dto = ErrorDTO(
                error_id=item["error_id"],
                occur_time=datetime.strptime(item["occur_time"], "%Y-%m-%d %H:%M:%S"),
                car_metric=car_metric,
                error_code=item["error_code"],
                error_msg=item["error_msg"]
            )
            result.append(err_dto)
        log.info(f"成功加载异常记录 {len(result)} 条")
        return result

    def query_by_car_id(self, car_id: str) -> List[ErrorDTO]:
        """按车辆编号筛选异常"""
        all_list = self.load_all_error()
        return [x for x in all_list if x.car_metric.car_id == car_id]

    def query_by_time_range(self, start: Optional[datetime], end: Optional[datetime]) -> List[ErrorDTO]:
        """按时间范围筛选异常；start=None代表从最早；end=None代表到最新"""
        all_list = self.load_all_error()
        res = []
        for dto in all_list:
            t = dto.occur_time
            if start is not None and t < start:
                continue
            if end is not None and t > end:
                continue
            res.append(dto)
        return res
