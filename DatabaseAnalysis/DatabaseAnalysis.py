# -*- encoding:utf-8-*-

import sqlite3

def RetManager(fetchone):
    if fetchone[0]:
        return fetchone[0]
    else:
        return 0

date = None
path = None
data = None

cash_container_type = {1: '回收箱', 2: '循环鼓', 6: '暂存'}

print('请输入路径或者日期，输入q退出')
while(True):
    shuru = input()
    if shuru == 'q':
        if data:
            data.close()
        exit()
    elif shuru.isalnum() and not path:
        print("请输入路径")
        date = shuru
        continue
    elif not shuru.isalnum() and not date:
        print("请输入日期")
        path = shuru
        continue
    elif shuru.isalnum() and path:
        date = shuru
        if data:
            data.close()
        data = sqlite3.connect(path + "\\sledb.db")
    elif not shuru.isalnum() and date:
        path = shuru
        if data:
            data.close()
        data = sqlite3.connect(path + "\\sledb.db")

    print('---------------------------------------------------------------------------------------------------')
    print(date+'对账详情:')
    current = data.cursor()

    '''当天应收总金额'''
    result = current.execute("select sum(transaction_value) from trans_info_incoming where busi_date=" + date)
    CashAmount = RetManager(result.fetchone())
    print('当天应收:' + str(CashAmount/100) + '元')

    print('------------纸币------------')
    '''纸币接收情况'''
    billAccept = {1: 0, 6: 0}
    result = current.execute(
        "select t.DESTINATION_CASH_CONTAINER_TYPE , sum(t.OPER_COUNT * t.DENOMINATION_TYPE) / 100 as billAccept from trans_info_of_cash_flow t where t.ACTION_TYPE=4 and t.CASH_TYPE=2 and t.DESTINATION_CASH_CONTAINER_TYPE in (1,6) and t.BUSI_DATE= \'%s\' group by t.DESTINATION_CASH_CONTAINER_TYPE" % date)
    detail = result.fetchall()
    for container in detail:
        if container[1]:
            billAccept[container[0]] = container[1]
            print('纸币接收到' + cash_container_type[container[0]] + ' : ' + str(container[1]) + '元')

    '''纸币循环鼓接收情况'''
    billLoopAccept = {1: 0, 2: 0, 3: 0, 4: 0}
    billLoopAcceptAmount = 0
    result = current.execute("select t.DESTINATION_CASH_BOX_NO ,sum(t.OPER_COUNT * t.DENOMINATION_TYPE)/100 as billAccept from trans_info_of_cash_flow t where t.ACTION_TYPE=4 and t.CASH_TYPE=2 and t.DESTINATION_CASH_CONTAINER_TYPE = 2 and t.DESTINATION_CASH_BOX_NO in (1,2,3,4) and t.BUSI_DATE='%s' group by t.DESTINATION_CASH_BOX_NO" % date)
    detail = result.fetchall()
    for boxno in detail:
        if boxno[1]:
            billLoopAccept[boxno[0]] = boxno[1]
            billLoopAcceptAmount += boxno[1]
            print('纸币接收到循环鼓%d : %d元' % (boxno[0], boxno[1]))

    '''纸币找零'''
    billLoopChange = {1: 0, 2: 0, 3: 0, 4: 0}
    billLoopChangeAmount = 0
    result = current.execute("select t.ORIGIN_CASH_BOX_NO,sum(t.OPER_COUNT * t.DENOMINATION_TYPE)/100 from trans_info_of_cash_flow t where  Action_type=5 and cash_type=2 and t.ORIGIN_CASH_BOX_NO in (1,2,3,4) and busi_date='%s' group by t.ORIGIN_CASH_BOX_NO" % date)
    detail = result.fetchall()
    for boxno in detail:
        if boxno[1]:
            billLoopChange[boxno[0]] = boxno[1]
            billLoopChangeAmount += boxno[1]
            print('纸币循环鼓%d找零 : %d元' % (boxno[0], boxno[1]))


    '''纸币补充箱补充'''
    result = current.execute("select abs(sum(TOTAL_AMOUNT_BEFORE_CHANGE - TOTAL_AMOUNT_AFTER_CHANGE)) / 100 from BOX_CHANGE_INFO_CASH where operation_type=1 and cash_type=2 and cash_container_type = 4 and busi_date =" + date)
    billSupplyBoxSet = RetManager(result.fetchone())
    print('纸币补充总金额 ： ' + str(billSupplyBoxSet) + '元')

    '''纸币补充到回收箱的金额'''
    result = current.execute("select abs(sum(TOTAL_AMOUNT_BEFORE_CHANGE - TOTAL_AMOUNT_AFTER_CHANGE)) / 100 from BOX_CHANGE_INFO_CASH where operation_type=3 and cash_type=2 and cash_container_type = 1 and busi_date =" + date)
    billSupplyToRecycle = RetManager(result.fetchone())
    if billSupplyToRecycle:
        print('纸币补充到回收箱 ： ' + str(billSupplyBoxSet) + '元')

    '''纸币补充到循环鼓'''
    billSupplyToLoop = {1: 0, 2: 0, 3: 0, 4: 0}
    billSupplyToLoopAmount = 0
    result = current.execute("select box_no , abs(sum(TOTAL_AMOUNT_BEFORE_CHANGE - TOTAL_AMOUNT_AFTER_CHANGE)) / 100 from BOX_CHANGE_INFO_CASH where operation_type=3 and cash_type=2 and cash_container_type = 2 and busi_date = '%s' group by box_no" % date)
    detail = result.fetchall()
    for boxno in detail:
        billSupplyToLoop[boxno[0]] = boxno[1]
        billSupplyToLoopAmount += boxno[1]
        if boxno[1]:
            print('纸币补充到循环鼓%d ： %d元' % (boxno[0], boxno[1]))


    '''纸币补充箱清空'''
    result = current.execute("select abs(sum(TOTAL_AMOUNT_BEFORE_CHANGE - TOTAL_AMOUNT_AFTER_CHANGE)) / 100 from BOX_CHANGE_INFO_CASH where operation_type=4 and cash_type=2 and cash_container_type = 4 and busi_date =" + date)
    billSupplyBoxClear = RetManager(result.fetchone())
    print('纸币补充箱清空 ： ' + str(billSupplyBoxClear) + '元')

    '''纸币循环鼓清空'''
    billLoopClear = {1: 0, 2: 0, 3: 0, 4: 0}
    result = current.execute("select box_no , abs(sum(TOTAL_AMOUNT_BEFORE_CHANGE - TOTAL_AMOUNT_AFTER_CHANGE)) / 100 from BOX_CHANGE_INFO_CASH where operation_type=4 and cash_type=2 and cash_container_type = 2 and busi_date = '%s' group by box_no" % date)
    for boxno in result.fetchall():
        billLoopClear[boxno[0]] = boxno[1]
        if boxno[1]:
            print('纸币循环鼓%d清空 ： %d元' % (boxno[0], boxno[1]))

    print('------------纸币分析结果------------')
    bOk = True
    for key in billLoopClear.keys():
        let = billSupplyToLoop[key] + billLoopAccept[key] - billLoopChange[key]
        ret = billLoopClear[key] - let
        if ret:
            bOk = False
            print('纸币循环鼓%d当天补充%d元，接收%d元，找零%d元，应剩%d元，实际清空%d元' % (key, billSupplyToLoop[key], billLoopAccept[key], billLoopChange[key], let, billLoopClear[key]))
    let = billSupplyBoxSet - billSupplyToLoopAmount - billSupplyToRecycle
    ret = billSupplyBoxClear - let
    if ret:
        bOk = False
        print('纸币补充箱当天补充%d元，补充到循环鼓%d元，补到回收箱%d元，应剩%d元，实际清空只有%d元' % (billSupplyBoxSet, billSupplyToLoopAmount, billSupplyToRecycle, let, billSupplyBoxClear))

    if bOk:
        print('纸币正常')


    print('------------硬币------------')
    '''硬币spare1补充'''
    result = current.execute("select abs(sum(TOTAL_COUNT_AFTER_CHANGE - TOTAL_COUNT_BEFORE_CHANGE)) from BOX_CHANGE_INFO_CASH where cash_type=1 and cash_container_type=3 and box_no=1 and operation_type=1 and busi_date =" + date)
    coinSpare1Supply = RetManager(result.fetchone())
    print('硬币spare1补充:' + str(coinSpare1Supply) + '枚')

    '''硬币spare2补充'''
    result = current.execute("select abs(sum(TOTAL_COUNT_AFTER_CHANGE - TOTAL_COUNT_BEFORE_CHANGE)) from BOX_CHANGE_INFO_CASH where cash_type=1 and cash_container_type=3 and box_no=2 and operation_type=1 and busi_date =" + date)
    coinSpare2Supply = RetManager(result.fetchone())
    print('硬币spare1补充:' + str(coinSpare2Supply) + '枚')

    '''硬币接收情况'''
    result = current.execute("select sum(t.OPER_COUNT) as CoinAccept from trans_info_of_cash_flow t where t.ACTION_TYPE=4 and t.CASH_TYPE=1 and t.BUSI_DATE=" + date)
    coinReceive = RetManager(result.fetchone())
    print('硬币接收:' + str(coinReceive) + '枚')

    '''硬币hopper找零情况'''
    result = current.execute("select sum(t.OPER_COUNT) as Change from trans_info_of_cash_flow t where t.ACTION_TYPE=5 and t.CASH_TYPE=1 and t.ORIGIN_CASH_CONTAINER_TYPE=2 and t.BUSI_DATE=" + date)
    coinHopper1Change = RetManager(result.fetchone())
    print('硬币hopper1找零:' + str(coinHopper1Change) + '枚')

    '''硬币spare1找零情况'''
    result = current.execute("select sum(t.OPER_COUNT) as Change from trans_info_of_cash_flow t where t.ACTION_TYPE=5 and t.CASH_TYPE=1 and t.ORIGIN_CASH_CONTAINER_TYPE=3 and t.ORIGIN_CASH_BOX_NO=1 and t.BUSI_DATE=" + date)
    coinSpare1Change = RetManager(result.fetchone())
    print('硬币spare1找零:' + str(coinSpare1Change) + '枚')

    '''硬币spare2找零情况'''
    result = current.execute("select sum(t.OPER_COUNT) as Change from trans_info_of_cash_flow t where t.ACTION_TYPE=5 and t.CASH_TYPE=1 and t.ORIGIN_CASH_CONTAINER_TYPE=3 and t.ORIGIN_CASH_BOX_NO=2 and t.BUSI_DATE=" + date)
    coinSpare2Change = RetManager(result.fetchone())
    print('硬币spare2找零:' + str(coinSpare2Change) + '枚')

    '''硬币hopper1清空'''
    result = current.execute("select abs(sum(TOTAL_COUNT_AFTER_CHANGE - TOTAL_COUNT_BEFORE_CHANGE)) from BOX_CHANGE_INFO_CASH where cash_type=1 and cash_container_type=2 and operation_type=4 and busi_date =" + date)
    coinHopper1Clear = RetManager(result.fetchone())
    print('硬币hopper1清空:' + str(coinHopper1Clear) + '枚')

    '''硬币spare1清空'''
    result = current.execute("select abs(sum(TOTAL_COUNT_AFTER_CHANGE - TOTAL_COUNT_BEFORE_CHANGE)) from BOX_CHANGE_INFO_CASH where cash_type=1 and cash_container_type=3 and box_no=1 and operation_type=4 and busi_date =" + date)
    coinSpare1Clear = RetManager(result.fetchone())
    print('硬币spare1清空:' + str(coinSpare1Clear) + '枚')

    '''硬币spare2清空'''
    result = current.execute("select abs(sum(TOTAL_COUNT_AFTER_CHANGE - TOTAL_COUNT_BEFORE_CHANGE)) from BOX_CHANGE_INFO_CASH where cash_type=1 and cash_container_type=3 and box_no=2 and operation_type=4 and busi_date =" + date)
    coinSpare2Clear = RetManager(result.fetchone())
    print('硬币spare1清空:' + str(coinSpare2Clear) + '枚')

    print('------------硬币分析结果------------')
    '''硬币循环鼓库存不对'''
    if not (coinReceive - coinHopper1Change) == coinHopper1Clear:
        print('硬币hopper当天接收'+str(coinReceive)+'枚，'+'从hopper找零'+str(coinHopper1Change)+'枚，应剩'+str(coinReceive - coinHopper1Change)+'枚，实际清空只有'+str(coinHopper1Clear)+'枚')

    '''备用找零箱库存不对'''
    if not (coinSpare1Supply - coinSpare1Change) == coinSpare1Clear:
        print('硬币备用找零箱1当天补充'+str(coinSpare1Supply)+'枚，'+'从备用找零箱1找零'+str(coinSpare1Change)+'枚，应剩'+str(coinSpare1Supply - coinSpare1Change)+'枚，实际清空只有'+str(coinSpare1Clear)+'枚')

    if not (coinSpare2Supply - coinSpare2Change) == coinSpare2Clear:
        print('硬币备用找零箱2当天补充'+str(coinSpare2Supply)+'枚，'+'从备用找零箱2找零'+str(coinSpare2Change)+'枚，应剩'+str(coinSpare2Supply - coinSpare2Change)+'枚，实际清空只有'+str(coinSpare2Clear)+'枚')
    print('---------------------------------------------------------------------------------------------------')

    print('票款：' + str(billAccept[1] + billLoopAcceptAmount + coinReceive - billLoopChangeAmount - coinSpare1Change - coinSpare2Change - coinHopper1Change))
