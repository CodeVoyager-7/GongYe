# GitHub 可移植项目选型与实施清单

## 1. 目标

本文档用于回答两个问题：

1. 在 GitHub 上有哪些和当前 SRU 项目贴近、同时具有创意的参考项目。
2. 这些项目里哪些适合直接移植，哪些更适合借鉴思路后本地实现。

当前项目的核心场景不是泛化的工业 AI，而是：

- 基于 SRU 时序数据做尾气 `H2S` / `SO2` 预测
- 将预测结果转换为风险预警
- 结合专家知识做可解释建议
- 用更大众化的界面向评委展示价值

因此，选型标准不是“仓库是否最火”，而是看它是否有助于增强以下 4 个能力：

- 大众化可视化
- 风险解释与可信度表达
- 在线推理与平台化展示
- 可持续扩展的工程结构

## 2. 总体结论

### 2.1 最值得借鉴的方向

最有价值的 GitHub 参考项目并不一定是“也做硫回收”的仓库，而是那些已经把下面这条链路做顺了的项目：

`工业时序建模 -> 风险识别 -> 解释输出 -> 可视化展示`

对你们当前项目最有帮助的，不是整仓照搬，而是分模块移植：

- 首页叙事和数字孪生式总览
- 风险可靠性分层
- 告警历史和人工复核机制
- 特征贡献解释
- 前后端接口化思路

### 2.2 当前优先级排序

1. 先借鉴异常检测/预测性维护类项目中的“解释与可靠性”模块
2. 再借鉴工业数字孪生/指挥中心类项目中的“展示与叙事”模块
3. 最后再考虑更重的工程架构升级，如 FastAPI + React 重构

## 3. 重点项目清单

## 3.1 `energy-sandbox`

- 仓库：[databricks-industry-solutions/energy-sandbox](https://github.com/databricks-industry-solutions/energy-sandbox)
- 定位：工业能源场景的 command center / digital twin / AI assistant 展示平台
- 创意点：
  - 首页像工业指挥中心，而不是普通数据页
  - 将数字孪生、自然语言交互、业务指标和时序监控融合到一个演示系统中
  - 适合做“评委一眼看懂”的大屏叙事

### 适合你们移植什么

- 首页的指挥中心式叙事结构
- 流程图或设备示意图驱动的展示方式
- 从“模型页”转向“业务问题页”的表达逻辑

### 不建议直接照搬什么

- Databricks 全套工程依赖
- 云端数据与平台服务绑定的实现方式

### 适配结论

- 可移植度：中
- 借鉴价值：高
- 推荐方式：只借展示思路，不整仓接入

## 3.2 `anomaly-detection-system`

- 仓库：[Kyulim-Kim/anomaly-detection-system](https://github.com/Kyulim-Kim/anomaly-detection-system)
- 定位：异常检测系统，强调解释性、可靠性和人工复核
- 创意点：
  - 不把模型输出当作最终结论，而是当作预警信号
  - 引入可靠性判断和人工复核机制
  - 适合做“AI 辅助决策而不是替代人”的平台设计

### 适合你们移植什么

- 风险可靠性分层
- “需人工复核”标签
- 预测结果的置信度表达
- 告警处理闭环

### 对你们的直接价值

你们当前已有：

- 风险等级
- 专家规则
- 告警历史

最缺的是：

- 哪些告警更可信
- 哪些告警需要人工确认

这正是这个方向最值得借的部分。

### 适配结论

- 可移植度：高
- 借鉴价值：很高
- 推荐方式：优先本地实现“风险可靠性分层”

## 3.3 `Predictive-Maintenance-for-Industrial-Equipment`

- 仓库：[kumaraadya/Predictive-Maintenance-for-Industrial-Equipment](https://github.com/kumaraadya/Predictive-Maintenance-for-Industrial-Equipment)
- 定位：预测性维护系统，包含模型、解释、接口和界面
- 创意点：
  - 采用 `FastAPI + Streamlit + SHAP`
  - 强调“为什么会报这个风险”
  - 结构适合做比赛项目升级版

### 适合你们移植什么

- SHAP 特征解释页
- 模型接口化思路
- “特征贡献排行榜” 卡片

### 适配结论

- 可移植度：高
- 借鉴价值：很高
- 推荐方式：第二阶段优先引入 SHAP 解释能力

## 3.4 `AQI-Anomaly-Detection-and-Prediction-System`

- 仓库：[devinxhacker/AQI-Anomaly-Detection-and-Prediction-System](https://github.com/devinxhacker/aqi-anomaly-detection-and-prediction-system)
- 定位：空气质量异常检测与预测平台
- 创意点：
  - 历史异常追踪做得清晰
  - 结果展示更偏产品化
  - 有较强的“运营平台”感觉

### 适合你们移植什么

- 告警历史浏览器
- 风险等级筛选
- 可导出的汇总结果页

### 适配结论

- 可移植度：高
- 借鉴价值：高
- 推荐方式：增强你们现有“告警记录追踪”页

## 3.5 `predictive-maintenance-system`

- 仓库：[Dhanush-1213/predictive-maintenance-system](https://github.com/Dhanush-1213/predictive-maintenance-system)
- 定位：前后端分离的预测性维护系统
- 创意点：
  - `FastAPI + React` 结构清晰
  - 更接近正式产品形态

### 适合你们移植什么

- API 层组织方式
- 前后端分离的架构思路
- 如果后面打磨成作品集或长期项目，可以作为升级路线

### 适配结论

- 可移植度：中
- 借鉴价值：中高
- 推荐方式：比赛当前阶段只借架构，不建议立即重构

## 4. 建议直接接入你们项目的功能

## 4.1 风险可靠性分层

参考来源：

- `anomaly-detection-system`

适配原因：

- 你们已经有 `pred_value`、`abs_error`、阈值和专家规则
- 可以直接在现有推理服务中增加：
  - `高可靠`
  - `中等可靠`
  - `需人工复核`
  - `稳定`

当前状态：

- 本项目已接入第一版“风险可靠性分层”
- 已在推理服务中返回 `reliability` 字段
- 已在平台增强页展示“结果可靠性”和“人工复核”提示

## 4.2 SHAP 解释页

参考来源：

- `Predictive-Maintenance-for-Industrial-Equipment`

适配原因：

- 评委最容易问“为什么这个时刻判断为危险”
- SHAP 能把 `a1-a5` 转成“本次风险主要受哪些变量影响”

建议实现形式：

- 新增 `模型解释` 或 `解释中心` 页面
- 针对 `y1 / y2` 输出：
  - Top 3 贡献变量
  - 正向推高风险的变量
  - 负向拉低风险的变量

## 4.3 告警历史浏览器

参考来源：

- `AQI-Anomaly-Detection-and-Prediction-System`

适配原因：

- 你们已有 `alert_history.csv`
- 已有基础的查询能力
- 只差更好的展示层

建议增强：

- 增加“已处理 / 未处理”筛选
- 增加“需人工复核”筛选
- 增加“按指标/风险等级/时间段”筛选

## 4.4 SRU 流程示意图首页

参考来源：

- `energy-sandbox`

适配原因：

- 当前评委最大理解障碍不是模型，而是不理解 SRU 场景
- 如果首页先用一张流程示意图解释 `MEA -> 配风 -> 尾气指标`
  再看告警，会更容易建立直觉

建议实现：

- 首页放一张简化 SRU 工艺示意图
- 用大众语言标注：
  - 输入负荷
  - 配风调节
  - 尾气质量
  - 风险提示

## 5. 当前不建议直接移植的内容

- Databricks 全生态依赖
- 重型工业 SCADA / PLC / IoT 接口
- 全量 React/Next.js 前端重构
- 云端大模型编排平台

原因很简单：

- 比赛周期有限
- 你们当前已经有一套可运行平台
- 现在最重要的是“做强解释和展示”，不是重造底座

## 6. 最优实施顺序

建议按下面顺序推进：

1. 继续完善“风险可靠性分层”
2. 引入 SHAP 特征贡献解释
3. 优化告警历史页和人工复核流程
4. 制作 SRU 首页流程示意图
5. 如有时间，再考虑 API 化或前后端分离升级

## 7. 最终建议

### 现在就做

- 保留当前 Streamlit 平台
- 把 GitHub 项目中的“解释、可靠性、叙事”能力接进来

### 下一阶段重点

- SHAP 解释
- 可靠性标注
- 工艺示意图首页

### 不建议现在做

- 整仓迁移
- 全架构重写
- 追求“工程最复杂”，而牺牲答辩可解释性

## 8. 参考链接

- [databricks-industry-solutions/energy-sandbox](https://github.com/databricks-industry-solutions/energy-sandbox)
- [Kyulim-Kim/anomaly-detection-system](https://github.com/Kyulim-Kim/anomaly-detection-system)
- [kumaraadya/Predictive-Maintenance-for-Industrial-Equipment](https://github.com/kumaraadya/Predictive-Maintenance-for-Industrial-Equipment)
- [devinxhacker/AQI-Anomaly-Detection-and-Prediction-System](https://github.com/devinxhacker/aqi-anomaly-detection-and-prediction-system)
- [Dhanush-1213/predictive-maintenance-system](https://github.com/Dhanush-1213/predictive-maintenance-system)
