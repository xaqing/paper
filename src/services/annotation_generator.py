class AnnotationBuilder:
    def build_general_comments(self):
        """生成统一批注"""
        return [
            {
                'type': 'GLOBAL',
                'content': '全文格式参照外国语学院论文排版规范进行修改',
                'position': 'cover'
            },
            {
                'type': 'GLOBAL', 
                'content': '再次核查全文语法及拼写错误并修改',
                'position': 'footer'
            }
        ]

    def create_structural_comment(self, issue):
        """构建结构问题批注"""
        return {
            'rule_id': issue.rule_id,
            'position': self._get_char_position(issue.section),
            'suggestions': self._get_fix_suggestions(issue.type)
        }