"""
Wisdom-Flow 测试配置文件

本模块包含 pytest 的全局配置、fixture 和测试工具函数。
为所有测试用例提供统一的测试环境配置和公共资源。

作者：QA Team
创建日期：2025-01-16
版本：1.0
"""

import os
import sys
import time
import pytest
import logging
from typing import Generator, Dict, Any
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 导入测试工具
from tests.utils.api_client import APIClient
from tests.utils.test_data import TestData
from tests.utils.logger import setup_test_logger


# ============================================================================
# 全局配置
# ============================================================================

# 测试环境配置
TEST_CONFIG = {
    "base_url": os.getenv("TEST_BASE_URL", "http://localhost"),
    "api_base_url": os.getenv("TEST_API_BASE_URL", "http://localhost:9380"),
    "management_url": os.getenv("TEST_MANAGEMENT_URL", "http://localhost:8888"),
    "management_api_url": os.getenv("TEST_MANAGEMENT_API_URL", "http://localhost:5000"),
    "admin_username": os.getenv("MANAGEMENT_ADMIN_USERNAME", "admin"),
    "admin_password": os.getenv("MANAGEMENT_ADMIN_PASSWORD", "12345678"),
    "timeout": int(os.getenv("TEST_TIMEOUT", "30")),
    "retry_count": int(os.getenv("TEST_RETRY_COUNT", "3")),
}


# ============================================================================
# Pytest Hooks
# ============================================================================

def pytest_configure(config):
    """
    Pytest 配置钩子，在测试会话开始前执行。
    
    Args:
        config: pytest 配置对象
    """
    # 设置测试日志
    setup_test_logger()
    
    # 添加自定义标记
    config.addinivalue_line(
        "markers", "smoke: 冒烟测试，验证核心功能"
    )
    config.addinivalue_line(
        "markers", "regression: 回归测试，验证已有功能"
    )
    config.addinivalue_line(
        "markers", "performance: 性能测试"
    )
    config.addinivalue_line(
        "markers", "security: 安全测试"
    )
    config.addinivalue_line(
        "markers", "slow: 运行时间较长的测试"
    )
    
    logging.info("=" * 80)
    logging.info("Wisdom-Flow 自动化测试开始")
    logging.info(f"测试环境: {TEST_CONFIG['base_url']}")
    logging.info("=" * 80)


def pytest_unconfigure(config):
    """
    Pytest 清理钩子，在测试会话结束后执行。
    
    Args:
        config: pytest 配置对象
    """
    logging.info("=" * 80)
    logging.info("Wisdom-Flow 自动化测试结束")
    logging.info("=" * 80)


# ============================================================================
# Session 级别 Fixtures（整个测试会话共享）
# ============================================================================

@pytest.fixture(scope="session")
def test_config() -> Dict[str, Any]:
    """
    提供测试配置信息。
    
    Returns:
        Dict[str, Any]: 测试配置字典
    """
    return TEST_CONFIG


@pytest.fixture(scope="session")
def test_data() -> TestData:
    """
    提供测试数据管理器。
    
    Returns:
        TestData: 测试数据管理器实例
    """
    return TestData()


# ============================================================================
# Module 级别 Fixtures（每个测试模块共享）
# ============================================================================

@pytest.fixture(scope="module")
def api_client(test_config) -> Generator[APIClient, None, None]:
    """
    提供 API 客户端实例，用于测试 API 接口。
    
    Args:
        test_config: 测试配置
        
    Yields:
        APIClient: API 客户端实例
    """
    client = APIClient(
        base_url=test_config["api_base_url"],
        timeout=test_config["timeout"]
    )
    
    yield client
    
    # 清理资源
    client.close()


@pytest.fixture(scope="module")
def management_api_client(test_config) -> Generator[APIClient, None, None]:
    """
    提供管理后台 API 客户端实例。
    
    Args:
        test_config: 测试配置
        
    Yields:
        APIClient: 管理后台 API 客户端实例
    """
    client = APIClient(
        base_url=test_config["management_api_url"],
        timeout=test_config["timeout"]
    )
    
    # 登录管理后台获取 token
    login_response = client.post("/api/auth/login", json={
        "username": test_config["admin_username"],
        "password": test_config["admin_password"]
    })
    
    if login_response.status_code == 200:
        token = login_response.json().get("token")
        client.set_auth_token(token)
        logging.info("管理后台登录成功")
    else:
        logging.error(f"管理后台登录失败: {login_response.text}")
    
    yield client
    
    # 清理资源
    client.close()


# ============================================================================
# Function 级别 Fixtures（每个测试函数独立）
# ============================================================================

@pytest.fixture(scope="function")
def test_user(management_api_client, test_data) -> Generator[Dict[str, Any], None, None]:
    """
    创建测试用户，测试结束后自动清理。
    
    Args:
        management_api_client: 管理后台 API 客户端
        test_data: 测试数据管理器
        
    Yields:
        Dict[str, Any]: 测试用户信息
    """
    # 生成测试用户数据
    user_data = test_data.generate_user_data()
    
    # 创建用户
    response = management_api_client.post("/api/users", json=user_data)
    
    if response.status_code == 201:
        user = response.json()
        logging.info(f"创建测试用户成功: {user['email']}")
        
        yield user
        
        # 清理：删除测试用户
        try:
            delete_response = management_api_client.delete(f"/api/users/{user['id']}")
            if delete_response.status_code == 200:
                logging.info(f"删除测试用户成功: {user['email']}")
        except Exception as e:
            logging.warning(f"删除测试用户失败: {e}")
    else:
        logging.error(f"创建测试用户失败: {response.text}")
        pytest.fail(f"创建测试用户失败: {response.text}")


@pytest.fixture(scope="function")
def test_knowledge_base(management_api_client, test_data) -> Generator[Dict[str, Any], None, None]:
    """
    创建测试知识库，测试结束后自动清理。
    
    Args:
        management_api_client: 管理后台 API 客户端
        test_data: 测试数据管理器
        
    Yields:
        Dict[str, Any]: 测试知识库信息
    """
    # 生成测试知识库数据
    kb_data = test_data.generate_knowledge_base_data()
    
    # 创建知识库
    response = management_api_client.post("/api/knowledgebases", json=kb_data)
    
    if response.status_code == 201:
        kb = response.json()
        logging.info(f"创建测试知识库成功: {kb['name']}")
        
        yield kb
        
        # 清理：删除测试知识库
        try:
            delete_response = management_api_client.delete(f"/api/knowledgebases/{kb['id']}")
            if delete_response.status_code == 200:
                logging.info(f"删除测试知识库成功: {kb['name']}")
        except Exception as e:
            logging.warning(f"删除测试知识库失败: {e}")
    else:
        logging.error(f"创建测试知识库失败: {response.text}")
        pytest.fail(f"创建测试知识库失败: {response.text}")


@pytest.fixture(scope="function")
def authenticated_user_client(api_client, test_user, test_config) -> Generator[APIClient, None, None]:
    """
    提供已认证的用户 API 客户端。
    
    Args:
        api_client: API 客户端
        test_user: 测试用户
        test_config: 测试配置
        
    Yields:
        APIClient: 已认证的 API 客户端
    """
    # 用户登录
    login_response = api_client.post("/v1/user/login", json={
        "email": test_user["email"],
        "password": test_user["password"]
    })
    
    if login_response.status_code == 200:
        token = login_response.json().get("data", {}).get("access_token")
        api_client.set_auth_token(token)
        logging.info(f"用户 {test_user['email']} 登录成功")
        
        yield api_client
    else:
        logging.error(f"用户登录失败: {login_response.text}")
        pytest.fail(f"用户登录失败: {login_response.text}")


# ============================================================================
# 测试辅助 Fixtures
# ============================================================================

@pytest.fixture(scope="function")
def wait_for_processing():
    """
    等待异步处理完成的辅助函数。
    
    Returns:
        Callable: 等待函数
    """
    def _wait(seconds: int = 5, message: str = "等待处理完成"):
        """
        等待指定秒数。
        
        Args:
            seconds: 等待秒数
            message: 等待信息
        """
        logging.info(f"{message}，等待 {seconds} 秒...")
        time.sleep(seconds)
    
    return _wait


@pytest.fixture(scope="function")
def retry_on_failure():
    """
    失败重试装饰器。
    
    Returns:
        Callable: 重试装饰器函数
    """
    def _retry(func, max_attempts: int = 3, delay: int = 2):
        """
        重试执行函数。
        
        Args:
            func: 要执行的函数
            max_attempts: 最大重试次数
            delay: 重试间隔（秒）
            
        Returns:
            函数执行结果
        """
        for attempt in range(1, max_attempts + 1):
            try:
                return func()
            except Exception as e:
                if attempt == max_attempts:
                    logging.error(f"重试 {max_attempts} 次后仍然失败: {e}")
                    raise
                logging.warning(f"第 {attempt} 次尝试失败，{delay} 秒后重试: {e}")
                time.sleep(delay)
    
    return _retry


# ============================================================================
# 性能测试 Fixtures
# ============================================================================

@pytest.fixture(scope="function")
def performance_monitor():
    """
    性能监控器，记录测试执行时间。
    
    Yields:
        Dict: 性能数据字典
    """
    perf_data = {
        "start_time": None,
        "end_time": None,
        "duration": None
    }
    
    perf_data["start_time"] = time.time()
    
    yield perf_data
    
    perf_data["end_time"] = time.time()
    perf_data["duration"] = perf_data["end_time"] - perf_data["start_time"]
    
    logging.info(f"测试执行时间: {perf_data['duration']:.2f} 秒")


# ============================================================================
# 断言辅助函数
# ============================================================================

def assert_response_success(response, expected_status: int = 200, message: str = ""):
    """
    断言 HTTP 响应成功。
    
    Args:
        response: HTTP 响应对象
        expected_status: 期望的状态码
        message: 自定义错误消息
    """
    actual_status = response.status_code
    
    if message:
        error_msg = f"{message}: 期望状态码 {expected_status}，实际 {actual_status}"
    else:
        error_msg = f"期望状态码 {expected_status}，实际 {actual_status}"
    
    if actual_status != expected_status:
        logging.error(f"{error_msg}\n响应内容: {response.text}")
    
    assert actual_status == expected_status, error_msg


def assert_contains_keys(data: dict, required_keys: list, message: str = ""):
    """
    断言字典包含指定的键。
    
    Args:
        data: 要检查的字典
        required_keys: 必需的键列表
        message: 自定义错误消息
    """
    missing_keys = [key for key in required_keys if key not in data]
    
    if missing_keys:
        error_msg = f"{message}: 缺少必需的键: {missing_keys}" if message else f"缺少必需的键: {missing_keys}"
        logging.error(f"{error_msg}\n实际数据: {data}")
        pytest.fail(error_msg)


# ============================================================================
# 导出公共函数供测试用例使用
# ============================================================================

__all__ = [
    "TEST_CONFIG",
    "test_config",
    "test_data",
    "api_client",
    "management_api_client",
    "test_user",
    "test_knowledge_base",
    "authenticated_user_client",
    "wait_for_processing",
    "retry_on_failure",
    "performance_monitor",
    "assert_response_success",
    "assert_contains_keys",
]

