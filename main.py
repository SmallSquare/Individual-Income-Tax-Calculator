from prettytable import PrettyTable


def get_tax_payable(cti):
    """
    计算应缴税额

    :cti: cumulative_taxable_income 累计应纳税所得额
    :return: tax payable
    """
    match cti:
        case x if x <= 36000:
            tax_payable = cti * 0.03
        case x if x <= 144000:
            tax_payable = cti * 0.10 - 2520.0
        case x if x <= 300000:
            tax_payable = cti * 0.20 - 16920.0
        case x if x <= 420000:
            tax_payable = cti * 0.25 - 31920.0
        case x if x <= 660000:
            tax_payable = cti * 0.30 - 52920.0
        case x if x <= 960000:
            tax_payable = cti * 0.35 - 85920.0
        case _:
            tax_payable = cti * 0.45 - 181920.0

    return round(tax_payable, 2)


def calculate_monthly(pretex_income,
                      num_of_period,
                      provident_fund_rate=0.12,
                      medical_insurance_rate=0.02,
                      pension_insurance_rate=0.08,
                      unemployment_insurance_rate=0.002,
                      industrial_injury_insurance_rate=0,
                      maternity_insurance_rate=0,
                      special_deduction=0):
    """
    按月计算

    :param pretex_income: 税前月薪
    :param num_of_period: 缴纳期数
    :param provident_fund_rate: 公积金比例
    :param medical_insurance_rate: 医疗保险比例
    :param pension_insurance_rate: 养老保险比例
    :param unemployment_insurance_rate: 失业保险比例
    :param industrial_injury_insurance_rate: 工伤保险比例
    :param maternity_insurance_rate: 生育保险比例
    :param special_deduction: 额外专项扣除
    :return: 返回一个包含结果的名为`result`的dict
    """
    result = dict()

    # 计算 五险一金、专项附加扣除
    provident_fund = pretex_income * provident_fund_rate
    medical_insurance = pretex_income * medical_insurance_rate
    pension_insurance = pretex_income * pension_insurance_rate
    unemployment_insurance = pretex_income * unemployment_insurance_rate
    industrial_injury_insurance = pretex_income * industrial_injury_insurance_rate
    maternity_insurance = pretex_income * maternity_insurance_rate
    insurances_and_fund = \
        provident_fund + medical_insurance + pension_insurance + unemployment_insurance + \
        industrial_injury_insurance + maternity_insurance
    final_provident_fund = provident_fund * 2

    result['pretex_income'] = pretex_income
    result['provident_fund'] = provident_fund
    result['medical_insurance'] = medical_insurance
    result['pension_insurance'] = pension_insurance
    result['unemployment_insurance'] = unemployment_insurance
    result['industrial_injury_insurance'] = industrial_injury_insurance
    result['maternity_insurance'] = maternity_insurance
    result['special_deduction'] = special_deduction
    result['insurances_and_fund'] = insurances_and_fund
    result['final_provident_fund'] = final_provident_fund

    # 计算 应纳税所得额
    taxable_income = \
        pretex_income - provident_fund - medical_insurance - pension_insurance - unemployment_insurance - \
        industrial_injury_insurance - maternity_insurance - special_deduction - 5000
    taxable_income = max(taxable_income, 0)
    result['taxable_income'] = taxable_income

    # 计算 累计应纳税所得额、累计应缴纳税额
    cumulative_taxable_income = taxable_income * num_of_period
    result['cumulative_taxable_income'] = cumulative_taxable_income
    tax_payable = get_tax_payable(cumulative_taxable_income)
    result['tax_payable'] = tax_payable

    # 计算 累计已纳税所得额、累计已缴纳税额
    cumulative_taxed_income = taxable_income * (num_of_period - 1)
    result['cumulative_taxed_income'] = cumulative_taxed_income
    tax_paid = get_tax_payable(cumulative_taxed_income)
    result['tax_paid'] = tax_paid

    # 计算 当期应缴纳税额
    tax_payable_currently = round(tax_payable - tax_paid, 2)
    result['tax_payable_currently'] = tax_payable_currently

    # 计算 税后工资
    after_tax_income = pretex_income - insurances_and_fund - tax_payable_currently
    result['after_tax_income'] = after_tax_income

    return result


def calculate_bonus(pretax_bonus):
    """
    计算年终奖的个税

    :param pretax_bonus: 税前年终奖金
    :return: 应缴税额，税后年终奖金
    """
    match pretax_bonus:
        case x if x / 12 <= 3000:
            tax_payable = x * 0.03
        case x if x / 12 <= 12000:
            tax_payable = x * 0.10 - 210.0
        case x if x / 12 <= 25000:
            tax_payable = x * 0.20 - 1410.0
        case x if x / 12 <= 35000:
            tax_payable = x * 0.25 - 2660.0
        case x if x / 12 <= 55000:
            tax_payable = x * 0.30 - 4410.0
        case x if x / 12 <= 80000:
            tax_payable = x * 0.35 - 7160.0
        case _:
            tax_payable = x * 0.45 - 15160.0
    return tax_payable, round(pretax_bonus - tax_payable, 2)


def calculate_yearly(pretex_income,
                     num_of_periods,
                     year_end_bonus=[0],
                     provident_fund_rate=0.12,
                     medical_insurance_rate=0.02,
                     pension_insurance_rate=0.08,
                     unemployment_insurance_rate=0.002,
                     industrial_injury_insurance_rate=0,
                     maternity_insurance_rate=0,
                     special_deduction=0):
    """
    按年计算，并打印汇总条目表格

    :param pretex_income: 税前月薪
    :param num_of_periods: 缴纳期数
    :param year_end_bonus: 年终奖金
    :param provident_fund_rate: 公积金比例
    :param medical_insurance_rate: 医疗保险比例
    :param pension_insurance_rate: 养老保险比例
    :param unemployment_insurance_rate: 失业保险比例
    :param industrial_injury_insurance_rate: 工伤保险比例
    :param maternity_insurance_rate: 生育保险比例
    :param special_deduction: 额外专项扣除
    :return: None
    """
    # 计算年终奖
    bonus_rates = []
    if year_end_bonus[-1] <= 100:  # 将n月年终奖转换为年终奖金数额
        for i in range(len(year_end_bonus)):
            bonus_rates.append(round(year_end_bonus[i] * num_of_periods / 12, 2))
            year_end_bonus[i] = round(pretex_income * year_end_bonus[i] * num_of_periods / 12, 2)
    else:
        for i in range(len(year_end_bonus)):
            bonus_rates.append(round(year_end_bonus[i] / pretex_income, 2))
    bonus_taxes, after_tax_bonuses = [], []
    for i in range(len(year_end_bonus)):
        bonus_tax, after_tax_bonus = calculate_bonus(year_end_bonus[i])
        bonus_taxes.append(bonus_tax)
        after_tax_bonuses.append(after_tax_bonus)
    # 计算月收入
    month_reports = list()
    table1 = PrettyTable(['条目', '月额', '率', '年额'])
    table2 = PrettyTable(['期', '税前工资', '五险一金扣除', '当期应缴税额', '税后工资', '累计应缴税额'])
    after_tax_incomes = list()
    for i in range(1, num_of_periods + 1):
        report = calculate_monthly(pretex_income,
                                   i,
                                   provident_fund_rate=provident_fund_rate,
                                   medical_insurance_rate=medical_insurance_rate,
                                   pension_insurance_rate=pension_insurance_rate,
                                   unemployment_insurance_rate=unemployment_insurance_rate,
                                   industrial_injury_insurance_rate=industrial_injury_insurance_rate,
                                   maternity_insurance_rate=maternity_insurance_rate,
                                   special_deduction=special_deduction)
        month_reports.append(report)
        table2.add_row([i, pretex_income, report['insurances_and_fund'], report['tax_payable_currently'],
                        report['after_tax_income'], report['tax_payable']])
        after_tax_incomes.append(report['after_tax_income'])
    table1.add_rows([
        ['税前工资', pretex_income, "-",
         pretex_income * num_of_periods],
        ['应缴公积金', month_reports[0]['provident_fund'], "%s%%" % (provident_fund_rate * 100),
         month_reports[0]['provident_fund'] * num_of_periods],
        ['医疗保险', month_reports[0]['medical_insurance'], "%s%%" % (medical_insurance_rate * 100),
         month_reports[0]['medical_insurance'] * num_of_periods],
        ['养老保险', month_reports[0]['pension_insurance'], "%s%%" % (pension_insurance_rate * 100),
         month_reports[0]['pension_insurance'] * num_of_periods],
        ['失业保险', month_reports[0]['unemployment_insurance'], "%s%%" % (unemployment_insurance_rate * 100),
         month_reports[0]['unemployment_insurance'] * num_of_periods],
        ['工伤保险', month_reports[0]['industrial_injury_insurance'], "%s%%" % (industrial_injury_insurance_rate * 100),
         month_reports[0]['industrial_injury_insurance'] * num_of_periods],
        ['生育保险', month_reports[0]['maternity_insurance'], "%s%%" % (maternity_insurance_rate * 100),
         month_reports[0]['maternity_insurance'] * num_of_periods],
        ['扣除五险一金', month_reports[0]['insurances_and_fund'], "-",
         month_reports[0]['insurances_and_fund'] * num_of_periods],
        ['额外专项扣除', month_reports[0]['special_deduction'], "-",
         month_reports[0]['special_deduction'] * num_of_periods],
        ['应纳税所得额', month_reports[0]['taxable_income'], "-",
         month_reports[0]['taxable_income'] * num_of_periods],
        ['实得公积金', month_reports[0]['final_provident_fund'],
         "%s%%+%s%%" % (provident_fund_rate * 100, provident_fund_rate * 100),
         month_reports[0]['final_provident_fund'] * num_of_periods],
        # ['税前年终奖金', year_end_bonus, "%d个月" % bonus_rate,
        #  pretex_income * num_of_periods + year_end_bonus],
    ])
    table2.add_row(["合计",
                    pretex_income * num_of_periods,
                    month_reports[-1]['insurances_and_fund'] * num_of_periods,
                    month_reports[-1]["tax_payable"],
                    round(sum(after_tax_incomes), 2),
                    "-"])
    for i in range(len(year_end_bonus)):
        table2.add_row(["年终%s个月" % (bonus_rates[i]), year_end_bonus[i], "0", bonus_taxes[i], after_tax_bonuses[i],
                        bonus_taxes[i]])
        table2.add_row(["合计%d(+%s)" % (i + 1, bonus_rates[i]),
                        round(pretex_income * num_of_periods + year_end_bonus[i], 2),
                        month_reports[-1]['insurances_and_fund'] * num_of_periods,
                        month_reports[-1]["tax_payable"] + bonus_taxes[i],
                        round(sum(after_tax_incomes) + after_tax_bonuses[i], 2),
                        "-"])
    print("\n【税前%s元×%d期 + 年终%s个月】" % (pretex_income, num_of_periods, bonus_rates))
    print(">按月基本工资条目：")
    print(table1)
    print(">年汇总条目：")
    print(table2)


if __name__ == '__main__':
    pass
