class ThesisComment(models.Model):
    CATEGORY_CHOICES = [
        ('format', '格式问题'),
        ('content', '内容问题'),
        ('academic', '学术规范')
    ]
    
    paper = models.ForeignKey(ResearchPaper, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    start_char = models.IntegerField()  # 批注起始位置
    end_char = models.IntegerField()
    auto_generated = models.BooleanField(default=True)
    resolved = models.BooleanField(default=False)
    comment_text = models.TextField()
    severity = models.IntegerField(choices=[(1, '建议'), (2, '警告'), (3, '严重')])