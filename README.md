# 智碳云析

面向研究生人工智能创新大赛的 SRU 硫回收项目，目标是把“工业时序预测 + 风险预警 + 专家知识 + 可视化展示”做成一个适合演示和答辩的平台。

## 项目目标

- 提前预测尾气中 `H2S` 和 `SO2` 的变化趋势
- 识别异常工况并给出预警等级
- 结合专家知识库生成可解释的排查建议
- 用更大众化的界面帮助评委快速理解项目价值

## 当前结构

```text
人工智能大赛/
├─ config/
├─ data/
├─ docs/
├─ notebooks/
├─ outputs/
├─ scripts/
├─ src/
├─ tests/
├─ requirements.txt
└─ README.md
```

## 数据集

当前已接入公开 `SRU` 数据集：

- [sru_openml.csv](C:/Users/lenovo/Desktop/人工智能大赛/data/raw/sru/sru_openml.csv)
- [SRU 数据说明](C:/Users/lenovo/Desktop/人工智能大赛/data/raw/sru/README.md)
- [匿名变量语义判别文档](C:/Users/lenovo/Desktop/人工智能大赛/docs/SRU匿名变量语义判别.md)

当前项目内采用的变量解释为：

- `a1`: MEA 区气体流量
- `a2`: AIR MEA 1 第一空气流量
- `a3`: AIR MEA 2 第二空气流量 / 反馈配风
- `a4`: SWS 区气体流量
- `a5`: AIR SWS 空气流量
- `y1`: 尾气 H2S 浓度
- `y2`: 尾气 SO2 浓度

## 可视化页面

当前 Streamlit 界面分为 6 个页面：

- `总览首页`：面向评委的一眼看懂版入口
- `风险监控`：查看告警、阈值和风险变化
- `模型能力`：展示不同模型的预测效果
- `智能建议`：展示告警解释与排查建议
- `平台增强`：在线推理、阈值预览、知识库和告警追踪
- `技术细节`：面向专业评审的补充页

## 启动方式

启动可视化平台：

```bash
cd E:\工业系统\demo_1\demo
python scripts/run_dashboard.py
```

默认地址：

```text
http://127.0.0.1:8501
```

运行测试：

```bash
python scripts/run_tests.py
```

## 常用脚本

```bash
python scripts/run_train_baseline.py
python scripts/run_train_lag_baseline.py
python scripts/run_train_slstm.py
python scripts/run_train_va_lstm.py
python scripts/run_train_itransformer.py
python scripts/run_eda_analysis.py
python scripts/run_result_visualization.py
python scripts/run_risk_warning.py
python scripts/run_decision_support.py
python scripts/run_tests.py
```


