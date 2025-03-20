class PaperCheckingSystem:
    def process_document(self, file_path):
        # 文档解析
        doc = DocxParser().parse(file_path)
        
        # 执行校验
        errors = []
        errors += StructureValidator().validate(doc)
        errors += BodyAnalyzer().analyze(doc)
        errors += FormatValidator().check(doc)
        
        # 生成批注
        annotations = FormatAnnotator().generate(errors)
        
        # 生成最终报告
        report = {
            'summary': self._generate_summary(errors),
            'annotations': annotations,
            'statistics': self._compile_stats(errors)
        }
        
        # 保存结果到<mcsymbol name="ResearchPaper" filename="models.py" path="c:\Users\Administrator\Desktop\paper\src\models.py" startline="1" type="class"></mcsymbol>
        self._save_to_database(doc, report)