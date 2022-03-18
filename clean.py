import pandas as pd

# 读取csv文件
df = pd.read_csv("Python_jobs.csv", encoding="utf-8")

# df.head()  # 查看导入的数据
# df.shape  # (行, 列)
# df.columns  # 查看导入的列数据

# 缺失值处理
# 数据滤除
df = df.drop(['positionId', 'companyId', 'companyLogo', 'thirdType', 'skillLables', 'positionLables',
              'industryLables', 'createTime', 'formatCreateTime', 'businessZones', 'salaryMonth',
              'jobNature', 'imState', 'lastLogin', 'publisherId', 'approve', 'subwayline', 'stationname',
              'linestaion', 'latitude', 'longitude', 'distance', 'hitags', 'resumeProcessRate',
              'resumeProcessDay', 'score', 'newScore', 'matchScore', 'matchScoreExplain', 'query',
              'explain', 'isSchoolJob', 'adWord', 'plus', 'pcShow', 'appShow', 'deliver', 'gradeDescription',
              'promotionScoreExplain', 'isHotHire', 'count', 'aggregatePositionIds', 'promotionType',
              'is51Job', 'hunterJob', 'detailRecall', 'famousCompany'], axis=1)

# df.shape  # 查看删除列后的数据
# df.head(5)

# 数据填充
df.fillna({'district': '滨江区'}, inplace=True)

df.drop_duplicates(inplace=True)  # 数据去重

# 将月薪salary列分割为最低月薪salary_min和最高月薪salary_max,并去除无关字符
salary_m = df['salary'].str.split('-', expand=True)
df = df.drop('salary', axis=1).join(salary_m)
df.rename(columns={0: 'salary_min', 1: 'salary_max'}, inplace=True)
# 将workYear列统一为：应届毕业生、一年以下、1-3年、3-5年、5-10年、10年以上六类，并去除无关字符;
workYear_m = df['workYear'].str.strip('经验年').str.replace('不限', '应届毕业生')
df = df.drop('workYear', axis=1).join(workYear_m)
# 将学历列划分类别：大专、本科、硕士、博士
edu_c = df['education'].str.replace(r'.*不限.*', '大专').str.replace(r'及以上.*', '')
df = df.drop('education', axis=1).join(edu_c)

df = df.reindex(columns=['seq', 'companyFullName', 'companyShortName', 'companySize', 'financeStage', 'city',
                         'district', 'positionName', 'education', 'workYear', 'salary_min', 'salary_max',
                         'industryField', 'firstType', 'secondType', 'positionAdvantage', 'companyLabelList'])
df['seq'] = range(df.iloc[:, 0].size)
df.set_index(['seq'], inplace=True)
print(df)

df.to_csv("Python_jobs_cleaned.csv", index=False)
