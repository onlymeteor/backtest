from account import Account
from data import Data


def prepare_account(strategy):
    # 如果策略没有配置账户，设置一个默认的回测账户
    if strategy.account is None:
        strategy.account = Account(data=Data())

    return strategy.account


def backtest(strategy, start, end, benchmark='399300.SZ'):
    # 配置回测账户
    account = prepare_account(strategy)

    # 通过数据对象获取交易日数据，轮询执行交易
    dates = account.data.get_dates(start, end)
    for date in dates:
        # 更新当天持仓信息
        account.update(date)
        # 策略产生当天的交易信号，并在内部执行
        strategy.run(date)
        # 交易日结束，记录净值
        account.write_record()
        # print(f'debug - {date} : 持仓{len(account._holdings)}只')

    # 回测结束，返回报告
    return account.create_report(benchmark)
