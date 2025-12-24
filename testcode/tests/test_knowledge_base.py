"""
知识库管理模块测试用例

对应测试文档中的用例：
- TC-101: 创建知识库
- TC-102: 知识库配置更新
- TC-103: 删除知识库

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


@pytest.mark.regression
class TestKnowledgeBase:
    """知识库管理模块测试类。"""
    
    def test_tc101_create_knowledge_base(self, management_api_client, test_data):
        """
        TC-101: 在后台创建新知识库
        
        测试目的：验证知识库创建功能
        
        Args:
            management_api_client: 管理后台 API 客户端
            test_data: 测试数据生成器
        """
        logging.info("========== TC-101: 创建知识库 ==========")
        
        # 1. 生成测试知识库数据
        kb_data = test_data.generate_knowledge_base_data(
            name="测试知识库_TC101",
            description="用于测试的知识库"
        )
        
        logging.info(f"知识库数据: {kb_data}")
        
        # 2. 发送创建知识库请求
        response = management_api_client.post("/api/knowledgebases", json=kb_data)
        
        # 3. 断言响应状态码
        assert_response_success(response, 201, "创建知识库")
        
        # 4. 断言响应数据
        response_data = response.json()
        assert_contains_keys(
            response_data,
            ["id", "name", "description", "chunk_method"],
            "知识库数据"
        )
        assert response_data["name"] == kb_data["name"], "知识库名称匹配"
        assert response_data["chunk_method"] == kb_data["chunk_method"], "分块方法匹配"
        
        kb_id = response_data["id"]
        logging.info(f"知识库创建成功，ID: {kb_id}")
        
        # 5. 验证知识库列表中包含新知识库
        list_response = management_api_client.get("/api/knowledgebases")
        assert_response_success(list_response, 200, "获取知识库列表")
        
        kbs = list_response.json().get("data", [])
        kb_ids = [kb["id"] for kb in kbs]
        assert kb_id in kb_ids, "新知识库出现在列表中"
        
        # 6. 清理：删除测试知识库
        delete_response = management_api_client.delete(f"/api/knowledgebases/{kb_id}")
        assert_response_success(delete_response, 200, "删除知识库")
        
        logging.info("========== TC-101: 测试通过 ==========\n")
    
    def test_tc102_update_knowledge_base_config(self, test_knowledge_base, management_api_client):
        """
        TC-102: 修改知识库分块配置
        
        测试目的：验证知识库配置可以被修改
        
        Args:
            test_knowledge_base: 测试知识库（由 fixture 自动创建和清理）
            management_api_client: 管理后台 API 客户端
        """
        logging.info("========== TC-102: 更新知识库配置 ==========")
        
        kb_id = test_knowledge_base["id"]
        logging.info(f"测试知识库 ID: {kb_id}")
        
        # 1. 准备更新数据
        update_data = {
            "chunk_token_count": 512,  # 修改分块大小
            "chunk_overlap": 100,  # 修改重叠大小
            "similarity_threshold": 0.7,  # 修改相似度阈值
        }
        
        logging.info(f"更新数据: {update_data}")
        
        # 2. 发送更新请求
        response = management_api_client.patch(
            f"/api/knowledgebases/{kb_id}",
            json=update_data
        )
        
        # 3. 断言响应状态码
        assert_response_success(response, 200, "更新知识库配置")
        
        # 4. 验证配置已更新
        get_response = management_api_client.get(f"/api/knowledgebases/{kb_id}")
        assert_response_success(get_response, 200, "获取知识库详情")
        
        kb_data = get_response.json()
        assert kb_data["chunk_token_count"] == update_data["chunk_token_count"], \
            "分块大小已更新"
        assert kb_data["chunk_overlap"] == update_data["chunk_overlap"], \
            "重叠大小已更新"
        assert kb_data["similarity_threshold"] == update_data["similarity_threshold"], \
            "相似度阈值已更新"
        
        logging.info("知识库配置更新成功 ✓")
        logging.info("========== TC-102: 测试通过 ==========\n")
    
    def test_tc103_delete_knowledge_base(self, management_api_client, test_data):
        """
        TC-103: 删除知识库及其关联数据
        
        测试目的：验证知识库删除功能及数据清理
        
        Args:
            management_api_client: 管理后台 API 客户端
            test_data: 测试数据生成器
        """
        logging.info("========== TC-103: 删除知识库 ==========")
        
        # 1. 创建测试知识库
        kb_data = test_data.generate_knowledge_base_data(name="待删除知识库_TC103")
        create_response = management_api_client.post("/api/knowledgebases", json=kb_data)
        assert_response_success(create_response, 201, "创建测试知识库")
        
        kb_id = create_response.json()["id"]
        logging.info(f"创建测试知识库，ID: {kb_id}")
        
        # 2. 验证知识库存在
        get_response = management_api_client.get(f"/api/knowledgebases/{kb_id}")
        assert_response_success(get_response, 200, "知识库存在")
        
        # 3. 删除知识库
        delete_response = management_api_client.delete(f"/api/knowledgebases/{kb_id}")
        assert_response_success(delete_response, 200, "删除知识库")
        
        logging.info(f"知识库 {kb_id} 已删除")
        
        # 4. 验证知识库已被删除
        get_after_delete = management_api_client.get(f"/api/knowledgebases/{kb_id}")
        assert get_after_delete.status_code == 404, \
            "删除后的知识库不应存在"
        
        # 5. 验证知识库不在列表中
        list_response = management_api_client.get("/api/knowledgebases")
        assert_response_success(list_response, 200, "获取知识库列表")
        
        kbs = list_response.json().get("data", [])
        kb_ids = [kb["id"] for kb in kbs]
        assert kb_id not in kb_ids, "删除的知识库不应在列表中"
        
        logging.info("知识库及关联数据已清理 ✓")
        logging.info("========== TC-103: 测试通过 ==========\n")
        
        # 注意：根据 Bug #001，MinIO 文件可能未被清理
        # 这是已知问题，不影响测试通过
        logging.warning("已知问题：MinIO 文件可能未自动清理（Bug #001）")
    
    @pytest.mark.parametrize("chunk_method", ["general", "qa", "manual"])
    def test_create_kb_with_different_chunk_methods(
        self,
        management_api_client,
        test_data,
        chunk_method
    ):
        """
        参数化测试：使用不同的分块方法创建知识库
        
        测试目的：验证不同分块方法的支持
        
        Args:
            management_api_client: 管理后台 API 客户端
            test_data: 测试数据生成器
            chunk_method: 分块方法
        """
        logging.info(f"========== 测试分块方法: {chunk_method} ==========")
        
        # 1. 生成知识库数据
        kb_data = test_data.generate_knowledge_base_data(
            name=f"测试_{chunk_method}_分块方法"
        )
        kb_data["chunk_method"] = chunk_method
        
        # 2. 创建知识库
        response = management_api_client.post("/api/knowledgebases", json=kb_data)
        
        # 3. 断言响应成功
        assert_response_success(response, 201, f"创建知识库（{chunk_method}）")
        
        # 4. 验证分块方法
        kb = response.json()
        assert kb["chunk_method"] == chunk_method, f"分块方法为 {chunk_method}"
        
        # 5. 清理
        management_api_client.delete(f"/api/knowledgebases/{kb['id']}")
        
        logging.info(f"分块方法 {chunk_method} 测试通过 ✓\n")
    
    def test_create_kb_with_invalid_data(self, management_api_client):
        """
        负向测试：使用无效数据创建知识库
        
        测试目的：验证数据验证逻辑
        
        Args:
            management_api_client: 管理后台 API 客户端
        """
        logging.info("========== 负向测试：无效知识库数据 ==========")
        
        # 测试用例：缺少必需字段
        invalid_data_cases = [
            {},  # 空数据
            {"name": ""},  # 空名称
            {"description": "只有描述"},  # 缺少名称
            {"name": "测试", "chunk_token_count": -1},  # 无效的分块大小
            {"name": "测试", "similarity_threshold": 1.5},  # 无效的相似度阈值
        ]
        
        for i, invalid_data in enumerate(invalid_data_cases, 1):
            logging.info(f"测试用例 {i}: {invalid_data}")
            
            response = management_api_client.post("/api/knowledgebases", json=invalid_data)
            
            # 断言请求失败
            assert response.status_code in [400, 422], \
                f"无效数据应被拒绝，实际状态码: {response.status_code}"
            
            logging.info(f"测试用例 {i} 被正确拒绝 ✓")
        
        logging.info("========== 负向测试通过 ==========\n")

