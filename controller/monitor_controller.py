from datetime import datetime

from form.monitor_main_form import MonitorMainForm
from service.car_data_service import CarDataService
from service.excel_export_service import ExcelExportService
from service.error_query_service import ErrorQueryService
from utils.log_util import log

class MonitorController:
    def __init__(self, root):
        self.ui_form = MonitorMainForm(root)
        self.data_service = CarDataService()
        self.root = root
        self.interval_ms = 800  # 每隔800毫秒生成一条模拟车辆数据
        # 实例化导出服务
        self.excel_export_service = ExcelExportService()
        self.error_query_service = ErrorQueryService()

        # 将导出业务回调注入UI层，解耦form与service
        # 记录上一次导出时间：None=还没有执行过导出
        self.last_export_time: datetime | None = None

        # 将导出业务回调注入UI层，解耦form与service
        self.ui_form.export_all_callback = self.handle_export_all_abnormal
        self.ui_form.export_increment_callback = self.handle_export_increment
        self.ui_form.export_by_time_callback = self.handle_export_by_time_range
        log.info("汽车监控控制器初始化完成")  # 使用新日志

    def handle_export_all_abnormal(self) -> bool:
        """按钮回调：读取全部异常并导出Excel"""
        err_list = self.error_query_service.load_all_error()
        ok = self.excel_export_service.export_error_list(err_list)
        if ok:
            self.last_export_time = datetime.now()
        return ok

    def handle_export_increment(self) -> bool:
        all_err = self.error_query_service.load_all_error()
        if self.last_export_time is None:
            log.info("尚未执行过导出，执行全量导出作为第一次增量")
            ok = self.excel_export_service.export_error_list(all_err, filename="abnormal_increment.xlsx")
        else:
            inc_list = [dto for dto in all_err if dto.occur_time > self.last_export_time]
            if not inc_list:
                return False
            ok = self.excel_export_service.export_error_list(inc_list, filename="abnormal_increment.xlsx")
        if ok:
            self.last_export_time = datetime.now()
        return ok

    def handle_export_by_time_range(self, start_dt: datetime, end_dt: datetime) -> bool:
        """直接接收已经解析好的datetime对象，不再解析字符串"""
        range_list = self.error_query_service.query_by_time_range(start_dt, end_dt)
        if not range_list:
            return False
        return self.excel_export_service.export_error_list(range_list, filename="abnormal_timerange.xlsx")

    def loop_fetch_data(self):
        """定时循环：生成数据 ->业务处理 ->追加到窗体表格"""
        car_dto = self.data_service.generate_mock_car_data()
        handled_dto = self.data_service.filter_and_handle_data(car_dto)
        self.ui_form.append_one_row(handled_dto)
        # 继续下一次定时任务
        self.root.after(self.interval_ms, self.loop_fetch_data)

    def start(self):
        self.loop_fetch_data()
        log.info("监控循环已启动")
