def export_with_comments(paper_id):
    """生成带批注的Word文档"""
    doc = Document()
    paper = ResearchPaper.objects.get(id=paper_id)
    
    # 插入原始内容
    for paragraph in paper.parsed_content:
        doc.add_paragraph(paragraph['text'])
        
    # 添加批注
    for comment in paper.comments.all():
        add_comment_to_docx(
            doc,
            start=comment.start_char,
            end=comment.end_char,
            text=comment.comment_text
        )
    
    return doc