# 测试数据目录

本目录用于存放测试所需的各类文件。

## 📁 目录结构

```
test_data/
├── README.md                    # 本文件
├── small_document.pdf          # 小文件（5页，~1MB）
├── medium_document.pdf         # 中文件（50页，~10MB）
├── large_document.pdf          # 大文件（200页，~50MB）
├── test_image.png              # 测试图片（包含文字）
├── test_excel.xlsx             # 测试 Excel 文件
├── test_word.docx              # 测试 Word 文件
└── test_ppt.pptx               # 测试 PPT 文件
```

## 📝 文件说明

### PDF 文档

- **small_document.pdf**：用于快速测试，包含基本文本、图片和表格
- **medium_document.pdf**：用于常规性能测试
- **large_document.pdf**：用于压力测试和大文件处理测试

### 其他格式

- **test_image.png**：包含中英文文字的图片，用于 OCR 测试
- **test_excel.xlsx**：包含多个 Sheet、公式和图表的 Excel 文件
- **test_word.docx**：包含格式化文本、表格和图片的 Word 文档
- **test_ppt.pptx**：包含多页幻灯片、图片和文本的 PPT 文件

## 🔨 准备测试文件

### 方法一：使用现有文档

将您的测试文档复制到本目录，并按照上述命名规则重命名。

### 方法二：生成测试文档

可以使用以下 Python 脚本生成测试 PDF：

```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_test_pdf(filename, num_pages):
    """生成测试 PDF 文件"""
    c = canvas.Canvas(filename, pagesize=letter)
    
    for i in range(num_pages):
        c.drawString(100, 750, f"测试页 {i+1}/{num_pages}")
        c.drawString(100, 700, "这是测试内容，用于文档解析测试。")
        c.drawString(100, 650, "Lorem ipsum dolor sit amet, consectetur adipiscing elit.")
        c.showPage()
    
    c.save()

# 生成小、中、大测试文件
generate_test_pdf("small_document.pdf", 5)
generate_test_pdf("medium_document.pdf", 50)
generate_test_pdf("large_document.pdf", 200)
```

### 方法三：下载示例文件

可以从公开的测试数据集下载示例文档：

- [PDF 示例](https://www.adobe.com/support/products/enterprise/knowledgecenter/media/c4611_sample_explain.pdf)
- [Office 示例](https://file-examples.com/)

## ⚠️ 注意事项

1. **文件大小**：确保测试文件符合预期大小，避免测试超时
2. **版权问题**：不要使用受版权保护的内容作为测试数据
3. **敏感信息**：测试文件中不应包含真实的敏感信息
4. **Git 忽略**：大型测试文件应添加到 `.gitignore` 中

## 📊 测试文件使用情况

| 测试用例 | 使用的文件 | 用途 |
|---------|-----------|------|
| TC-201 | small_document.pdf | PDF 解析测试 |
| TC-202 | test_image.png | OCR 识别测试 |
| TC-203 | test_excel.xlsx | Excel 解析测试 |
| TC-702 | small/medium/large_document.pdf | 解析性能测试 |

---



