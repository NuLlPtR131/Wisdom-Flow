<div align="center">
  <img src="management/web/src/common/assets/images/layouts/logo-text-2.png" width="400" alt="WisdomFlow">
</div>



---

## 🌟 简介

WisdomFlow是一个基于RAG（检索增强生成）技术的智能知识管理与问答系统，专注于解决实际应用中的知识管理、文档解析与智能问答需求。

WisdomFlow提供了完整的知识管理解决方案，包括文档解析、知识库构建、智能问答、用户管理等核心功能，特别适合企业、高校等团队构建内部知识库和智能问答系统。

## 🎯 核心功能

### 🔧 强大的后台管理系统
- **用户管理**：支持用户创建、权限配置、团队管理
- **知识库管理**：灵活创建、编辑、删除知识库，支持批量操作
- **文件管理**：集中管理所有上传的文档，支持批量解析与导入
- **系统配置**：灵活配置模型参数、解析引擎、存储设置等

### 📄 增强的文档解析能力
- **MinerU解析引擎**：替代传统DeepDoc算法，提供更精准的文档解析
- **多格式支持**：支持PDF、Word、Excel、PPT等多种文档格式
- **图片解析**：支持文档中图片的解析与存储
- **结构保留**：保持文档原有的结构和格式信息

### 💬 智能问答系统
- **RAG技术**：基于检索增强生成，确保回答的准确性和可溯源性
- **图文输出**：支持模型回答时关联引用文本块的相关图片
- **多模型支持**：兼容多种主流大语言模型
- **流式输出**：支持实时响应的流式回答体验

### 📝 文档撰写模式
- **全新交互体验**：提供类似文档编辑的问答模式
- **上下文管理**：支持长文档的分段撰写与管理
- **格式控制**：支持基本的文本格式控制

### 🎨 用户友好界面
- **权限回收**：前台系统简化用户界面，聚焦核心功能
- **主题支持**：支持多种主题切换，满足不同用户偏好
- **响应式设计**：适配不同屏幕尺寸的设备

## 🏗️ 系统架构

WisdomFlow采用模块化的架构设计，各组件之间松耦合，便于扩展和维护：

```
WisdomFlow/
├── api/                 # 后端API服务
│   ├── apps/           # 应用模块
│   ├── db/             # 数据库管理
│   └── utils/          # 工具函数
├── agentic_reasoning/  # 智能推理模块
├── graphrag/           # 图RAG功能模块
├── management/         # 管理后台
│   ├── server/         # 管理后台服务
│   └── web/            # 管理后台前端
├── rag/                # RAG核心功能
│   ├── app/            # 应用核心
│   ├── llm/            # 大语言模型集成
│   └── utils/          # RAG工具函数
├── sdk/                # Python SDK
└── web/                # 前端应用
    ├── public/         # 静态资源
    └── src/            # 前端源码
```

### 核心模块说明

#### 1. 前端应用 (web/)
- 基于Vue.js和TypeScript开发
- 提供用户友好的问答界面
- 支持文档撰写模式
- 响应式设计，适配多种设备

#### 2. 后端API (api/)
- 基于Flask开发的RESTful API
- 处理用户请求、文档管理、知识库操作等
- 提供与前端和管理后台的交互接口

#### 3. 管理后台 (management/)
- 独立的后台管理系统
- 基于V3 Admin Vite框架
- 支持用户、团队、知识库、文件等管理功能

#### 4. RAG核心 (rag/)
- 实现检索增强生成的核心逻辑
- 集成多种文档解析引擎
- 知识库构建与检索算法
- 与大语言模型的交互接口

#### 5. 智能推理 (agentic_reasoning/)
- 提供深度推理和研究能力
- 基于提示工程的智能决策

#### 6. 图RAG (graphrag/)
- 基于图结构的知识库表示
- 实体关系提取与分析
- 图检索与推理算法

#### 7. SDK (sdk/)
- Python SDK，方便开发者集成
- 提供与WisdomFlow的交互接口
- 支持知识库管理、文档上传、问答调用等功能

## 📥 快速开始

### 1. 硬件要求

- 内存要求: 最低16G以上，推荐32G以上
- GPU要求：Turing及以后架构，6G显存以上
- 磁盘空间要求: 20G以上，推荐使用SSD

### 2. 部署方式

推荐使用Docker进行部署，简单快捷：

```bash
# 克隆项目代码
git clone https://github.com/zstar1003/ragflow-plus.git
cd ragflow-plus

# 启动服务
docker compose -f docker/docker-compose.yml up -d
```

### 3. 访问系统

- **前端应用**: http://localhost
- **管理后台**: http://localhost/admin
- **API地址**: http://localhost/api/v1

## 🔧 如何使用

### 1. 创建知识库

通过管理后台或API创建知识库，用于存储和管理文档。

### 2. 上传文档

上传需要管理的文档，系统将自动解析并存储到知识库中。

### 3. 智能问答

在前端应用中提问，系统将基于知识库内容生成准确的回答。

### 4. 文档撰写

使用文档撰写模式，进行长文档的创作和管理。

## 📚 API文档

WisdomFlow提供完整的API接口，支持通过SDK或直接调用API进行集成：

### Python SDK

```python
from ragflow_sdk import RAGFlow

# 初始化SDK
api_key = "your-api-key"
base_url = "http://localhost:9380"
rag_object = RAGFlow(api_key=api_key, base_url=base_url)

# 创建知识库
dataset = rag_object.create_dataset(name="my-knowledge-base")

# 上传文档
rag_object.upload_document(dataset_id=dataset.id, file_path="document.pdf")
```

### OpenAI兼容API

```python
from openai import OpenAI

model = "deepseek-r1:1.5b"
client = OpenAI(api_key="your-api-key", base_url=f"http://localhost/api/v1/chats_openai/{dialog_id}")

completion = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": "你是一个乐于助人的助手"},
        {"role": "user", "content": "你是谁？"},
    ],
    stream=True
)
```

## 🛠️ 如何贡献

1. Fork本GitHub仓库
2. 将fork克隆到本地：  
`git clone git@github.com:<你的用户名>/ragflow-plus.git`
3. 创建本地分支：  
`git checkout -b my-branch`
4. 提交信息需包含充分说明：  
`git commit -m '提交信息需包含充分说明'`
5. 推送更改到GitHub（含必要提交信息）：  
`git push origin my-branch`
6. 提交PR等待审核

## 🚀 鸣谢

本项目基于以下开源项目开发：

- [ragflow](https://github.com/infiniflow/ragflow)
- [v3-admin-vite](https://github.com/un-pany/v3-admin-vite)
- [minerU](https://github.com/opendatalab/MinerU)



## 📜 许可证与使用限制
1. **本仓库基于AGPLv3许可证**  
   由于包含第三方AGPLv3代码，本项目必须遵循AGPLv3的全部条款。这意味着：
   - 任何**衍生作品**（包括修改或组合代码）必须继续使用AGPLv3并公开源代码。  
   - 若通过**网络服务**提供本软件，用户有权获取对应源码。

2. **商用说明**  
   - **允许商用**：本软件遵循AGPLv3，允许商业使用，包括SaaS和企业内部部署。
   - **不修改代码**：若仅原样运行（不修改、不衍生），仍需遵守AGPLv3，包括：  
     - 提供完整的源代码（即使未修改）。  
     - 若作为网络服务提供，需允许用户下载对应源码（AGPLv3第13条）。
   - **不允许闭源商用**：如需闭源（不公开修改后的代码）商用，需获得所有代码版权持有人的书面授权（包括上游AGPLv3代码作者）  

3. **免责声明**  
   本项目不提供任何担保，使用者需自行承担合规风险。若需法律建议，请咨询专业律师。


