import json
import os
from dto.error_dto import ErrorDTO

class ReportService:
    """异常数据持久化、模拟上报服务，操作ErrorDTO"""
    def __init__(self):
        self.save_file = "abnormal_car_data.json"

    def save_abnormal_data(self, error_dto: ErrorDTO):
        """保存ErrorDTO异常对象到本地json"""
        data_list = []
        if os.path.exists(self.save_file):
            with open(self.save_file, "r", encoding="utf-8") as f:
                try:
                    data_list = json.load(f)
                except json.JSONDecodeError:
                    data_list = []
        # 调用dto方法转可序列化字典
        data_list.append(error_dto.to_json_dict())
        with open(self.save_file, "w", encoding="utf-8") as f:
            json.dump(data_list, f, ensure_ascii=False, indent=2)

    def mock_report(self, error_dto: ErrorDTO):
        """模拟http上报，入参ErrorDTO"""
        print(f"【模拟上报异常】异常ID:{error_dto.error_id} 车辆:{error_dto.car_metric.car_id} "
              f"错误码:{error_dto.error_code} 说明:{error_dto.error_msg}")
