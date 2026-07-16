# 知识条目规范

## 存放方式

每条知识使用一个 Markdown 文件，按主题建立子目录，例如：

- `knowledge/projects/`
- `knowledge/customers/`
- `knowledge/decisions/`

## 必填元数据

```yaml
title: 条目标题
date: 2026-07-16
time: "14:30"
source: 原始材料名称或链接
status: fact
```

`status` 只能使用：

- `fact`：有明确来源支持的事实；
- `inference`：基于事实形成的推断；
- `pending-confirmation`：尚待确认的事项。

原始材料有具体时间时必须填写 `time`；没有明确时间时省略该字段，不要虚构。对于既有历史记录，除非明确要求，不为补充时间而回填或改写。

## 推荐正文结构

```markdown
## 事实

## 推断

## 待确认

## 后续动作
```
