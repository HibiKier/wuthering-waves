from pydantic import BaseModel


class CodeModel(BaseModel):
    id: str
    """id"""
    order: str
    """兑换码"""
    reward: str
    """奖励"""
    label: str
    """标签"""
    type: str
    """类型"""
    is_fail: str = "0"
    """是否失败"""
    is_update: str
    """是否更新"""
    qufu: str
    """区服"""
    author: str
    """作者"""
    create_time: str
    """创建时间"""
    begin_time: str
    """开始时间"""
    over_time: str
    """结束时间"""
    is_cur_month: str
    """是否当前月份"""
