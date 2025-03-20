class FormatValidator:
    def check_cover(self):
        """封面校验逻辑"""
        errors = []
        # 检查中文题目长度合理性
        if len(self.parser.metadata['ch_title']) > 50:
            errors.append(FormatError('CH_TITLE_TOO_LONG', severity=2))
        
        # 检查承诺书签名
        if not self._find_digital_signature():
            errors.append(FormatError('MISSING_SIGNATURE', severity=3))
        
        return errors

    def _find_digital_signature(self):
        """检测电子签名（图片识别+文字匹配）"""
        # 使用OpenCV识别签名区域
        # 匹配"承诺人（签名）："后的内容