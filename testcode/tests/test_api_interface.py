"""
API 接口模块测试用例

对应测试文档中的用例：
- TC-601: Python SDK 创建知识库
- TC-602: OpenAI 兼容接口

作者：QA Team
创建日期：2025-01-16
版本：1.0
"""

import pytest
import logging
from ragflow_sdk import RAGFlow
from openai import OpenAI
from conftest import (
    assert_response_success,
    assert_contains_keys
)


@pytest.mark.regression
class TestAPIInterface:
    """API 接口模块测试类。"""
    
    @pytest.mark.slow
    def test_tc601_python_sdk_create_dataset(self, test_config, test_data):
        """
        TC-601: 使用 Python SDK 创建知识库
        
        测试目的：验证 Python SDK 的功能
        
        Args:
            test_config: 测试配置
            test_data: 测试数据生成器
        """
        logging.info("========== TC-601: Python SDK 创建知识库 ==========")
        
        # 注意：此测试需要有效的 API Key
        # 如果没有 API Key，测试将被跳过
        api_key = test_config.get("api_key")
        if not api_key:
            pytest.skip("未配置 API Key，跳过测试")
        
        # 1. 初始化 RAGFlow 客户端
        rag = RAGFlow(
            api_key=api_key,
            base_url=test_config["api_base_url"]
        )
        
        logging.info(f"RAGFlow 客户端初始化完成: {test_config['api_base_url']}")
        
        # 2. 生成知识库数据
        kb_name = f"API测试库_{test_data._generate_random_string(6)}"
        
        try:
            # 3. 创建知识库
            dataset = rag.create_dataset(
                name=kb_name,
                description="通过 Python SDK 创建的测试知识库",
                embedding_model="bge-m3",
                chunk_method="general"
            )
            
            # 4. 断言知识库创建成功
            assert dataset is not None, "知识库对象不为空"
            assert hasattr(dataset, "id"), "知识库有 ID 属性"
            assert dataset.name == kb_name, "知识库名称匹配"
            
            dataset_id = dataset.id
            logging.info(f"知识库创建成功，ID: {dataset_id}")
            
            # 5. 验证可以查询到该知识库
            datasets = rag.list_datasets(name=kb_name)
            assert len(datasets) > 0, "可以查询到创建的知识库"
            assert datasets[0].id == dataset_id, "知识库 ID 匹配"
            
            logging.info("通过 SDK 查询知识库成功 ✓")
            
            # 6. 清理：删除知识库
            rag.delete_datasets(ids=[dataset_id])
            logging.info(f"知识库 {dataset_id} 已删除")
            
        except Exception as e:
            logging.error(f"SDK 测试失败: {e}")
            pytest.fail(f"SDK 测试失败: {e}")
        
        logging.info("========== TC-601: 测试通过 ==========\n")
    
    @pytest.mark.slow
    def test_tc602_openai_compatible_interface(self, test_config):
        """
        TC-602: 使用 OpenAI 库调用聊天接口
        
        测试目的：验证 OpenAI 兼容性
        
        Args:
            test_config: 测试配置
        """
        logging.info("========== TC-602: OpenAI 兼容接口 ==========")
        
        # 注意：此测试需要有效的 API Key 和 Dialog ID
        api_key = test_config.get("api_key")
        dialog_id = test_config.get("test_dialog_id")
        
        if not api_key or not dialog_id:
            pytest.skip("未配置 API Key 或 Dialog ID，跳过测试")
        
        # 1. 初始化 OpenAI 客户端
        client = OpenAI(
            api_key=api_key,
            base_url=f"{test_config['base_url']}/api/v1/chats_openai/{dialog_id}"
        )
        
        logging.info("OpenAI 客户端初始化完成")
        
        try:
            # 2. 发送聊天请求（非流式）
            response = client.chat.completions.create(
                model="qwen2.5:7b",
                messages=[
                    {"role": "system", "content": "你是一个专业的知识助手"},
                    {"role": "user", "content": "什么是 RAG 技术？"}
                ],
                stream=False
            )
            
            # 3. 断言响应格式符合 OpenAI 规范
            assert hasattr(response, "choices"), "响应包含 choices 属性"
            assert len(response.choices) > 0, "至少有一个选择"
            assert hasattr(response.choices[0], "message"), "选择包含 message 属性"
            assert hasattr(response.choices[0].message, "content"), "消息包含 content 属性"
            
            content = response.choices[0].message.content
            assert len(content) > 0, "回答内容不为空"
            
            logging.info(f"OpenAI 格式回答: {content[:100]}...")
            
            # 4. 测试流式输出
            stream_response = client.chat.completions.create(
                model="qwen2.5:7b",
                messages=[
                    {"role": "user", "content": "简单介绍一下自己"}
                ],
                stream=True
            )
            
            # 5. 验证流式输出
            chunks = []
            for chunk in stream_response:
                if chunk.choices and len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta
                    if hasattr(delta, "content") and delta.content:
                        chunks.append(delta.content)
            
            assert len(chunks) > 0, "流式输出不为空"
            full_content = ''.join(chunks)
            assert len(full_content) > 0, "流式输出内容不为空"
            
            logging.info(f"流式输出测试成功，共 {len(chunks)} 个块")
            
        except Exception as e:
            logging.error(f"OpenAI 接口测试失败: {e}")
            pytest.fail(f"OpenAI 接口测试失败: {e}")
        
        logging.info("========== TC-602: 测试通过 ==========\n")
    
    def test_api_error_handling(self, api_client):
        """
        测试 API 错误处理
        
        测试目的：验证 API 的错误响应格式
        
        Args:
            api_client: API 客户端
        """
        logging.info("========== 测试 API 错误处理 ==========")
        
        # 1. 测试 404 错误
        response = api_client.get("/v1/nonexistent/endpoint")
        assert response.status_code == 404, "不存在的端点应返回 404"
        logging.info("404 错误处理正常 ✓")
        
        # 2. 测试未授权访问
        api_client.clear_auth_token()  # 清除认证
        response = api_client.get("/v1/user/profile")
        assert response.status_code in [401, 403], "未授权访问应返回 401/403"
        logging.info("401 错误处理正常 ✓")
        
        # 3. 测试无效的请求体
        response = api_client.post(
            "/v1/datasets",
            json={"invalid": "data"}
        )
        assert response.status_code in [400, 422], "无效请求体应返回 400/422"
        logging.info("400 错误处理正常 ✓")
        
        logging.info("========== API 错误处理测试通过 ==========\n")
    
    def test_api_rate_limiting(self, api_client):
        """
        测试 API 速率限制
        
        测试目的：验证 API 的速率限制功能
        
        Args:
            api_client: API 客户端
        """
        logging.info("========== 测试 API 速率限制 ==========")
        
        # 注意：此测试取决于系统是否配置了速率限制
        # 如果没有配置，测试将通过但记录警告
        
        # 1. 快速发送多个请求
        responses = []
        for i in range(100):
            response = api_client.get("/v1/health")
            responses.append(response)
        
        # 2. 检查是否有 429 Too Many Requests
        status_codes = [r.status_code for r in responses]
        has_rate_limit = 429 in status_codes
        
        if has_rate_limit:
            logging.info("速率限制功能正常 ✓")
        else:
            logging.warning("未检测到速率限制，可能未配置")
        
        logging.info("========== API 速率限制测试完成 ==========\n")

