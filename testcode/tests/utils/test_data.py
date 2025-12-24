"""
测试数据生成器

提供测试所需的各种数据生成方法，包括用户、知识库、文档等。

作者：QA Team
创建日期：2025-01-16
版本：1.0
"""

import random
import string
import uuid
from datetime import datetime
from typing import Dict, Any, List


class TestData:
    """
    测试数据生成器类。
    
    提供各种测试数据的生成方法，确保数据唯一性和有效性。
    """
    
    def __init__(self):
        """初始化测试数据生成器。"""
        self.timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        self.counter = 0
    
    def _generate_unique_id(self) -> str:
        """
        生成唯一标识符。
        
        Returns:
            str: 唯一标识符
        """
        self.counter += 1
        return f"{self.timestamp}_{self.counter}_{uuid.uuid4().hex[:8]}"
    
    def _generate_random_string(self, length: int = 8) -> str:
        """
        生成随机字符串。
        
        Args:
            length: 字符串长度，默认 8
            
        Returns:
            str: 随机字符串
        """
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    def generate_email(self, prefix: str = "test") -> str:
        """
        生成测试邮箱地址。
        
        Args:
            prefix: 邮箱前缀，默认 "test"
            
        Returns:
            str: 邮箱地址
        """
        unique_id = self._generate_unique_id()
        return f"{prefix}_{unique_id}@test.wisdomflow.com"
    
    def generate_username(self, prefix: str = "user") -> str:
        """
        生成测试用户名。
        
        Args:
            prefix: 用户名前缀，默认 "user"
            
        Returns:
            str: 用户名
        """
        unique_id = self._generate_random_string(6)
        return f"{prefix}_{unique_id}"
    
    def generate_password(self, length: int = 12) -> str:
        """
        生成符合规则的密码。
        
        Args:
            length: 密码长度，默认 12
            
        Returns:
            str: 密码（包含大小写字母、数字和特殊字符）
        """
        # 确保包含各种字符类型
        password = [
            random.choice(string.ascii_uppercase),  # 大写字母
            random.choice(string.ascii_lowercase),  # 小写字母
            random.choice(string.digits),  # 数字
            random.choice("!@#$%^&*"),  # 特殊字符
        ]
        
        # 填充剩余字符
        remaining_length = length - len(password)
        all_chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password.extend(random.choices(all_chars, k=remaining_length))
        
        # 打乱顺序
        random.shuffle(password)
        
        return ''.join(password)
    
    def generate_user_data(
        self,
        email: str = None,
        nickname: str = None,
        password: str = None
    ) -> Dict[str, Any]:
        """
        生成测试用户数据。
        
        Args:
            email: 邮箱地址，不提供则自动生成
            nickname: 昵称，不提供则自动生成
            password: 密码，不提供则自动生成
            
        Returns:
            Dict[str, Any]: 用户数据字典
        """
        if email is None:
            email = self.generate_email()
        
        if nickname is None:
            nickname = self.generate_username("测试用户")
        
        if password is None:
            password = self.generate_password()
        
        return {
            "email": email,
            "nickname": nickname,
            "password": password,
            "avatar": "https://api.dicebear.com/7.x/avataaars/svg",
            "status": 1,  # 1=激活, 0=禁用
            "role": "user",  # user=普通用户, admin=管理员
        }
    
    def generate_knowledge_base_data(
        self,
        name: str = None,
        description: str = None
    ) -> Dict[str, Any]:
        """
        生成测试知识库数据。
        
        Args:
            name: 知识库名称，不提供则自动生成
            description: 知识库描述，不提供则自动生成
            
        Returns:
            Dict[str, Any]: 知识库数据字典
        """
        if name is None:
            unique_id = self._generate_random_string(6)
            name = f"测试知识库_{unique_id}"
        
        if description is None:
            description = f"自动化测试创建的知识库 - {datetime.now()}"
        
        return {
            "name": name,
            "description": description,
            "chunk_method": "general",  # general=通用, qa=问答, manual=手动
            "chunk_token_count": 256,  # 分块大小
            "chunk_overlap": 50,  # 分块重叠
            "enable_rerank": True,  # 启用重排序
            "similarity_threshold": 0.6,  # 相似度阈值
            "top_n": 8,  # 检索数量
        }
    
    def generate_document_data(
        self,
        name: str = None,
        kb_id: str = None
    ) -> Dict[str, Any]:
        """
        生成测试文档数据。
        
        Args:
            name: 文档名称，不提供则自动生成
            kb_id: 知识库 ID
            
        Returns:
            Dict[str, Any]: 文档数据字典
        """
        if name is None:
            unique_id = self._generate_random_string(6)
            name = f"测试文档_{unique_id}.pdf"
        
        return {
            "name": name,
            "kb_id": kb_id,
            "parser_method": "auto",  # auto=自动, manual=手动
            "parser_config": {
                "chunk_token_count": 256,
                "layout_recognize": True,
                "table_recognize": True,
                "image_extract": True,
            },
        }
    
    def generate_chat_assistant_data(
        self,
        name: str = None,
        dataset_ids: List[str] = None
    ) -> Dict[str, Any]:
        """
        生成测试聊天助手数据。
        
        Args:
            name: 助手名称，不提供则自动生成
            dataset_ids: 关联的知识库 ID 列表
            
        Returns:
            Dict[str, Any]: 聊天助手数据字典
        """
        if name is None:
            unique_id = self._generate_random_string(6)
            name = f"测试助手_{unique_id}"
        
        if dataset_ids is None:
            dataset_ids = []
        
        return {
            "name": name,
            "dataset_ids": dataset_ids,
            "llm": {
                "model_name": "qwen2.5:7b",
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 2048,
            },
            "prompt": {
                "system": "你是一个专业的知识助手，请基于知识库内容准确回答问题。",
                "similarity_threshold": 0.6,
                "top_n": 8,
                "enable_rerank": True,
            },
        }
    
    def generate_team_data(
        self,
        name: str = None,
        description: str = None
    ) -> Dict[str, Any]:
        """
        生成测试团队数据。
        
        Args:
            name: 团队名称，不提供则自动生成
            description: 团队描述，不提供则自动生成
            
        Returns:
            Dict[str, Any]: 团队数据字典
        """
        if name is None:
            unique_id = self._generate_random_string(6)
            name = f"测试团队_{unique_id}"
        
        if description is None:
            description = f"自动化测试创建的团队 - {datetime.now()}"
        
        return {
            "name": name,
            "description": description,
            "members": [],
        }
    
    def generate_test_question(self, topic: str = "RAG") -> str:
        """
        生成测试问题。
        
        Args:
            topic: 问题主题，默认 "RAG"
            
        Returns:
            str: 测试问题
        """
        questions = {
            "RAG": [
                "什么是 RAG 技术？",
                "RAG 技术有什么优势？",
                "RAG 的应用场景有哪些？",
                "如何优化 RAG 系统的性能？",
            ],
            "MinerU": [
                "MinerU 是什么？",
                "MinerU 支持哪些文档格式？",
                "如何使用 MinerU 解析 PDF？",
            ],
            "General": [
                "请介绍一下系统的主要功能。",
                "如何创建知识库？",
                "系统支持哪些模型？",
            ],
        }
        
        topic_questions = questions.get(topic, questions["General"])
        return random.choice(topic_questions)
    
    def generate_bulk_users(self, count: int = 10) -> List[Dict[str, Any]]:
        """
        批量生成测试用户数据。
        
        Args:
            count: 用户数量，默认 10
            
        Returns:
            List[Dict[str, Any]]: 用户数据列表
        """
        return [self.generate_user_data() for _ in range(count)]
    
    def generate_bulk_knowledge_bases(self, count: int = 5) -> List[Dict[str, Any]]:
        """
        批量生成测试知识库数据。
        
        Args:
            count: 知识库数量，默认 5
            
        Returns:
            List[Dict[str, Any]]: 知识库数据列表
        """
        return [self.generate_knowledge_base_data() for _ in range(count)]

