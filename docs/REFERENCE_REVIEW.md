# 开源对照与升级决策

核查日期：**2026-10-28**。Star 数是当日仓库页面的观察值，会变化，不代表实现正确性或金融收益。原始 GitHub API 返回限流，因此使用仓库公开页面的 `stargazerCount` 与 `currentOid`；结构化记录见 [reference-snapshot.json](reference-snapshot.json)。

## 实际阅读的项目与资料

| 参考 | 当日 Star | 阅读依据 | 采纳与取舍 |
|---|---:|---|---|
| [TradingAgents](https://github.com/TauricResearch/TradingAgents) | 117,542 | README；下列固定版本的结构化调用与 schema 源码 | 保留分析／风险／判断分工；升级原生 JSON Schema、数字与单位校验；本项目模型失败仍弃权，不照搬自由文本降级 |
| [LangGraph](https://github.com/langchain-ai/langgraph) | 44,030 | README、官方 persistence 文档 | 明确状态与持久化边界，补运行输入摘要、角色轨迹和报告校验；当前流程不需要长时恢复，暂不增加图调度依赖 |
| [Promptfoo](https://github.com/promptfoo/promptfoo) | 26,533 | README；下列固定版本的断言文档 | 借鉴可重复案例、确定性断言和变体对照；实现独立的离线压力评测，不引入 Node 运行依赖 |
| [Polymarket Agents](https://github.com/Polymarket/agents) | 3,804 | README 的 API／connector／模型分层 | 保持平台适配器与判断逻辑分离，补 YES token 与交易所历史序列；不引入钱包或下单能力 |
| [旧 py-clob-client](https://github.com/Polymarket/py-clob-client) | 1,223 | README 的 archived／not functional 声明 | **不采用**。官方要求迁往 [py-sdk](https://github.com/Polymarket/py-sdk)，而本题的少量只读接口继续使用轻量 REST |

固定版本资料：

- TradingAgents [`structured.py`](https://github.com/TauricResearch/TradingAgents/blob/c4544913a14ed3df5f1ed7b9e8483270ce20682a/tradingagents/agents/structured.py) 与 [`schemas.py`](https://github.com/TauricResearch/TradingAgents/blob/c4544913a14ed3df5f1ed7b9e8483270ce20682a/tradingagents/agents/schemas.py)：原生结构化输出、类型化决策、确定性渲染及降级策略。
- Promptfoo [expected outputs 文档](https://github.com/promptfoo/promptfoo/blob/e48ed85e08ff8a1ca74fa7d0e41daf47cf155efb/site/docs/configuration/expected-outputs/index.md)：程序化 JSON、数值、延迟与自定义断言；本项目只借鉴评测方法，未执行 Promptfoo。
- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence)：checkpoint 与 store 是不同能力。当前项目的 JSONL 轨迹**不是**可恢复的 LangGraph checkpoint。
- [Polymarket price history](https://docs.polymarket.com/developers/CLOB/timeseries)：`market` 是资产／token ID，`fidelity` 以分钟表示。
- [Kalshi candlesticks](https://docs.kalshi.com/api-reference/market/get-market-candlesticks)：区分 YES 报价 OHLC、成交价 OHLC 与该 K 线内成交合约量。

## 对现版的判断

初版已经覆盖招聘题目的功能，但若作为 AI 研究工程师作品，三个缺口值得补：

1. 单轮真实快照无法体现概率追踪。升级增加两家平台的原生历史读取与离线重放；保存 `event_time` 和 `received_at`，不创建虚假的历史市场快照。
2. 单元测试无法说明检测规则的取舍。升级增加 12 类、288 个合成案例和四种消融设置，报告混淆矩阵、误报、漏报、风险越权及失败案例。
3. 引用 ID 存在不代表引用正确。升级对结构化 `claims` 校验值、符号和单位；模型结构化输出采用原生 JSON Schema，可显式切换兼容模式。

另外增加 TOML 配置、代码／输入哈希、角色轨迹和报告完整性校验，使实验与提交更可核对。

## 没有增加的部分

本题允许简单的 prompt + 结构化输出。当前线性流程无需为了框架名称增加 LangGraph、向量数据库、消息队列或多轮辩论。没有外部新闻数据和标注集时，也不包装成金融 RAG 或完整自主投研系统。

本轮改动使作品更接近成熟项目的工程与评测习惯；它仍是研究原型。真实历史回填不等同于真实检测评测，合成留出集也不等于真实市场外部验证。
