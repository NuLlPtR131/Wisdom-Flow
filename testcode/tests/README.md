# Wisdom-Flow 自动化测试

## 📋 简介

本目录包含 Wisdom-Flow 系统的自动化测试代码，基于 Wisdom-Flow 测试文档编写，覆盖功能测试、性能测试、兼容性测试和安全测试。

## 🗂️ 目录结构

```
tests/
├── conftest.py                    # Pytest 配置和公共 fixtures
├── pytest.ini                     # Pytest 配置文件
├── requirements.txt               # 测试依赖包
├── README.md                      # 本文件
├── utils/                         # 测试工具模块
│   ├── __init__.py
│   ├── api_client.py             # API 客户端封装
│   ├── test_data.py              # 测试数据生成器
│   └── logger.py                 # 日志配置
├── test_user_management.py       # 用户管理测试
├── test_knowledge_base.py        # 知识库管理测试
├── test_api_interface.py         # API 接口测试
├── test_performance.py           # 性能测试
└── test_logs/                    # 测试日志目录（自动生成）
```

## 🚀 快速开始

### 1. 安装依赖

```bash
# 进入测试目录
cd tests

# 安装测试依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件（可选）：

```bash
# 测试环境配置
TEST_BASE_URL=http://localhost
TEST_API_BASE_URL=http://localhost:9380
TEST_MANAGEMENT_URL=http://localhost:8888
TEST_MANAGEMENT_API_URL=http://localhost:5000

# 管理员账号
MANAGEMENT_ADMIN_USERNAME=admin
MANAGEMENT_ADMIN_PASSWORD=12345678

# 测试配置
TEST_TIMEOUT=30
TEST_RETRY_COUNT=3
```

### 3. 运行测试

#### 运行所有测试

```bash
pytest
```

#### 运行特定测试模块

```bash
# 用户管理测试
pytest test_user_management.py

# 知识库管理测试
pytest test_knowledge_base.py

# API 接口测试
pytest test_api_interface.py
```

#### 按标记运行测试

```bash
# 冒烟测试
pytest -m smoke

# 回归测试
pytest -m regression

# 性能测试
pytest -m performance

# 排除慢速测试
pytest -m "not slow"
```

#### 并行测试

```bash
# 使用 4 个进程并行执行
pytest -n 4
```

#### 生成测试报告

```bash
# HTML 报告
pytest --html=reports/test_report.html --self-contained-html

# 覆盖率报告
pytest --cov=tests --cov-report=html
```

## 📝 测试用例对照表

| 测试文件 | 测试用例 | 文档编号 | 说明 |
|---------|---------|---------|------|
| `test_user_management.py` | `test_tc001_create_user_by_admin` | TC-001 | 管理员创建用户 |
| `test_user_management.py` | `test_tc002_user_login_success` | TC-002 | 用户登录 |
| `test_user_management.py` | `test_tc003_user_login_wrong_password` | TC-003 | 错误密码登录 |
| `test_user_management.py` | `test_tc004_permission_control` | TC-004 | 权限控制测试 |
| `test_knowledge_base.py` | `test_tc101_create_knowledge_base` | TC-101 | 创建知识库 |
| `test_knowledge_base.py` | `test_tc102_update_knowledge_base_config` | TC-102 | 更新知识库配置 |
| `test_knowledge_base.py` | `test_tc103_delete_knowledge_base` | TC-103 | 删除知识库 |
| `test_api_interface.py` | `test_tc601_python_sdk_create_dataset` | TC-601 | Python SDK 测试 |
| `test_api_interface.py` | `test_tc602_openai_compatible_interface` | TC-602 | OpenAI 兼容性测试 |
| `test_performance.py` | `test_tc701_concurrent_users` | TC-701 | 并发用户测试 |
| `test_performance.py` | `test_tc702_document_parsing_performance` | TC-702 | 文档解析性能 |
| `test_performance.py` | `test_tc703_memory_stability` | TC-703 | 内存稳定性测试 |

## 🔧 工具类说明

### APIClient

API 客户端封装类，提供统一的 HTTP 请求接口。

```python
from tests.utils.api_client import APIClient

# 创建客户端
client = APIClient(base_url="http://localhost:9380", timeout=30)

# 设置认证 Token
client.set_auth_token("your-token")

# 发送请求
response = client.get("/v1/user/profile")
response = client.post("/v1/datasets", json={"name": "test"})

# 上传文件
response = client.upload_file(
    "/v1/files/upload",
    "document.pdf",
    field_name="file"
)
```

### TestData

测试数据生成器，提供各种测试数据生成方法。

```python
from tests.utils.test_data import TestData

# 创建生成器
test_data = TestData()

# 生成用户数据
user = test_data.generate_user_data()

# 生成知识库数据
kb = test_data.generate_knowledge_base_data()

# 生成测试问题
question = test_data.generate_test_question(topic="RAG")
```

## 📊 Fixtures 说明

### 全局 Fixtures

- `test_config`: 测试配置字典
- `test_data`: 测试数据生成器
- `api_client`: API 客户端（前台）
- `management_api_client`: 管理后台 API 客户端

### 测试资源 Fixtures

- `test_user`: 自动创建和清理的测试用户
- `test_knowledge_base`: 自动创建和清理的测试知识库
- `authenticated_user_client`: 已认证的用户客户端

### 辅助 Fixtures

- `wait_for_processing`: 等待异步处理完成
- `retry_on_failure`: 失败重试装饰器
- `performance_monitor`: 性能监控器

## 🎯 测试最佳实践

### 1. 测试命名规范

```python
# 测试类命名：Test + 模块名
class TestUserManagement:
    pass

# 测试方法命名：test_ + 用例编号 + 描述
def test_tc001_create_user_by_admin(self):
    pass
```

### 2. 使用注释说明

```python
def test_tc001_create_user_by_admin(self, management_api_client, test_data):
    """
    TC-001: 管理员在后台创建新用户
    
    测试目的：验证管理员可以成功创建新用户
    
    Args:
        management_api_client: 管理后台 API 客户端
        test_data: 测试数据生成器
    """
    # 测试代码
    pass
```

### 3. 使用标记分类

```python
@pytest.mark.smoke  # 冒烟测试
@pytest.mark.regression  # 回归测试
@pytest.mark.slow  # 慢速测试
@pytest.mark.performance  # 性能测试
def test_example(self):
    pass
```

### 4. 资源自动清理

```python
def test_with_cleanup(self, test_user):
    # test_user 由 fixture 自动创建
    # 测试结束后自动清理
    pass
```

### 5. 使用断言辅助函数

```python
from conftest import assert_response_success, assert_contains_keys

# 断言响应成功
assert_response_success(response, 200, "创建用户")

# 断言包含必需的键
assert_contains_keys(data, ["id", "name", "email"], "用户数据")
```

## 📈 持续集成

### GitHub Actions 配置示例

```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        cd tests
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        cd tests
        pytest -m "not slow" --html=reports/test_report.html
    
    - name: Upload test report
      uses: actions/upload-artifact@v2
      with:
        name: test-report
        path: tests/reports/
```

## 🐛 常见问题

### 1. 测试环境未启动

**错误**：`Connection refused`

**解决**：确保 Wisdom-Flow 系统已启动

```bash
docker compose -f docker/docker-compose.yml up -d
```

### 2. 依赖包版本冲突

**解决**：使用虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. API Key 未配置

**错误**：`未配置 API Key，跳过测试`

**解决**：在测试配置中添加 API Key

```python
# .env 文件
TEST_API_KEY=your-api-key
```

### 4. 测试数据未清理

**解决**：测试失败时手动清理

```bash
# 运行清理脚本（如果提供）
python scripts/cleanup_test_data.py
```

---



