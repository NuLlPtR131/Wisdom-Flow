"""
用户管理模块测试用例

对应测试文档中的用例：
- TC-001: 用户注册（后台创建用户）
- TC-002: 用户登录（前台系统）
- TC-003: 错误密码登录（负向测试）
- TC-004: 权限控制测试

作者：QA Team
创建日期：2025-01-16
版本：1.0
"""

import pytest
import logging
from conftest import (
    assert_response_success,
    assert_contains_keys
)


@pytest.mark.smoke
class TestUserManagement:
    """用户管理模块测试类。"""
    
    def test_tc001_create_user_by_admin(self, management_api_client, test_data):
        """
        TC-001: 管理员在后台创建新用户
        
        测试目的：验证管理员可以成功创建新用户
        
        Args:
            management_api_client: 管理后台 API 客户端
            test_data: 测试数据生成器
        """
        logging.info("========== TC-001: 管理员创建用户 ==========")
        
        # 1. 生成测试用户数据
        user_data = test_data.generate_user_data(
            email="test_tc001@example.com",
            nickname="测试用户_TC001",
            password="Test@1234"
        )
        
        logging.info(f"测试数据: {user_data}")
        
        # 2. 发送创建用户请求
        response = management_api_client.post("/api/users", json=user_data)
        
        # 3. 断言响应状态码
        assert_response_success(response, 201, "创建用户")
        
        # 4. 断言响应数据
        response_data = response.json()
        assert_contains_keys(response_data, ["id", "email", "nickname"], "用户数据")
        assert response_data["email"] == user_data["email"], "邮箱匹配"
        assert response_data["nickname"] == user_data["nickname"], "昵称匹配"
        
        logging.info(f"用户创建成功，ID: {response_data['id']}")
        
        # 5. 验证用户列表中包含新用户
        list_response = management_api_client.get("/api/users")
        assert_response_success(list_response, 200, "获取用户列表")
        
        users = list_response.json().get("data", [])
        user_ids = [u["id"] for u in users]
        assert response_data["id"] in user_ids, "新用户出现在列表中"
        
        # 6. 清理：删除测试用户
        delete_response = management_api_client.delete(f"/api/users/{response_data['id']}")
        assert_response_success(delete_response, 200, "删除用户")
        
        logging.info("========== TC-001: 测试通过 ==========\n")
    
    def test_tc002_user_login_success(self, api_client, test_user):
        """
        TC-002: 用户登录前台系统
        
        测试目的：验证用户可以使用邮箱和密码登录
        
        Args:
            api_client: API 客户端
            test_user: 测试用户（由 fixture 自动创建和清理）
        """
        logging.info("========== TC-002: 用户登录 ==========")
        
        # 1. 准备登录数据
        login_data = {
            "email": test_user["email"],
            "password": test_user["password"]
        }
        
        logging.info(f"登录邮箱: {login_data['email']}")
        
        # 2. 发送登录请求
        response = api_client.post("/v1/user/login", json=login_data)
        
        # 3. 断言响应状态码
        assert_response_success(response, 200, "用户登录")
        
        # 4. 断言响应数据
        response_data = response.json()
        assert_contains_keys(
            response_data.get("data", {}),
            ["access_token", "user"],
            "登录响应数据"
        )
        
        # 5. 验证 Token 有效性
        access_token = response_data["data"]["access_token"]
        assert len(access_token) > 0, "Token 不为空"
        
        # 6. 验证用户信息
        user_info = response_data["data"]["user"]
        assert user_info["email"] == test_user["email"], "登录用户邮箱匹配"
        
        logging.info(f"用户登录成功，Token: {access_token[:20]}...")
        logging.info("========== TC-002: 测试通过 ==========\n")
    
    def test_tc003_user_login_wrong_password(self, api_client, test_user):
        """
        TC-003: 使用错误密码登录（负向测试）
        
        测试目的：验证系统的错误处理和安全性
        
        Args:
            api_client: API 客户端
            test_user: 测试用户
        """
        logging.info("========== TC-003: 错误密码登录 ==========")
        
        # 1. 准备错误的登录数据
        login_data = {
            "email": test_user["email"],
            "password": "WrongPassword@123"  # 错误的密码
        }
        
        logging.info(f"使用错误密码登录: {login_data['email']}")
        
        # 2. 发送登录请求
        response = api_client.post("/v1/user/login", json=login_data)
        
        # 3. 断言响应状态码（应该失败）
        assert response.status_code in [400, 401, 403], \
            f"错误密码登录应失败，实际状态码: {response.status_code}"
        
        # 4. 验证响应不包含敏感信息
        response_text = response.text.lower()
        assert "password" not in response_text or "密码" not in response_text, \
            "响应中不应包含敏感信息"
        
        # 5. 验证未生成 Token
        response_data = response.json()
        assert "access_token" not in response_data.get("data", {}), \
            "错误密码不应生成 Token"
        
        logging.info("错误密码登录被正确拒绝")
        logging.info("========== TC-003: 测试通过 ==========\n")
    
    def test_tc004_permission_control(self, authenticated_user_client, management_api_client):
        """
        TC-004: 普通用户无法访问管理后台
        
        测试目的：验证前后台权限隔离
        
        Args:
            authenticated_user_client: 已认证的普通用户客户端
            management_api_client: 管理后台 API 客户端
        """
        logging.info("========== TC-004: 权限控制测试 ==========")
        
        # 1. 获取普通用户的 Token
        user_token = authenticated_user_client.auth_token
        logging.info(f"普通用户 Token: {user_token[:20]}...")
        
        # 2. 尝试使用普通用户 Token 访问管理后台 API
        # 临时设置管理后台客户端使用普通用户 Token
        original_token = management_api_client.auth_token
        management_api_client.set_auth_token(user_token)
        
        try:
            # 3. 尝试访问管理后台用户列表
            response = management_api_client.get("/api/users")
            
            # 4. 断言响应状态码（应该被拒绝）
            assert response.status_code in [401, 403], \
                f"普通用户不应访问管理后台，实际状态码: {response.status_code}"
            
            logging.info("普通用户访问管理后台被正确拒绝")
            
            # 5. 尝试访问其他管理后台 API
            endpoints = [
                "/api/teams",
                "/api/knowledgebases",
                "/api/files",
            ]
            
            for endpoint in endpoints:
                resp = management_api_client.get(endpoint)
                assert resp.status_code in [401, 403], \
                    f"普通用户不应访问 {endpoint}，实际状态码: {resp.status_code}"
                logging.info(f"访问 {endpoint} 被拒绝 ✓")
            
        finally:
            # 6. 恢复管理后台客户端的原始 Token
            management_api_client.set_auth_token(original_token)
        
        logging.info("========== TC-004: 测试通过 ==========\n")
    
    @pytest.mark.parametrize("invalid_email", [
        "invalid-email",  # 无 @ 符号
        "@example.com",  # 缺少用户名
        "user@",  # 缺少域名
        "user @example.com",  # 包含空格
        "",  # 空字符串
    ])
    def test_create_user_invalid_email(self, management_api_client, test_data, invalid_email):
        """
        参数化测试：创建用户时使用无效邮箱
        
        测试目的：验证邮箱格式验证
        
        Args:
            management_api_client: 管理后台 API 客户端
            test_data: 测试数据生成器
            invalid_email: 无效的邮箱地址
        """
        logging.info(f"========== 测试无效邮箱: {invalid_email} ==========")
        
        # 1. 生成测试用户数据（使用无效邮箱）
        user_data = test_data.generate_user_data(email=invalid_email)
        
        # 2. 发送创建用户请求
        response = management_api_client.post("/api/users", json=user_data)
        
        # 3. 断言响应状态码（应该失败）
        assert response.status_code in [400, 422], \
            f"无效邮箱应被拒绝，实际状态码: {response.status_code}"
        
        logging.info(f"无效邮箱 {invalid_email} 被正确拒绝 ✓\n")

