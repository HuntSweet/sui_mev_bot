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

[![](https://mermaid.ink/img/pako:eNp9U99v0kAc_1ea7kWTw6Ttk30wGXRQ3kzmk1ceCr2ORmhJf0SXZYkzRpnZhAU31C1ubrCpycaWGIeA-M_0ruy_sPRY6CThHpq7-3w-38-n37tbYwuWhliRXbHVSpF5IikmEw7Hy9MNhSW7l2T7ItjfIe_PFJbC47HIwZvG0O--83st8rFBCTkmkXjEJCHdG_19S_ot_OlbLibj4XLRsJg0QtqETUFkaoo54z667uDh6-DDIanW4-7JSJqCpFbHtT1ca-I_V7ixTa6O8Hk9ZpeKeBKkdchhm2wO7waSkvAe_Ufca9ynkaQYHG0sQdxu4up3WiY3L3FwvhfstnH1DflyJ_FSVCjNQb_bojEpMzdD4SE57uDeKakfBD-PZ1hpLqJlJpHIQc8ffI7jPMXnhaTnQzbPRl-34iEzkVTmYEZ1_MFlcNGMFZapsRzm6-8Er36Tk5dhQ-ME6iwLcJzr1-nNj61RZyNOECJCFlJnmmJuN_3-NTkazN6-x9Dvn-DuBsXDW-AP98fnyiQeRAmmzCw90dlbViipjiMhnanYRlm1VxndKJXEBf2hDhzXtp4hcUEQhMk88dzQ3KLIV178J3ZQwTK1qTyfnyPn7sjDJwQWeSCBDMjehojDSZACaQ6keSBzQA6_wtSNBWwZ2WXV0MK3uzZWKaxbRGWksGI41ZCueiV33LH1kKp6rrW8ahZY0bU9BFjb8laKrKirJSdceRVNdZFkqGHTy7eUimo-tazJcv0fU7SWrw?type=png)](https://mermaid-js.github.io/mermaid-live-editor/edit#pako:eNp9U99v0kAc_1ea7kWTw6Ttk30wGXRQ3kzmk1ceCr2ORmhJf0SXZYkzRpnZhAU31C1ubrCpycaWGIeA-M_0ruy_sPRY6CThHpq7-3w-38-n37tbYwuWhliRXbHVSpF5IikmEw7Hy9MNhSW7l2T7ItjfIe_PFJbC47HIwZvG0O--83st8rFBCTkmkXjEJCHdG_19S_ot_OlbLibj4XLRsJg0QtqETUFkaoo54z667uDh6-DDIanW4-7JSJqCpFbHtT1ca-I_V7ixTa6O8Hk9ZpeKeBKkdchhm2wO7waSkvAe_Ufca9ynkaQYHG0sQdxu4up3WiY3L3FwvhfstnH1DflyJ_FSVCjNQb_bojEpMzdD4SE57uDeKakfBD-PZ1hpLqJlJpHIQc8ffI7jPMXnhaTnQzbPRl-34iEzkVTmYEZ1_MFlcNGMFZapsRzm6-8Er36Tk5dhQ-ME6iwLcJzr1-nNj61RZyNOECJCFlJnmmJuN_3-NTkazN6-x9Dvn-DuBsXDW-AP98fnyiQeRAmmzCw90dlbViipjiMhnanYRlm1VxndKJXEBf2hDhzXtp4hcUEQhMk88dzQ3KLIV178J3ZQwTK1qTyfnyPn7sjDJwQWeSCBDMjehojDSZACaQ6keSBzQA6_wtSNBWwZ2WXV0MK3uzZWKaxbRGWksGI41ZCueiV33LH1kKp6rrW8ahZY0bU9BFjb8laKrKirJSdceRVNdZFkqGHTy7eUimo-tazJcv0fU7SWrw)


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

### 使用 pip

如果不使用 Poetry，也可以直接使用 pip：

```bash
pip install pysui websockets python-dotenv scipy numpy aiohttp pytest pytest-asyncio
```

## 使用方法

启动机器人

```