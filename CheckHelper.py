from datetime import datetime


class CheckHelper:
    def __init__(self):
        pass

    @staticmethod
    def get_time_now():
        return datetime.now()

    @staticmethod
    def get_date_from_str(str):
        return datetime.strptime(str, "%Y-%m-%d")

    @staticmethod
    def check_true_date(str):
        return True if CheckHelper.get_time_now() >= CheckHelper.get_date_from_str(str) else False
