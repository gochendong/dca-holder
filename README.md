<div align="center">
<h1> DCA Holder </h1>

这是一个融合了平均成本法与长期持有策略的加密量化策略, 在主流交易所**币安/欧易/Bitget**上实现, 其思想同样适用于其他核心资产, 如纳指, 黄金等

Github: [https://github.com/gochendong/dca-holder](https://github.com/gochendong/bulita)

所有代码均有实盘资金7*24小时测试, 非demo级别, 请放心使用

币安实盘展示: https://www.binance.com/zh-CN/copy-trading/lead-details/4467924166879352065

商务合作请联系[布里塔](https://chat.bulita.net)

</div>

## 特点

1. **100%开源**, 只需要填写API即可开启自动化交易, 目前支持币安/欧易/Bitget, 只支持现货BTC/USDT, 支持多账户
2. **核心思想**是平均成本与屯币, 如果价格上涨, 将在固定盈利点卖出, 并将盈利进行永久屯币, 如果价格下跌, 将不断补仓, 拉低成本
3. 闲置的USDT可选择自动划转到理财账户享受借贷利润

## 使用

1. 填写配置文件.env.example, 并将其重命名为.env
   ```
   cp .env.example .env
   ```
2. 确保已运行redis服务
   ```
   docker-compose -f docker-compose-redis.yaml up -d
   ```
3. 安装依赖 
    ```
    python3 -m pip install -r requirements.txt 
    ```
4. 运行程序
    ```
    python3 main.py
    ```
   程序会自动读取配置文件并开始运行, 可以使用screen/nohup/supervisor等方式实现进程守护

## 注意事项
1. 程序初始时, 请保证你的现货账户中不持有任何BTC, 并且现货或理财账户中拥有足够的USDT
2. 程序运行后, 不要手动交易BTC(手动加减仓需停止程序, 并修改redis中dca:xxx:BTC:long:cost对应的值), 充提USDT, 交易其他币种或重启程序不影响策略

## 交易哲学
>**Q:** 为什么不直接持有BTC?
> 
>**A:** 交易是反人性的

>**Q:** 为什么不定投BTC?
> 
>**A:** 会买的是徒弟, 会卖的是师父

>**Q:** 为什么不将份数调小从而扩大仓位
>
>**A:** 盈亏同源

## 参考文献

[https://github.com/ccxt/ccxt](https://github.com/ccxt/ccxt)

[https://binance-docs.github.io/apidocs/spot/cn](https://binance-docs.github.io/apidocs/spot/cn)

[https://www.okx.com/docs-v5/zh/](https://www.okx.com/docs-v5/zh/)

[https://www.bitget.com/zh-CN/api-doc/spot/intro](https://www.bitget.com/zh-CN/api-doc/spot/intro)

## License

[MIT licensed](./LICENSE)

## 赞助本项目

![](https://docs.bulita.net/media/202412/usdt_1733018911.png)