from main import *

# 计算年汇总条目
calculate_yearly(27000,  # 基础月薪
                 12,  # 缴纳期数
                 [2, 3, 4],  # 年终奖范围，list，元素可填月份如[2, 3, 4]或者金额[10000, 20000]
                 provident_fund_rate=0.12,  # 住房公积金比例
                 medical_insurance_rate=0.02,  # 医疗保险比例
                 pension_insurance_rate=0.08,  # 养老保险比例
                 unemployment_insurance_rate=0.002,  # 失业保险比例
                 industrial_injury_insurance_rate=0,  # 工伤保险比例
                 maternity_insurance_rate=0,  # 生育保险比例
                 special_deduction=1500  # 额外专项扣除
                 )

# 也可以计算单月的
calculate_yearly(27000,  # 基础工资
                 1)  # 期数设定为单月
