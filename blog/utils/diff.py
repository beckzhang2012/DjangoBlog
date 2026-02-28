#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
文本差异对比工具
"""
from diff_match_patch import diff_match_patch
from django.utils.html import escape


def get_diff_text(old_text: str, new_text: str) -> str:
    """
    对比两个文本的差异并返回高亮显示的HTML
    """
    dmp = diff_match_patch()
    diffs = dmp.diff_main(old_text, new_text)
    dmp.diff_cleanupSemantic(diffs)
    
    html = []
    for op, data in diffs:
        text = escape(data)
        if op == 0:  # 相同文本
            html.append(f'<span class="diff-equal">{text}</span>')
        elif op == 1:  # 新增文本
            html.append(f'<span class="diff-insert">{text}</span>')
        elif op == -1:  # 删除文本
            html.append(f'<span class="diff-delete">{text}</span>')
    
    return ''.join(html)


def get_version_diff(version1, version2):
    """
    获取两个版本之间的差异
    """
    title_diff = get_diff_text(version1.title, version2.title)
    body_diff = get_diff_text(version1.body, version2.body)
    
    return {
        'title_diff': title_diff,
        'body_diff': body_diff,
        'version1': version1,
        'version2': version2
    }
