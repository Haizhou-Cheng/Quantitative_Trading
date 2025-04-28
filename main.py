import json
import requests
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from datetime import datetime, timedelta
from matplotlib.dates import DateFormatter, HourLocator

# 设置字体为支持中文的字体
rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 或者使用其他支持中文的字体，如 SimHei
rcParams['axes.unicode_minus'] = False

# 配置参数
name_map = {
    #"HK:700": "腾讯控股",
    #"SH:600519": "贵州茅台",
    "SZ:002594": "比亚迪"
}

api_url = "https://api.qos.hk/snapshot?key=b3053f8ec33f11a965f60555a7b9bc59"
update_interval = 30  # 秒

# 初始化数据存储
history_data = {
    code: {'timestamps': [], 'prices': [], 'volumes': [], 'amounts': []}
    for code in name_map
}

def fetch_data():
    """获取最新行情数据"""
    payload = json.dumps({"codes": list(name_map.keys())})
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(api_url, headers=headers, data=payload)
        return response.json()["data"]
    except Exception as e:
        print(f"数据获取失败：{str(e)}")
        return None
    




    

class Strategy:
    def __init__(self, short_window=5, long_window=20):
        self.short_window = short_window
        self.long_window = long_window
        self.position = 0  # 持仓状态
    
    def generate_signal(self, data):
        data['short_ma'] = data['prices'].rolling(self.short_window).mean()
        data['long_ma'] = data['prices'].rolling(self.long_window).mean()
        
        # 金叉买入，死叉卖出
        if data['short_ma'].iloc[-1] > data['long_ma'].iloc[-1]:
            return 'BUY'
        elif data['short_ma'].iloc[-1] < data['long_ma'].iloc[-1]:
            return 'SELL'
        else:
            return 'HOLD'
        




    

def update_chart():
    """更新图表"""
    for ax in [ax1, ax2, ax3]:
        ax.clear()
    
    for code in name_map:
        timestamps = [datetime.fromtimestamp(ts) for ts in history_data[code]['timestamps']]
        
        # 价格走势（折线图）
        ax1.plot(timestamps, history_data[code]['prices'], 
                marker='o', label=name_map[code])
        
        # 成交量（柱状图）
        ax2.bar(timestamps, history_data[code]['volumes'],
               width=0.02, alpha=0.5, label=name_map[code])
        
        # 成交额（折线图）
        ax3.plot(timestamps, history_data[code]['amounts'],
                linestyle='--', label=name_map[code])

    # 设置坐标轴格式
    time_format = DateFormatter("%H:%M")
    for ax in [ax1, ax2, ax3]:
        ax.xaxis.set_major_formatter(time_format)
        ax.xaxis.set_major_locator(HourLocator())  # 设置X轴主刻度为每小时
        ax.grid(True)
        ax.legend()

    ax1.set_ylabel('Price (Yuan)')
    ax2.set_ylabel('Volume (in lots)')
    ax3.set_ylabel('Transaction Amount (in ten thousand yuan)')
    
    plt.tight_layout()  # 自动调整布局
    plt.draw()  # 更新绘图
    plt.pause(0.1)


    

def main():
    """主运行循环"""
    strategy = Strategy()  # 初始化策略
    last_signal = {code: 'HOLD' for code in name_map}  # 初始化每只股票的最后信号

    while True:
        start_time = time.time()
        
        # 获取数据
        data = fetch_data()
        if data:
            for stock in data:
                code = stock["c"]
                if code in history_data:
                    # 记录当前时间戳
                    ts = datetime.now().timestamp()
                    try:
                        history_data[code]['timestamps'].append(ts)
                        history_data[code]['prices'].append(stock["lp"])
                        history_data[code]['volumes'].append(int(stock["v"]) / 100)  # 转换为手
                        history_data[code]['amounts'].append(float(stock["t"]) / 10000)  # 转换为万元
                    except KeyError as e:
                        print(f"数据解析失败：{stock}，错误：{e}")

                    # 转换数据为DataFrame
                    data_frame = pd.DataFrame(history_data[code])

                    # 生成交易信号
                    signal = strategy.generate_signal(data_frame)

                    # 如果信号变化，则更新
                    if signal != last_signal[code]:
                        last_signal[code] = signal  # 更新信号
                        print(f"股票 {name_map[code]} 当前信号：{signal}")
            update_chart()
        
        # 等待下一个周期
        elapsed = time.time() - start_time
        if elapsed < update_interval:
            time.sleep(update_interval - elapsed)



# 创建画布
plt.ion()  # 启用交互模式
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 8))
fig.suptitle('Real-time Stock Market Monitoring')

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        plt.close()
        print("监控已停止")