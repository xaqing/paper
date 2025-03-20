class FormatAnnotator:
    def generate_final_comments(self, errors):
        """生成总结性批注（新增实现）"""
        major_errors = [e for e in errors if e.startswith('ERR_MAJOR')]
        return [
            "全文格式需参照外国语学院规范修改",
            "请再次核查语法及拼写错误"
        ] + [ERROR_MAP[e] for e in major_errors]

    def create_annotation(self, error_type, position):
        """创建批注数据结构（新增）"""
        return {
            'type': error_type,
            'message': ERROR_MAP.get(error_type, '未知错误类型'),
            'start_char': position['start'],
            'end_char': position['end'],
            'severity': SEVERITY_LEVEL[error_type]
        }