# Dividou
一个文件分类复制工具
## func：
把左边选的文件复制到右边选的文件夹里面
## 入口：
### 入口函数
Dividour类 的 `__init__()`……
### 用法
用的时候直接
```python
>>> Dividour()
```
## 适用场景
+ 分类照片……
+ 给文本文件的preview还没写……
## 已知Bugs
+ 缩小程序对话框的时候会导致某些控件消失，再放大的时候消失的控件就会重新出现……
+ 对于文件a，如果目标分类文件夹内有文件名相同哈希值不同的文件b存在，会导致a可以无限复制进去…没有检查…
