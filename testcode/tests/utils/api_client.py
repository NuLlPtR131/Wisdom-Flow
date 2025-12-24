"""
API 客户端工具类

封装 HTTP 请求方法，提供统一的 API 调用接口。
支持认证、重试、日志记录等功能。

作者：QA Team
创建日期：2025-01-16
版本：1.0
"""

import logging
import requests
from typing import Dict, Any, Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class APIClient:
    """
    API 客户端类，封装 HTTP 请求方法。
    
    Attributes:
        base_url (str): API 基础 URL
        timeout (int): 请求超时时间（秒）
        session (requests.Session): requests 会话对象
        auth_token (str): 认证 Token
    """
    
    def __init__(self, base_url: str, timeout: int = 30):
        """
        初始化 API 客户端。
        
        Args:
            base_url: API 基础 URL
            timeout: 请求超时时间（秒），默认 30 秒
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.auth_token: Optional[str] = None
        
        # 配置重试策略
        retry_strategy = Retry(
            total=3,  # 最大重试次数
            backoff_factor=1,  # 重试间隔
            status_forcelist=[429, 500, 502, 503, 504],  # 需要重试的状态码
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # 设置默认请求头
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Wisdom-Flow-Test-Client/1.0"
        })
        
        logging.info(f"API 客户端初始化完成: {self.base_url}")
    
    def set_auth_token(self, token: str):
        """
        设置认证 Token。
        
        Args:
            token: 认证 Token
        """
        self.auth_token = token
        self.session.headers.update({
            "Authorization": f"Bearer {token}"
        })
        logging.debug(f"设置认证 Token: {token[:20]}...")
    
    def clear_auth_token(self):
        """清除认证 Token。"""
        self.auth_token = None
        if "Authorization" in self.session.headers:
            del self.session.headers["Authorization"]
        logging.debug("清除认证 Token")
    
    def _build_url(self, endpoint: str) -> str:
        """
        构建完整的 API URL。
        
        Args:
            endpoint: API 端点
            
        Returns:
            str: 完整的 URL
        """
        endpoint = endpoint.lstrip("/")
        return f"{self.base_url}/{endpoint}"
    
    def _log_request(self, method: str, url: str, **kwargs):
        """
        记录请求日志。
        
        Args:
            method: HTTP 方法
            url: 请求 URL
            **kwargs: 其他请求参数
        """
        log_msg = f"{method} {url}"
        if "json" in kwargs:
            log_msg += f"\n请求数据: {kwargs['json']}"
        if "params" in kwargs:
            log_msg += f"\n查询参数: {kwargs['params']}"
        logging.info(log_msg)
    
    def _log_response(self, response: requests.Response):
        """
        记录响应日志。
        
        Args:
            response: HTTP 响应对象
        """
        log_msg = f"响应状态码: {response.status_code}"
        
        try:
            if response.headers.get("Content-Type", "").startswith("application/json"):
                log_msg += f"\n响应数据: {response.json()}"
            else:
                log_msg += f"\n响应内容: {response.text[:500]}"
        except Exception as e:
            log_msg += f"\n无法解析响应: {e}"
        
        if response.status_code >= 400:
            logging.error(log_msg)
        else:
            logging.info(log_msg)
    
    def request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> requests.Response:
        """
        发送 HTTP 请求（通用方法）。
        
        Args:
            method: HTTP 方法（GET, POST, PUT, DELETE 等）
            endpoint: API 端点
            **kwargs: 其他请求参数（json, params, headers 等）
            
        Returns:
            requests.Response: HTTP 响应对象
            
        Raises:
            requests.RequestException: 请求失败时抛出
        """
        url = self._build_url(endpoint)
        
        # 设置超时
        if "timeout" not in kwargs:
            kwargs["timeout"] = self.timeout
        
        # 记录请求日志
        self._log_request(method, url, **kwargs)
        
        try:
            response = self.session.request(method, url, **kwargs)
            
            # 记录响应日志
            self._log_response(response)
            
            return response
            
        except requests.RequestException as e:
            logging.error(f"请求失败: {method} {url} - {e}")
            raise
    
    def get(self, endpoint: str, **kwargs) -> requests.Response:
        """
        发送 GET 请求。
        
        Args:
            endpoint: API 端点
            **kwargs: 其他请求参数
            
        Returns:
            requests.Response: HTTP 响应对象
        """
        return self.request("GET", endpoint, **kwargs)
    
    def post(self, endpoint: str, **kwargs) -> requests.Response:
        """
        发送 POST 请求。
        
        Args:
            endpoint: API 端点
            **kwargs: 其他请求参数
            
        Returns:
            requests.Response: HTTP 响应对象
        """
        return self.request("POST", endpoint, **kwargs)
    
    def put(self, endpoint: str, **kwargs) -> requests.Response:
        """
        发送 PUT 请求。
        
        Args:
            endpoint: API 端点
            **kwargs: 其他请求参数
            
        Returns:
            requests.Response: HTTP 响应对象
        """
        return self.request("PUT", endpoint, **kwargs)
    
    def patch(self, endpoint: str, **kwargs) -> requests.Response:
        """
        发送 PATCH 请求。
        
        Args:
            endpoint: API 端点
            **kwargs: 其他请求参数
            
        Returns:
            requests.Response: HTTP 响应对象
        """
        return self.request("PATCH", endpoint, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """
        发送 DELETE 请求。
        
        Args:
            endpoint: API 端点
            **kwargs: 其他请求参数
            
        Returns:
            requests.Response: HTTP 响应对象
        """
        return self.request("DELETE", endpoint, **kwargs)
    
    def upload_file(
        self,
        endpoint: str,
        file_path: str,
        field_name: str = "file",
        additional_data: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        """
        上传文件。
        
        Args:
            endpoint: API 端点
            file_path: 文件路径
            field_name: 表单字段名，默认为 "file"
            additional_data: 附加表单数据
            
        Returns:
            requests.Response: HTTP 响应对象
        """
        url = self._build_url(endpoint)
        
        with open(file_path, "rb") as f:
            files = {field_name: f}
            data = additional_data or {}
            
            logging.info(f"上传文件: {file_path} -> {url}")
            
            response = self.session.post(
                url,
                files=files,
                data=data,
                timeout=self.timeout * 3  # 文件上传超时时间延长
            )
            
            self._log_response(response)
            
            return response
    
    def close(self):
        """关闭会话，释放资源。"""
        self.session.close()
        logging.info("API 客户端会话已关闭")
    
    def __enter__(self):
        """上下文管理器入口。"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器退出，自动关闭会话。"""
        self.close()

