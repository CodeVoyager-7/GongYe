# GitHub 项目接入与优化记录

## 1. 本轮改进目标

当前系统已经具备 `SRU 数据接入 -> 延迟分析 -> SLSTM 预测 -> 风险预警 -> 辅助决策 -> Streamlit 展示` 的基础闭环。本轮改进目标是从 GitHub 上筛选更适配的项目思路，并将可落地的模型接入当前工程。

## 2. 已接入的 GitHub 思路

### 2.1 `Soft_Sensor_Experiments`：VA-LSTM 思路

参考项目：

- [Soft_Sensor_Experiments](https://github.com/JustusvLiebig/Soft_Sensor_Experiments)

接入内容：

- 新增变量注意力 LSTM 模型
- 输出变量注意力权重摘要
- 与现有 `SLSTM`、`XGBoost-lag` 做统一指标对比

本地文件：

- [va_lstm_model.py](C:/Users/lenovo/Desktop/人工智能大赛/src/models/advanced/va_lstm_model.py)
- [train_va_lstm.py](C:/Users/lenovo/Desktop/人工智能大赛/src/training/train_va_lstm.py)
- [run_train_va_lstm.py](C:/Users/lenovo/Desktop/人工智能大赛/scripts/run_train_va_lstm.py)

当前结论：

- 当前实现未超过 `SLSTM`
- 可作为变量注意力和可解释性方向的备选模型
- 不建议作为当前主模型

### 2.2 `Time-Series-Library / iTransformer`：倒置 Transformer 思路

参考项目：

- [Time-Series-Library](https://github.com/thuml/Time-Series-Library)

接入内容：

- 新增 iTransformer-style 模型
- 将变量视作 token，将历史序列作为变量 token 的表示输入
- 与 `XGBoost`、`XGBoost-lag`、`SLSTM`、`VA-LSTM` 统一对比

本地文件：

- [itransformer_model.py](C:/Users/lenovo/Desktop/人工智能大赛/src/models/advanced/itransformer_model.py)
- [train_itransformer.py](C:/Users/lenovo/Desktop/人工智能大赛/src/training/train_itransformer.py)
- [run_train_itransformer.py](C:/Users/lenovo/Desktop/人工智能大赛/scripts/run_train_itransformer.py)

当前结论：

- 当前 iTransformer-style 模型取得最优测试结果
- 已作为新的最佳模型接入预测曲线、模型对比、风险预警与辅助决策链路

## 3. 最新模型结果

当前最优测试结果：

- `iTransformer-style y1 R2 = 0.7014`
- `iTransformer-style y2 R2 = 0.8165`

对比结论：

- 静态 `XGBoost` 不能有效刻画 SRU 动态过程
- `XGBoost-lag` 验证了时滞特征的有效性
- `SLSTM` 显著提升双目标预测效果
- `iTransformer-style` 进一步提升预测精度，成为当前主模型
- `VA-LSTM` 暂未提升精度，但保留了变量注意力解释方向

## 4. 仍需改进的方向

1. 增加独立测试集和多随机种子实验，避免单次训练偶然性。
2. 对 `seq_len`、学习率、层数等参数做系统调优。
3. 将风险阈值从固定分位数升级为可配置阈值。
4. 将辅助决策建议进一步接入专家知识库。
5. 增加模型解释模块，例如变量注意力可视化或 SHAP。
6. 后续可继续接入 `Merlion` 或 `MTAD-GAT`，增强异常检测模型能力。
