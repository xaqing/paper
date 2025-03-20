class BodyAnalyzer:
    def analyze_introduction(self, section):
        """引言部分校验（新增页数限制）"""
        errors = []
        if section['page_count'] > FormatRules.INTRO_PAGE_LIMIT:
            errors.append('ERR_INTRO_TOO_LONG')
        
        # 检测二级标题
        if any(h.level >=2 for h in section['headings']):
            errors.append('ERR_INTRO_SUBHEADINGS')
        
        return errors

    def check_references(self, doc_sections):
        """参考文献交叉验证（新增实现）"""
        cited_refs = self._extract_citations(doc_sections['body'])
        listed_refs = self._parse_reference_list(doc_sections['references'])
        
        return {
            'unused_refs': list(set(listed_refs) - set(cited_refs)),
            'uncited_sources': list(set(cited_refs) - set(listed_refs))
        }