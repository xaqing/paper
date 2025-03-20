class FormatRules:
    # 基础格式规则
    ABSTRACT_ZH_MAX = 500  # 中文摘要上限
    ABSTRACT_EN_MAX = 2000
    INTRO_PAGE_LIMIT = 2
    
    # 新增结构校验规则
    SECTION_ORDER = [
        'cover_zh', 'cover_en', 'declaration',
        'abstract_zh', 'abstract_en', 'toc',
        'introduction', 'literature_review', 'methodology',
        'results', 'conclusion', 'references', 'appendix'
    ]
    
    # 新增标题规则
    TITLE_LEVEL_RULES = {
        'max_level': 3,
        'first_section_max_level': 1
    }