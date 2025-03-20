import pytest
from unittest.mock import Mock
# 新增以下导入
from docx import Document  # 导入缺失的Document类
import httpx  # 导入HTTPX模块
from src.parsers.ai_enhanced_parser import AIParser, DocxParser, RetryableError, PermanentError  # 导入自定义异常

@pytest.fixture
def mock_config(mocker):
    """增强配置模拟"""
    config = {
        "ai_integration": {
            "deepseek_r1": {
                "enabled": True,
                "api_base": "http://mock-api",
                "api_key_path": "./config/api_keys/deepseek.yaml",  # 保持路径一致性
                "modules": {"content_evaluation": True}
            }
        }
    }
    # 新增文件存在性模拟
    mocker.patch('os.path.exists', side_effect=lambda path: 
        path == config['ai_integration']['deepseek_r1']['api_key_path'] or 
        path == 'test.docx')
    return config

@pytest.fixture  # 添加fixture装饰器（关键修复）
def mock_docx(mocker):
    """完全隔离文档初始化过程"""
    mock_doc = mocker.Mock()
    mock_para = mocker.Mock(text="测试标题")
    mock_doc.paragraphs = [mock_para]
    
    # 深度拦截docx初始化过程
    mocker.patch('src.parsers.ai_enhanced_parser.Document', return_value=mock_doc)
    mocker.patch('docx.Document', return_value=mock_doc)
    # 拦截ZIP文件校验
    mocker.patch('zipfile.is_zipfile', return_value=True)
    # 替换物理包读取器
    mocker.patch('docx.opc.phys_pkg.PhysPkgReader.__new__', lambda cls, *args: Mock())
    
    return mock_doc

def test_server_error_retry(mock_config, mocker, mock_docx):
    """测试服务端错误重试逻辑"""
    # 新增API密钥读取模拟
    mocker.patch.object(DocxParser, '_load_api_key', return_value="mock_api_key")
    
    # 统一使用模拟文档
    parser = DocxParser(mock_config)
    parser.doc = mock_docx  # 注入模拟文档
    
    # 模拟500错误
    mocker.patch('httpx.Client.post', side_effect=httpx.HTTPStatusError(
        "Server error", request=Mock(), response=Mock(status_code=500)
    ))
    
    with pytest.raises(RetryableError):
        parser.parse_advanced("test.docx")

def test_client_error_handling(mock_config, mocker, mock_docx):
    """测试客户端错误处理"""
    # 新增API密钥读取模拟
    mocker.patch.object(DocxParser, '_load_api_key', return_value="mock_api_key")
    
    # 统一使用模拟文档
    parser = DocxParser(mock_config)
    parser.doc = mock_docx  # 注入模拟文档
    
    # 模拟400错误
    mocker.patch('httpx.Client.post', side_effect=httpx.HTTPStatusError(
        "Bad request", request=Mock(), response=Mock(status_code=400)
    ))
    
    with pytest.raises(PermanentError):
        parser.parse_advanced("test.docx")