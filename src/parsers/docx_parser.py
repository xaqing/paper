class DocxParser:
    def extract_sections(self, doc):
        """识别文档结构模块"""
        section_ranges = {
            'cover_zh': self._find_section(doc, '中文封面', max_pages=1),
            'declaration': self._find_commitment(doc),
            'abstract_zh': self._detect_abstract(doc, language='zh'),
            'toc': self._detect_table_of_contents(doc)
        }
        return section_ranges

    def _find_commitment(self, doc):
        """诚信承诺书定位（新增正则匹配）"""
        pattern = re.compile(r'我谨在此承诺：.*?《(.*?)》', re.DOTALL)
        for i, p in enumerate(doc.paragraphs):
            if match := pattern.search(p.text):
                return {
                    'start': i,
                    'title': match.group(1),
                    'has_signature': self._check_signature(doc, i)
                }

    def _detect_table_of_contents(self, doc):
        """目录检测（增强版）"""
        return {
            'is_auto_generated': 'TOC' in [s.name for s in doc.styles],
            'levels': self._analyze_toc_levels(doc)
        }