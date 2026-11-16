# SRU 数据集说明

## 数据来源

本数据集通过 `scikit-learn` 的 `fetch_openml` 接口从 OpenML 下载，数据集名称为 `sulfur`，常用于 `Sulfur Recovery Unit`（硫回收装置）软测量与工业时序建模任务。

## 本地文件

- 数据文件：[sru_openml.csv](C:/Users/lenovo/Desktop/人工智能大赛/data/sru/sru_openml.csv)
- 简要说明：[README.txt](C:/Users/lenovo/Desktop/人工智能大赛/data/sru/README.txt)

## 数据规模

- 样本数：`10081`
- 字段数：`7`

## 当前字段

- `a1`
- `a2`
- `a3`
- `a4`
- `a5`
- `y2`
- `y1`

## 说明

当前 OpenML 版本保存的是标准化后的字段名，输入变量被命名为 `a1-a5`，输出变量为 `y1/y2`。根据公开论文和常见 SRU 数据集说明，通常可理解为：

- `a1-a5`：5 个工艺输入变量
- `y1/y2`：2 个尾气质量或排放相关输出变量

当前已补充字段语义映射表：

- [sru_variable_mapping.csv](C:/Users/lenovo/Desktop/人工智能大赛/data/external/sru_variable_mapping.csv)
- [SRU匿名变量语义判别.md](C:/Users/lenovo/Desktop/人工智能大赛/docs/SRU匿名变量语义判别.md)

根据公开 SRU 软测量 benchmark 文献，当前字段可解释为：

- `a1`：MEA区气体流量
- `a2`：第一空气流量 AIR MEA 1
- `a3`：第二空气流量 AIR MEA 2
- `a4`：SWS区气体流量
- `a5`：SWS区空气流量
- `y1`：尾气H2S浓度
- `y2`：尾气SO2浓度

其中 `a4/a5` 在不同文献中存在顺序差异，建议在答辩中说明为“基于多数文献和数据相关性的语义推定，真实装置接入时需由位号表最终确认”。
