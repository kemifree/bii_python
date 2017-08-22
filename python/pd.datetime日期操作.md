# 日期操作

#### 字符串日期选择
```
table['日期'] = table['日期范围'].str.findall(r'\d{4}-\d{2}-\d{2}').str.get(1)
```
