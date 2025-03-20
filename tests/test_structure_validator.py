import pytest
from unittest.mock import MagicMock
from unittest.mock import patch
# 移除错误导入
# from re_validator import DocxStructureValidator

# 保留正确导入
from src.validators.structure_validator import DocxStructureValidator

@patch('src.validators.structure_validator.DocxStructureValidator._load_document')
def test_style_consistency(mock_load):
    """测试样式一致性检测（仅验证字体和段落间距）"""
    validator = DocxStructureValidator()

    # Mock 文档对象
    mock_doc = MagicMock()
    
    # 模拟所有段落字体一致
    normal_para = MagicMock()
    normal_para.style.name = 'Normal'
    normal_para.style.font.name = 'Times New Roman'
    normal_para.paragraph_format.space_after.pt = 12

    mock_doc.paragraphs = [normal_para for _ in range(5)]
    
    # 配置mock返回
    mock_load.return_value = mock_doc

    # 执行
    result = validator.validate_style_consistency("dummy_path.docx")

    # 断言（仅保留样式相关断言）
    assert result["font_consistency"] is True
    assert result["paragraph_spacing"] is True


def test_missing_college_name():
    """测试缺失学院名称"""
    validator = DocxStructureValidator()
    mock_doc = MagicMock()
    mock_doc.inline_shapes.__len__.return_value = 1  # LOGO存在
    mock_doc.paragraphs = [
        MagicMock(text="题    目：\t基于深度学习的文档解析"),  # 标题存在
        MagicMock(text="学校名称：\tXX大学")  # 学校存在
    ]
    result = validator._check_cover(mock_doc)
    assert '学院名称' in result['missing_fields']


def test_missing_school_name():
    """测试缺失学校名称（根据需求学校名称非必填）"""
    validator = DocxStructureValidator()
    mock_doc = MagicMock()
    mock_doc.inline_shapes.__len__.return_value = 1  # LOGO存在
    mock_doc.paragraphs = [
        MagicMock(text="题    目：\t基于深度学习的文档解析"),
        MagicMock(text="学  院：\t外国语学院")  # 学院存在
        # 没有学校（根据需求允许）
    ]
    result = validator._check_cover(mock_doc)
    # 学校名称不是必检字段，应该不会出现在缺失字段中
    assert '学校名称' not in result['missing_fields']

def test_missing_title():  # 原测试需要同步调整
    """测试缺失标题"""
    validator = DocxStructureValidator()
    mock_doc = MagicMock()
    mock_doc.inline_shapes.__len__.return_value = 1  # LOGO存在
    mock_doc.paragraphs = [
        MagicMock(text="学  院：\t外国语学院"),
        # 缺失题目（必填项）
    ]
    result = validator._check_cover(mock_doc)
    assert '论文标题' in result['missing_fields']


def test_missing_logo():
    """测试缺失LOGO"""
    validator = DocxStructureValidator()
    mock_doc = MagicMock()
    mock_doc.inline_shapes.__len__.return_value = 0  # LOGO缺失
    mock_doc.paragraphs = [
        MagicMock(text="题    目：\t基于深度学习的文档解析"),
        MagicMock(text="学  院：\t外国语学院"),
        MagicMock(text="学校名称：\tXX大学")
    ]
    result = validator._check_cover(mock_doc)
    assert '学校LOGO' in result['missing_fields']


def test_full_cover():
    """测试完整封面"""
    validator = DocxStructureValidator()
    mock_doc = MagicMock()
    mock_doc.inline_shapes.__len__.return_value = 1  # LOGO存在
    mock_doc.paragraphs = [
        MagicMock(text="题    目：\t中华优秀传统文化融入初中英语阅读教学研究"),
        MagicMock(text="学  院：\t外国语学院"),
        MagicMock(text="学校名称：\tXX大学"),
        MagicMock(text="作者：李四")
    ]
    result = validator._check_cover(mock_doc)
    assert result['exists'] is True
    assert result['missing_fields'] == []


def test_enhanced_cover_validation():
    """验证增强版封面检测逻辑"""
    validator = DocxStructureValidator()
    
    # 测试缺失学院的情况
    missing_college_doc = MagicMock()
    missing_college_doc.inline_shapes.__len__.return_value = 1
    missing_college_doc.paragraphs = [
        MagicMock(text="题    目：\t深度学习研究"),  # 包含标题
        MagicMock(text="学校名称：XX大学")  # 包含学校
    ]
    
    missing_result = validator._check_cover(missing_college_doc)
    assert '学院名称' in missing_result['missing_fields']

    # 测试缺失学校的情况
    missing_school_doc = MagicMock()
    missing_school_doc.inline_shapes.__len__.return_value = 1
    missing_school_doc.paragraphs = [
        MagicMock(text="学院：外国语学院"),  # 包含学院
        MagicMock(text="论文标题：XX研究")
    ]
    
    school_result = validator._check_cover(missing_school_doc)
    assert '学校名称' not in school_result['missing_fields']  # 根据源码逻辑，学校名称不是必检字段


def test_multiple_logos():
    """测试多个LOGO情况（应视为有效）"""
    validator = DocxStructureValidator()
    mock_doc = MagicMock()
    mock_doc.inline_shapes.__len__.return_value = 3  # 多个LOGO
    mock_doc.paragraphs = [
        MagicMock(text="题    目：\t跨文化交际研究"),
        MagicMock(text="学  院：\t国际关系学院")
    ]
    result = validator._check_cover(mock_doc)
    assert '学校LOGO' not in result['missing_fields']


def test_cover_field_priority():
    """验证封面字段检测优先级（标题>学院>LOGO）"""
    validator = DocxStructureValidator()
    mock_doc = MagicMock()
    mock_doc.inline_shapes.__len__.return_value = 0  # 缺失LOGO
    mock_doc.paragraphs = [
        # 同时缺失标题和学院
        MagicMock(text="学校名称：\tXX大学")
    ]
    
    result = validator._check_cover(mock_doc)
    # 应优先报告标题缺失
    assert '论文标题' in result['missing_fields']
    assert '学院名称' in result['missing_fields']
    assert result['missing_fields'].index('论文标题') < result['missing_fields'].index('学院名称')


@patch('src.validators.structure_validator.DocxStructureValidator._load_document')
def test_mixed_font_styles(mock_load):
    """测试混合字体样式检测"""
    validator = DocxStructureValidator()
    mock_doc = MagicMock()
    
    # 创建混合样式的段落
    para1 = MagicMock(style=MagicMock(name='Normal', font=MagicMock(name='Times New Roman')))
    para2 = MagicMock(style=MagicMock(name='Heading 1', font=MagicMock(name='Arial')))
    
    mock_doc.paragraphs = [para1, para2]
    # 配置mock返回
    mock_load.return_value = mock_doc
    
    result = validator.validate_style_consistency("dummy.docx")
    assert result["font_consistency"] is False

@patch('src.validators.structure_validator.DocxStructureValidator._load_document')
def test_paragraph_spacing_levels(mock_load):
    """测试多级段落间距合规性"""
    validator = DocxStructureValidator()
    mock_doc = MagicMock()
    
    # 12磅（合规）、18磅（合规）、8磅（违规）
    paras = [
        MagicMock(paragraph_format=MagicMock(space_after=MagicMock(pt=12))),
        MagicMock(paragraph_format=MagicMock(space_after=MagicMock(pt=18))),
        MagicMock(paragraph_format=MagicMock(space_after=MagicMock(pt=8)))
    ]
    
    mock_doc.paragraphs = paras
    # 配置mock返回
    mock_load.return_value = mock_doc
    
    result = validator.validate_style_consistency("dummy.docx")
    assert result["paragraph_spacing"] is False

