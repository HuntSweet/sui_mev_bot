class Config:
    # Sui RPC节点配置
    SUI_RPC_URL = "https://fullnode.mainnet.sui.io:443"
    
    # 套利参数配置
    MIN_PROFIT_THRESHOLD = 0.01  # 最小利润阈值（以USD计）
    GAS_BUFFER = 1.2            # gas预估缓冲系数
    GAS_TOKEN = "0x2::sui::SUI"
    # 交易所和交易对配置
    MONITORED_DEXS = [
        "turbos",
        "cetus",
        "deepbook"
    ]
    
    # 监控配置
    POLLING_INTERVAL = 1  # 区块监控间隔（秒） 