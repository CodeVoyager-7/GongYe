# SRU 匿名变量语义判别

## 1. 结论

当前项目使用的 OpenML `sulfur` 数据集在 CSV 中只保留了 `a1-a5/y1-y2` 这样的匿名字段。但通过追溯 SRU 软测量 benchmark 的公开论文，可以将其基本对应到文献中的 `u1-u5/y1-y2`。

整理后的映射表：

- [sru_variable_mapping.csv](C:/Users/lenovo/Desktop/人工智能大赛/data/external/sru_variable_mapping.csv)

| CSV字段 | 文献符号 | 语义 | 置信度 |
|---|---|---|---|
| `a1` | `u1` | MEA区气体流量，MEA gas flow | 高 |
| `a2` | `u2` | 第一空气流量，AIR MEA 1 | 高 |
| `a3` | `u3` | 第二空气流量，AIR MEA 2 | 高 |
| `a4` | `u4` | SWS区气体流量，Gas flow in SWS zone | 中 |
| `a5` | `u5` | SWS区空气流量，AIR SWS | 中 |
| `y1` | `y1` | 尾气H2S浓度 | 高 |
| `y2` | `y2` | 尾气SO2浓度 | 高 |

## 2. 主要依据

### 2.1 OpenML 数据集本身

OpenML `sulfur` 数据集只展示字段名为 `a1-a5/y1-y2`，没有直接给出工艺位号。项目本地说明中也记录了该数据来自 `fetch_openml`，OpenML data_id 为 `23515`。

因此，仅依靠 OpenML 页面不能确定变量物理含义，必须追溯 SRU benchmark 论文。

### 2.2 IFAC 2002 原始 SRU 软测量论文

Fortuna 等人的 `Soft Analysers for a Sulfur Recovery Unit` 说明：

- 该 SRU 来自意大利 ERG PETROLI ISAB refinery。
- 软测量目标是在线预测尾气中的 H2S 和 SO2。
- 五个输入变量由专家知识选择，包括：
  - MEA GAS
  - AIR MEA 1
  - AIR MEA 2
  - AIR SWS
  - SWS GAS

论文还说明 AIR MEA 1 和 AIR SWS 由操作员手动设定，AIR MEA 2 由自动反馈回路控制。

### 2.3 后续 SRU benchmark 文献

后续多篇 SRU 软测量论文将变量整理为：

- `u1`: MEA gas flow
- `u2`: First air flow
- `u3`: Second air flow
- `u4`: Gas flow in SWS zone
- `u5`: Air flow in SWS zone
- `y1`: H2S concentration
- `y2`: SO2 concentration

其中，2023 年的尾气质量预警论文明确写出该 benchmark 包含 `10081` 个样本，并给出 `u1-u5/y1-y2` 的输入输出表。

## 3. 为什么 a1-a5 可以对应 u1-u5

项目本地 CSV 字段是：

```text
a1, a2, a3, a4, a5, y2, y1
```

OpenML 对原始变量名做了匿名化或标准化处理。因此最合理的对应方式是：

```text
a1 -> u1
a2 -> u2
a3 -> u3
a4 -> u4
a5 -> u5
y1 -> y1
y2 -> y2
```

这个对应关系也能被数据相关性部分支持：

- `a1` 与 `a2` 的相关系数约为 `0.913`，符合 MEA气体流量与MEA区第一空气流量联动。
- `a4` 与 `a5` 的相关系数约为 `0.876`，符合 SWS区气体流量与SWS区空气流量联动。
- `y1` 与 `y2` 呈明显负相关，符合 H2S/SO2 在Claus配风控制中互相制约的工艺关系。

## 4. 需要谨慎的地方

`a4/a5` 的顺序存在文献差异：

- 一些文献表格写作 `u4 = Gas flow in SWS zone`，`u5 = Air flow in SWS zone`。
- 个别后续论文表格写作 `u4 = Air flow in SWS zone`，`u5 = Gas flow in SWS zone`。
- IFAC 原始论文列举变量时先写 AIR SWS，再写 SWS GAS，但图示编号顺序又是 AIR SWS 在 Fig.2.b，SWS GAS 在 Fig.2.e。

因此，当前项目中建议将：

```text
a4/a5 = SWS区气量与空气量这一对变量
```

作为稳妥表述；如果需要单独解释，则采用多数后续建模表格和数据相关性支持的版本：

```text
a4 = SWS区气体流量
a5 = SWS区空气流量
```

## 5. 对当前项目的影响

### 5.1 模型解释

后续图表和答辩中，可以不再只说 `a1-a5`，而是写成：

- `a1 / MEA gas flow`
- `a2 / AIR MEA 1`
- `a3 / AIR MEA 2`
- `a4 / SWS gas flow`
- `a5 / AIR SWS`
- `y1 / H2S concentration`
- `y2 / SO2 concentration`

### 5.2 专家知识库

专家知识库中的 `related_dataset_variable` 可以基于该映射进一步优化：

- 与配风相关的规则优先关联 `a2/a3/a5`
- 与酸气负荷相关的规则优先关联 `a1/a4`
- `y1` 明确解释为 H2S 风险
- `y2` 明确解释为 SO2 风险

当前已据此重新制定专家规则：

- `y1/H2S` 高风险：优先解释为欠配风、MEA/SWS负荷增加、COS/CS2水解不足或催化剂转化效率异常。
- `y2/SO2` 高风险：优先解释为过量配风、SWS支路配风偏高、尾气处理负荷上升或分析仪/控制回路异常。
- 通用规则：处理 H2S/SO2 比值偏离、分析仪漂移和 SWS 支路扰动。

### 5.3 答辩表述

推荐表述：

> OpenML 版本保留了 `a1-a5/y1-y2` 的匿名字段。我们进一步追溯 SRU 软测量 benchmark 文献，将其对应到 `u1-u5/y1-y2`：输入变量主要为 MEA 区气体流量、MEA 区空气流量、SWS 区气体流量和SWS区空气流量，输出变量为尾气 H2S 和 SO2 浓度。其中 `a4/a5` 在不同文献中存在顺序差异，因此项目中将其作为 SWS 区气量和空气量这一组变量进行解释，并在后续真实装置接入时通过位号表确认。

## 6. 参考资料

- OpenML sulfur dataset: https://www.openml.org/search?id=23515&type=data
- Fortuna et al., Soft Analysers for a Sulfur Recovery Unit: https://skoge.folk.ntnu.no/prost/proceedings/ifac2002/data/content/01320/1320.pdf
- Tail Gas Quality Warning System in a Sulfur Recovery Unit: https://ieco.usb.ac.ir/article_8028_02da131feb3de193c57c509eced540b6.pdf
- Fast Tunable Gradient RBF Networks for Online Modeling: https://eprints.soton.ac.uk/443130/1/TGRBF_JPC_re1.pdf
