from typing import List
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
import os
from dto.error_dto import ErrorDTO
from utils.log_util import log


class ExcelExportService:
    """将ErrorDTO异常列表导出为Excel，不改动原有json存储逻辑"""

    def __init__(self):
        self.export_file_name = "abnormal_export.xlsx"

    def export_error_list(self, error_list: List[ErrorDTO], filename: str = None) -> bool:
        """
        导出异常DTO列表到excel
        :param error_list: ErrorDTO对象列表
        :param filename: 可选，自定义输出文件名
        :return: True成功 / False失败
        """
        if not error_list:
            log.warn("待导出的异常数据为空，跳过导出")
            return False

        out_file = filename if filename else self.export_file_name

        try:
            wb = Workbook()
            ws = wb.active
            ws.title = "异常车辆数据"

            # 表头
            headers = [
                "异常ID",
                "异常发生时间",
                "车辆编号",
                "车速(km/h)",
                "电机温度",
                "电池电压",
                "总里程",
                "错误码",
                "错误描述"
            ]
            ws.append(headers)

            # 设置表头样式
            header_font = Font(bold=True)
            for col in range(1, len(headers) + 1):
                cell = ws.cell(row=1, column=col)
                cell.font = header_font
                cell.alignment = Alignment(horizontal="center")

            # 写入每一行数据
            for err_dto in error_list:
                row_data = [
                    err_dto.error_id,
                    err_dto.occur_time.strftime("%Y-%m-%d %H:%M:%S"),
                    err_dto.car_metric.car_id,
                    err_dto.car_metric.speed,
                    err_dto.car_metric.temperature,
                    err_dto.car_metric.voltage,
                    err_dto.car_metric.mileage,
                    err_dto.error_code,
                    err_dto.error_msg
                ]
                ws.append(row_data)

            # 简单列宽
            ws.column_dimensions["A"].width = 36
            ws.column_dimensions["B"].width = 20
            ws.column_dimensions["I"].width = 30

            wb.save(out_file)
            log.info(f"Excel导出成功，文件:{os.path.abspath(out_file)}")
            return True

        except Exception as e:
            log.error(f"Excel导出发生异常：{str(e)}")
            return False
