class ThesisParser:
    def __init__(self, doc_path):
        self.doc = Document(doc_path)
        self.metadata = self._parse_metadata()
    
    def _parse_metadata(self):
        """解析封面、摘要等元数据"""
        return {
            'ch_title': self._extract_chinese_title(),
            'en_title': self._extract_english_title(),
            'abstract_zh': self._get_section_text('中文摘要'),
            'abstract_en': self._get_section_text('英文摘要')
        }

    def _extract_chinese_title(self):
        """提取中文题目（处理多行情况）"""
        for p in self.doc.paragraphs:
            if '题目：' in p.text:
                return p.text.split('：')[1].strip()