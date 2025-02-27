# DEX Arbitrage Bot

一个基于 Sui 网络的 DEX 套利机器人框架，支持多种套利策略和数据源。



## 项目状态 

❗️ ****当前开发阶段****   

本项目为开发框架，仅包含以下模块：

- 项目结构搭建 
- 基础类定义 
- 接口设计
- 部分模块实现
- 运行主逻辑

❌ ****尚未实现****   

- 完整业务逻辑 

- 数据持久化 

- 完整测试用例

  

## 功能特点

- **多数据源支持**
  - Sui 链上交易监控
  - Shio Feed 实时数据
  - 支持自定义数据源扩展
  - 支持自定义数据筛选扩展

- **灵活的套利策略**
  - 两池子套利（基于解析解）（适用于FlowX Swap AMM与 Kriya 1等Dex）
  - 多池子套利（基于梯度搜索）
  - 支持添加自定义策略

- **智能路径搜索**
  - 支持自定义路径
  - 基于受影响池子的动态路径搜索
  - 流动性和代币黑名单过滤
  - 可配置最大路径长度

- **风险控制**
  - 最小利润阈值
  - Gas 成本估算
  - 代币价格实时监控

## 项目结构

```text
src/
├── analysis/      # 分析交易模块
├── common/        # 通用工具
├── db/            # 数据库
├── execution/     # 交易执行
├── monitor/       # 数据监控
├── path/          # 路径搜索
├── strategy/      # 套利策略
└── token_price/   # 代币价格
```



## 流程图

[![](https://mermaid.ink/img/pako:eNp9VF1P01AY_itNudHkzKTdlb0woSvduFuCV57uoltPWePWLv2IEsIFCVEw4GYWmApBxA3UBAaJkWWb88_0nI1_YdszWOd0vTp93-fjPc857TpbsDTECuyqrVaKzFNJMZngcbw8LSgs2b8ie5fDw3fk7bnC0nb4LHLwtj7wO2_8bpO8r1NAjkkknjAipLXR79ek18QfvuZiNB6uFA2LkRHSxuhJU4wKKUiqNVw9wNUG_nWN63vk-gRf1MYiyNQU8z9T4m49PqIkwgf3jYexIVKRjyTOUxzdtPFgixxv4V53WpSS4RjwqUV2BtN7lCLEEsStBt7-RnFzpx9eHAz3W3j7FTmuxb2WIiGZg36nSUOgyNwMhIfktI27Z6R2NPxxOoMKh34USf2jxk9qMhfJpcejk6Ou3_8Y05F52p-3GXr2ZOd89Hk3vpl0RM1wMK06fv9qeNmICWeocYaHoe3Ps9vvu6P2ZhxAnZchFaYmc0P1ezfkpD97cbPQ733BnU3aD66aPzgMz4-mkYmlkZ0NLTudWcy5UFIdR0I6U7GNsmqvMbpRKgkL-mMdOK5tPUfCQjKZHK8TLwzNLQp85eVfZAcVLFOb0PP5OXRuih58kWCRB5II0mD5bop4XwQpIAGZAzIPMhwIEr13YwFbRnZZNbTgV7AekhTWLaIyUlghWGpIV72SG6a4EUBVz7VW1swCK7i2hwBrW95qkRV0teQEb15FU10kGWpwEOU7SEU1n1nW-HXjDybqp6I?type=png)](https://mermaid-js.github.io/mermaid-live-editor/edit#pako:eNp9VF1P01AY_itNudHkzKTdlb0woSvduFuCV57uoltPWePWLv2IEsIFCVEw4GYWmApBxA3UBAaJkWWb88_0nI1_YdszWOd0vTp93-fjPc857TpbsDTECuyqrVaKzFNJMZngcbw8LSgs2b8ie5fDw3fk7bnC0nb4LHLwtj7wO2_8bpO8r1NAjkkknjAipLXR79ek18QfvuZiNB6uFA2LkRHSxuhJU4wKKUiqNVw9wNUG_nWN63vk-gRf1MYiyNQU8z9T4m49PqIkwgf3jYexIVKRjyTOUxzdtPFgixxv4V53WpSS4RjwqUV2BtN7lCLEEsStBt7-RnFzpx9eHAz3W3j7FTmuxb2WIiGZg36nSUOgyNwMhIfktI27Z6R2NPxxOoMKh34USf2jxk9qMhfJpcejk6Ou3_8Y05F52p-3GXr2ZOd89Hk3vpl0RM1wMK06fv9qeNmICWeocYaHoe3Ps9vvu6P2ZhxAnZchFaYmc0P1ezfkpD97cbPQ733BnU3aD66aPzgMz4-mkYmlkZ0NLTudWcy5UFIdR0I6U7GNsmqvMbpRKgkL-mMdOK5tPUfCQjKZHK8TLwzNLQp85eVfZAcVLFOb0PP5OXRuih58kWCRB5II0mD5bop4XwQpIAGZAzIPMhwIEr13YwFbRnZZNbTgV7AekhTWLaIyUlghWGpIV72SG6a4EUBVz7VW1swCK7i2hwBrW95qkRV0teQEb15FU10kGWpwEOU7SEU1n1nW-HXjDybqp6I)


## 开发指南

1. 添加新的数据源
   - 继承 `Monitor` 类
   - 实现 `monitor_transactions` 方法
2. 添加新的过滤策略
   - 继承 `TransactionFilter` 类
   - 实现 `filter` 方法
3. 添加新的套利策略
   - 继承 `Strategy` 类
   - 实现 `find_arbitrage_opportunity` 方法



## 环境要求

- Python 3.8+
- pip 20.0+

## 安装指南

1. **创建并激活虚拟环境**

```bash
# 使用 venv
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

2. **安装依赖**

```bash
# 使用 requirements.txt
pip install -r requirements.txt

# 或者使用 poetry（推荐）
poetry install
```


## 依赖管理

项目使用 Poetry 进行依赖管理，主要依赖包括：

```toml
[tool.poetry.dependencies]
python = "^3.8"
websockets = ">=10.0,<13.0"  # 与pysui兼容的版本
python-dotenv = "^1.0.0"
pysui = "0.79.0" 
scipy = "^1.9.0"
numpy = "^1.21.0"
aiohttp = "^3.8.0"
pytest = "^7.0.0"
pytest-asyncio = "^0.18.0"
```

### 使用 Poetry

1. **安装 Poetry**
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. **安装项目依赖**
```bash
poetry install
```

3. **添加新依赖**
```bash
poetry add package-name
```

4. **更新依赖**
```bash
poetry update
```

5. **导出 requirements.txt**
```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

