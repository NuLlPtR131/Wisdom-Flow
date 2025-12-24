"""
测试辅助函数模块

提供各种辅助函数和工具方法，简化测试代码编写。

作者：QA Team
创建日期：2025-01-16
版本：1.0
"""

import time
import logging
from typing import Callable, Any, Dict, List
from functools import wraps


def retry_on_exception(
    max_attempts: int = 3,
    delay: int = 2,
    exceptions: tuple = (Exception,)
):
    """
    失败重试装饰器。
    
    Args:
        max_attempts: 最大重试次数
        delay: 重试间隔（秒）
        exceptions: 需要重试的异常类型
        
    Returns:
        Callable: 装饰器函数
        
    Example:
        @retry_on_exception(max_attempts=3, delay=1)
        def unstable_function():
            # 可能失败的操作
            pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt == max_attempts:
                        logging.error(
                            f"{func.__name__} 重试 {max_attempts} 次后仍然失败: {e}"
                        )
                        raise
                    
                    logging.warning(
                        f"{func.__name__} 第 {attempt} 次尝试失败，"
                        f"{delay} 秒后重试: {e}"
                    )
                    time.sleep(delay)
            
            if last_exception:
                raise last_exception
        
        return wrapper
    return decorator


def measure_time(func: Callable) -> Callable:
    """
    测量函数执行时间的装饰器。
    
    Args:
        func: 要测量的函数
        
    Returns:
        Callable: 装饰后的函数
        
    Example:
        @measure_time
        def slow_function():
            time.sleep(1)
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        
        logging.info(f"{func.__name__} 执行时间: {elapsed_time:.2f} 秒")
        
        return result
    
    return wrapper


def wait_until(
    condition: Callable[[], bool],
    timeout: int = 30,
    interval: int = 1,
    error_message: str = "等待条件超时"
) -> bool:
    """
    等待直到条件满足或超时。
    
    Args:
        condition: 条件函数，返回 bool
        timeout: 超时时间（秒）
        interval: 检查间隔（秒）
        error_message: 超时错误消息
        
    Returns:
        bool: 条件是否满足
        
    Raises:
        TimeoutError: 超时时抛出
        
    Example:
        wait_until(
            lambda: api_client.get("/status").json()["ready"],
            timeout=60,
            error_message="服务未就绪"
        )
    """
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            if condition():
                return True
        except Exception as e:
            logging.debug(f"条件检查异常: {e}")
        
        time.sleep(interval)
    
    raise TimeoutError(f"{error_message}（超时 {timeout} 秒）")


def poll_until_status(
    get_status_func: Callable[[], str],
    expected_status: str,
    timeout: int = 60,
    interval: int = 5
) -> bool:
    """
    轮询直到状态达到预期值。
    
    Args:
        get_status_func: 获取状态的函数
        expected_status: 期望的状态
        timeout: 超时时间（秒）
        interval: 轮询间隔（秒）
        
    Returns:
        bool: 是否达到预期状态
        
    Example:
        poll_until_status(
            lambda: client.get(f"/tasks/{task_id}").json()["status"],
            "completed",
            timeout=120
        )
    """
    logging.info(f"开始轮询状态，期望: {expected_status}，超时: {timeout}秒")
    
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            current_status = get_status_func()
            logging.debug(f"当前状态: {current_status}")
            
            if current_status == expected_status:
                logging.info(f"状态已达到预期: {expected_status}")
                return True
            
            if current_status == "failed":
                logging.error("任务失败")
                return False
                
        except Exception as e:
            logging.warning(f"获取状态异常: {e}")
        
        time.sleep(interval)
    
    logging.error(f"状态轮询超时（{timeout}秒）")
    return False


def compare_dicts(
    actual: Dict[str, Any],
    expected: Dict[str, Any],
    ignore_keys: List[str] = None
) -> tuple:
    """
    比较两个字典，返回差异。
    
    Args:
        actual: 实际数据
        expected: 期望数据
        ignore_keys: 要忽略的键列表
        
    Returns:
        tuple: (是否相同, 差异列表)
        
    Example:
        is_same, diffs = compare_dicts(
            actual={"name": "test", "age": 30},
            expected={"name": "test", "age": 25},
            ignore_keys=["id"]
        )
    """
    ignore_keys = ignore_keys or []
    differences = []
    
    # 检查期望的键
    for key, expected_value in expected.items():
        if key in ignore_keys:
            continue
        
        if key not in actual:
            differences.append(f"缺少键: {key}")
        elif actual[key] != expected_value:
            differences.append(
                f"键 {key} 不匹配: 期望 {expected_value}, 实际 {actual[key]}"
            )
    
    # 检查实际数据中的额外键
    for key in actual.keys():
        if key not in expected and key not in ignore_keys:
            differences.append(f"额外的键: {key}")
    
    is_same = len(differences) == 0
    
    if not is_same:
        logging.debug(f"字典差异: {differences}")
    
    return is_same, differences


def sanitize_filename(filename: str) -> str:
    """
    清理文件名，移除非法字符。
    
    Args:
        filename: 原始文件名
        
    Returns:
        str: 清理后的文件名
        
    Example:
        clean_name = sanitize_filename("test/file:name?.txt")
        # 返回: "test_file_name_.txt"
    """
    import re
    
    # 移除非法字符
    clean = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # 移除控制字符
    clean = ''.join(char for char in clean if ord(char) >= 32)
    
    # 限制长度
    if len(clean) > 255:
        name, ext = clean.rsplit('.', 1) if '.' in clean else (clean, '')
        clean = f"{name[:250]}.{ext}" if ext else name[:255]
    
    return clean


def format_bytes(bytes_size: int) -> str:
    """
    格式化字节大小为人类可读格式。
    
    Args:
        bytes_size: 字节数
        
    Returns:
        str: 格式化后的大小
        
    Example:
        format_bytes(1536) # 返回 "1.50 KB"
        format_bytes(1048576) # 返回 "1.00 MB"
    """
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    size = float(bytes_size)
    unit_index = 0
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    return f"{size:.2f} {units[unit_index]}"


def format_duration(seconds: float) -> str:
    """
    格式化时长为人类可读格式。
    
    Args:
        seconds: 秒数
        
    Returns:
        str: 格式化后的时长
        
    Example:
        format_duration(3665) # 返回 "1小时 1分钟 5秒"
    """
    if seconds < 60:
        return f"{seconds:.2f}秒"
    
    minutes, seconds = divmod(seconds, 60)
    
    if minutes < 60:
        return f"{int(minutes)}分钟 {int(seconds)}秒"
    
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours)}小时 {int(minutes)}分钟 {int(seconds)}秒"


def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    截断字符串到指定长度。
    
    Args:
        text: 原始字符串
        max_length: 最大长度
        suffix: 后缀
        
    Returns:
        str: 截断后的字符串
        
    Example:
        truncate_string("很长的文本内容...", 10) # 返回 "很长的文本内容..."
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def extract_error_message(response: Any) -> str:
    """
    从 HTTP 响应中提取错误消息。
    
    Args:
        response: HTTP 响应对象
        
    Returns:
        str: 错误消息
        
    Example:
        error_msg = extract_error_message(response)
    """
    try:
        if hasattr(response, 'json'):
            data = response.json()
            
            # 常见的错误字段
            for key in ['error', 'message', 'msg', 'detail', 'error_message']:
                if key in data:
                    return str(data[key])
            
            return str(data)
        
        return response.text if hasattr(response, 'text') else str(response)
        
    except Exception:
        return "无法提取错误消息"


def is_valid_uuid(uuid_string: str) -> bool:
    """
    验证字符串是否为有效的 UUID。
    
    Args:
        uuid_string: 要验证的字符串
        
    Returns:
        bool: 是否为有效的 UUID
        
    Example:
        is_valid_uuid("550e8400-e29b-41d4-a716-446655440000") # True
    """
    import uuid
    
    try:
        uuid.UUID(uuid_string)
        return True
    except (ValueError, AttributeError):
        return False


def deep_merge(dict1: Dict, dict2: Dict) -> Dict:
    """
    深度合并两个字典。
    
    Args:
        dict1: 第一个字典
        dict2: 第二个字典（优先级更高）
        
    Returns:
        Dict: 合并后的字典
        
    Example:
        result = deep_merge(
            {"a": 1, "b": {"c": 2}},
            {"b": {"d": 3}, "e": 4}
        )
        # 返回: {"a": 1, "b": {"c": 2, "d": 3}, "e": 4}
    """
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    
    return result

