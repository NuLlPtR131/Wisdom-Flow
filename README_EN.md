<div align="center">
  <img src="management/web/src/common/assets/images/layouts/logo-text-2.png" width="400" alt="WisdomFlow">
</div>



## 🌟 Introduction

**WisdomFlow**  is an intelligent knowledge management and question-answering system based on RAG (Retrieval-Augmented Generation) technology. It focuses on solving practical needs in knowledge management, document parsing, and intelligent question-answering.

WisdomFlow provides a complete knowledge management solution, including document parsing, knowledge base construction, intelligent question-answering, user management, and other core functions. It is particularly suitable for enterprises, universities, and other teams to build internal knowledge bases and intelligent question-answering systems.

## 🎯 Core Features

### 🔧 Powerful Admin Management System
- **User Management**: Support user creation, permission configuration, and team management
- **Knowledge Base Management**: Flexible creation, editing, and deletion of knowledge bases with batch operations
- **File Management**: Centralized management of all uploaded documents with batch parsing and import
- **System Configuration**: Flexible configuration of model parameters, parsing engines, storage settings, etc.

### 📄 Enhanced Document Parsing
- **MinerU Parsing Engine**: Replaces traditional DeepDoc algorithm for more accurate document parsing
- **Multi-format Support**: Supports PDF, Word, Excel, PPT, and other document formats
- **Image Parsing**: Supports parsing and storage of images in documents
- **Structure Preservation**: Maintains the original structure and formatting of documents

### 💬 Intelligent Question-Answering System
- **RAG Technology**: Based on retrieval-augmented generation to ensure answer accuracy and traceability
- **Text-Image Output**: Supports displaying related images linked to referenced text blocks in model responses
- **Multi-model Support**: Compatible with multiple mainstream large language models
- **Streaming Output**: Supports real-time streaming answer experience

### 📝 Document Writing Mode
- **New Interactive Experience**: Provides document editing-like question-answering mode
- **Context Management**: Supports segmented writing and management of long documents
- **Format Control**: Supports basic text formatting control

### 🎨 User-Friendly Interface
- **Permission Reclaiming**: Frontend system simplifies user interface, focusing on core functions
- **Theme Support**: Supports multiple theme switching to meet different user preferences
- **Responsive Design**: Adapts to devices with different screen sizes

## 🏗️ System Architecture

WisdomFlow adopts a modular architecture design with loosely coupled components for easy expansion and maintenance:

```
WisdomFlow/
├── api/                 # Backend API services
│   ├── apps/           # Application modules
│   ├── db/             # Database management
│   └── utils/          # Utility functions
├── agentic_reasoning/  # Intelligent reasoning module
├── graphrag/           # Graph RAG function module
├── management/         # Admin background
│   ├── server/         # Admin backend services
│   └── web/            # Admin frontend
├── rag/                # RAG core functions
│   ├── app/            # Application core
│   ├── llm/            # Large language model integration
│   └── utils/          # RAG utility functions
├── sdk/                # Python SDK
└── web/                # Frontend application
    ├── public/         # Static resources
    └── src/            # Frontend source code
```

### Core Module Description

#### 1. Frontend Application (web/)
- Developed based on Vue.js and TypeScript
- Provides user-friendly question-answering interface
- Supports document writing mode
- Responsive design, adapting to multiple devices

#### 2. Backend API (api/)
- RESTful API developed based on Flask
- Handles user requests, document management, knowledge base operations, etc.
- Provides interaction interface with frontend and admin background

#### 3. Admin Background (management/)
- Independent admin management system
- Based on V3 Admin Vite framework
- Supports user, team, knowledge base, file, and other management functions

#### 4. RAG Core (rag/)
- Implements core logic of retrieval-augmented generation
- Integrates multiple document parsing engines
- Knowledge base construction and retrieval algorithms
- Interaction interface with large language models

#### 5. Intelligent Reasoning (agentic_reasoning/)
- Provides deep reasoning and research capabilities
- Intelligent decision-making based on prompt engineering

#### 6. Graph RAG (graphrag/)
- Knowledge base representation based on graph structure
- Entity relationship extraction and analysis
- Graph retrieval and reasoning algorithms

#### 7. SDK (sdk/)
- Python SDK for easy developer integration
- Provides interaction interface with WisdomFlow
- Supports knowledge base management, document upload, question-answering calls, etc.

## 📥 Quick Start

### 1. Hardware Requirements

- Memory: Minimum 16G, recommended 32G or more
- GPU: Turing and later architectures, 6G VRAM or more
- Disk space: 20G or more, SSD recommended

### 2. Deployment Method

Docker deployment is recommended for simplicity and speed:

```bash
# Clone project code
git clone https://github.com/zstar1003/ragflow-plus.git
cd ragflow-plus

# Start service
docker compose -f docker/docker-compose.yml up -d
```

### 3. Access System

- **Frontend Application**: http://localhost
- **Admin Background**: http://localhost/admin
- **API Address**: http://localhost/api/v1

## 🔧 How to Use

### 1. Create Knowledge Base

Create a knowledge base through the admin background or API for storing and managing documents.

### 2. Upload Documents

Upload documents to be managed, and the system will automatically parse and store them in the knowledge base.

### 3. Intelligent Question-Answering

Ask questions in the frontend application, and the system will generate accurate answers based on the knowledge base content.

### 4. Document Writing

Use document writing mode for creating and managing long documents.

## 📚 API Documentation

WisdomFlow provides a complete API interface, supporting integration through SDK or direct API calls:

### Python SDK

```python
from ragflow_sdk import RAGFlow

# Initialize SDK
api_key = "your-api-key"
base_url = "http://localhost:9380"
rag_object = RAGFlow(api_key=api_key, base_url=base_url)

# Create knowledge base
dataset = rag_object.create_dataset(name="my-knowledge-base")

# Upload document
rag_object.upload_document(dataset_id=dataset.id, file_path="document.pdf")
```

### OpenAI Compatible API

```python
from openai import OpenAI

model = "deepseek-r1:1.5b"
client = OpenAI(api_key="your-api-key", base_url=f"http://localhost/api/v1/chats_openai/{dialog_id}")

completion = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Who are you?"},
    ],
    stream=True
)
```

## 🛠️ How to Contribute

1. **Fork** this GitHub repository
2. Clone your fork locally:

   ```bash
   git clone git@github.com:<your-username>/ragflow-plus.git
   ```
3. Create a new branch:

   ```bash
   git checkout -b my-branch
   ```
4. Commit with a descriptive message:

   ```bash
   git commit -m 'Provide a clear and descriptive commit message'
   ```
5. Push changes to GitHub:

   ```bash
   git push origin my-branch
   ```
6. Submit a PR and wait for review.

## 🚀 Acknowledgements

This project is based on the following open-source projects:

* [ragflow](https://github.com/infiniflow/ragflow)
* [v3-admin-vite](https://github.com/un-pany/v3-admin-vite)
* [minerU](https://github.com/opendatalab/MinerU)

