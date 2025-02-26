# DEX Arbitrage Bot

一个基于 Sui 网络的 DEX 套利机器人框架，支持多种套利策略和数据源。



## 项目状态 

❗️ ***\*当前开发阶段\****   

本项目为初期开发框架，仅包含以下基础模块：

- 项目结构搭建 
- 基础类定义 
- 接口设计 
- 运行主逻辑

❌ ***\*尚未实现\****   

- 核心业务逻辑 

- 数据持久化 

- 异常处理 

-  完整测试用例

  

## 功能特点

- **多数据源支持**
  - Sui 链上交易监控
  - Shio Feed 实时数据
  - 支持自定义数据源扩展

- **灵活的套利策略**
  - 两池子套利（基于解析解）
  - 多池子套利（基于梯度搜索）
  - 支持添加自定义策略

- **智能路径搜索**
  - 支持自定义路径
  - 基于受影响池子的动态路径搜索
  - 流动性和代币黑名单过滤
  - 可配置最大路径长度

- **风险控制**
  - 滑点控制
  - 最小利润阈值
  - Gas 成本估算
  - 代币价格实时监控

## 项目结构

```text
src/
├── analysis/       # 分析交易模块
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

## 使用方法

启动机器人

```
python main.py
```

## 开发指南

1. 添加新的数据源
   - 继承 `Monitor` 类
   - 实现 `monitor_transactions` 方法
2. 添加新的套利策略
   - 继承 `Strategy` 类
   - 实现 `find_arbitrage_opportunity` 方法

## 测试

运行测试：

```
pytest tests/ -v
```

## 许可证

MIT License - 查看 LICENSE 文件了解详情

## 免责声明

本项目仅供学习和研究使用，作者不对使用本项目造成的任何损失负责。在使用本项目进行实际交易之前，请充分了解相关风险。