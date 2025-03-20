class ContentAnalyzer:
    def analyze_abstract(self):
        """中英文摘要对比分析"""
        zh_len = len(self.parser.metadata['abstract_zh'])
        en_len = len(self.parser.metadata['abstract_en'])
        
        if zh_len > 500:
            yield ContentIssue('ABSTRACT_ZH_TOO_LONG', position='abstract_zh')
        if en_len > 2000:
            yield ContentIssue('ABSTRACT_EN_TOO_LONG', position='abstract_en')
        
        # 使用spacy进行语义对比
        similarity = self._calculate_semantic_similarity()
        if similarity < 0.7:
            yield ContentIssue('ABSTRACT_MISMATCH', severity=2)

    def check_references(self):
        """参考文献交叉验证"""
        # 提取文内引用标记
        citations = re.findall(r'\(([A-Za-z]+,?\s\d{4})\)', self.full_text)
        # 验证与参考文献列表的匹配