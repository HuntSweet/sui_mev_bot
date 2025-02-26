# DEX Arbitrage Bot

一个基于 Sui 网络的 DEX 套利机器人，支持多种套利策略和数据源。

## 功能特点

- 多数据源支持
  - Sui 链上交易监控
  - Shio Feed 实时数据
  - 支持自定义数据源扩展

- 灵活的套利策略
  - 两池子套利（基于解析解）
  - 多池子套利（基于梯度搜索）
  - 支持添加自定义策略

- 实时价格监控
  - 支持多个 DEX
  - 实时流动性分析
  - 价格影响评估

- 风险控制
  - 滑点控制
  - 最小利润阈值
  - Gas 成本估算

## 项目结构 
src/
├── analysis/ # 分析模块
├── common/ # 通用工具
├── execution/ # 交易执行
├── monitor/ # 数据监控
├── strategy/ # 套利策略
└── token_price/ # 代币价格

## 安装

1. 克隆项目

## 开发指南

1. 添加新的数据源
- 继承 `Monitor` 类
- 实现 `monitor_transactions` 方法

2. 添加新的套利策略
- 继承 `Strategy` 类
- 实现 `find_arbitrage_opportunity` 方法

3. 添加新的 DEX 支持
- 在 `config.py` 中添加 DEX 配置
- 实现相应的接口适配器

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交改动 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

MIT License - 查看 [LICENSE](LICENSE) 文件了解详情

## 免责声明

本项目仅供学习和研究使用，作者不对使用本项目造成的任何损失负责。在使用本项目进行实际交易之前，请充分了解相关风险。