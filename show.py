import pandas as pd
from collections import Counter
from pyecharts import Pie, Bar, Grid
from pyecharts import Funnel
from pyecharts import Radar
from pyecharts import Map
from pyecharts import Boxplot
import jieba
from imageio import imread
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
from pylab import mpl

# 读取csv文件
df = pd.read_csv('Python_jobs_cleaned.csv')

# （1）公司信息可视化
# 公司招聘信息数量
job_data_company = df["companyShortName"]
num_job_company = Counter(job_data_company)
job_company_list = sorted(num_job_company.items(), key=lambda x: x[1], reverse=True)
job_company = [x[0] for x in job_company_list[:20]]
num_company = [x[1] for x in job_company_list[:20]]
bar_company = Bar("各公司发布的招聘信息数量", title_pos='40%')
bar_company.add("", job_company, num_company, yaxis_name="招聘岗位数量",
                yaxis_name_gap=40, xaxis_rotate=45, is_label_show=True)
bar_company.render("companyShortName.html")
# 公司规模
job_data_companySize = df["companySize"]
num_job_companySize = Counter(job_data_companySize)
job_companySize = list(num_job_companySize.keys())
print(job_companySize)
num_companySize = list(num_job_companySize.values())
num_companySize_value = [num_companySize]
print(num_companySize_value)
schema = [('50-150人', 400), ('500-2000人', 400), ('少于15人', 400),
          ('150-500人', 400), ('2000人以上', 400), ('15-50人', 400)]
radar_companySize = Radar()
radar_companySize.config(schema)
radar_companySize.add("公司规模", num_companySize_value, label_color=["#4e79a7"], is_area_show=True)
radar_companySize.render("companySize.html")
# 公司融资情况
num_financeStage = Counter(df["financeStage"])
finance_stage = list(num_financeStage.keys())
finance_num = list(num_financeStage.values())
bar_financeStage = Bar("融资阶段-柱状图", title_pos='20%')
bar_financeStage.add("", finance_stage, finance_num, yaxis_name="公司数量", yaxis_name_gap=40,
                     xaxis_rotate=30, is_label_show=True)
pie_financeStage = Pie("融资阶段-饼状图", title_pos='55%')
pie_financeStage.add("", finance_stage, finance_num, is_label_show=True, radius=[25, 65],
                     center=[62, 50], rosetype='area', legend_orient="vertical", legend_pos="85%")
grid_financeStage = Grid(width=1200)
grid_financeStage.add(bar_financeStage, grid_right="60%")
grid_financeStage.add(pie_financeStage, grid_left="60%")
grid_financeStage.render("financeStage.html")
# 公司经营范围统计
num_industryField = Counter(df["industryField"])
job_industryField_list = sorted(num_industryField.items(), key=lambda x: x[1], reverse=True)
industry_Field = [x[0] for x in job_industryField_list[:30]]
industry_num = [x[1] for x in job_industryField_list[:30]]
pie_industryField = Pie("公司经营范围", title_pos='35%')
pie_industryField.add("", industry_Field, industry_num, is_label_show=True,
                      radius=[30, 75], center=[45, 50], legend_orient="vertical", legend_pos="85%", )
grid_industryField = Grid(width=900)
grid_industryField.add(pie_industryField, grid_right="50%")
grid_industryField.render("industryField.html")

# （2）招聘数量可视化
# 各城市招聘Python岗位数量
job_data_city = df["city"]
num_job_city = Counter(job_data_city)
job_city_list = sorted(num_job_city.items(), key=lambda x: x[1], reverse=True)
job_city = [x[0] for x in job_city_list[:20]]
num_city = [x[1] for x in job_city_list[:20]]
bar_city = Bar("各城市招聘Python岗位数量", title_pos='40%')
bar_city.add("", job_city, num_city, label_color=['#5AB5FF'], yaxis_name="招聘岗位数量",
             yaxis_name_gap=40, xaxis_rotate=55, is_label_show=True)
bar_city.render("city.html")
# 全国各省招聘Python岗位数量
dfp = pd.read_excel('province.xlsx')
dfp['city'] = dfp['city'].str.replace('市', '')
dfp['province'] = dfp['province'].str.replace('省', '')
dfp['province'] = dfp['province'].str.replace('市', '')
df_new = pd.merge(df, dfp.loc[:, ['city', 'province']], how='left', on='city').drop_duplicates()
job_data_province = df_new["province"]
num_job_province = Counter(job_data_province)
job_province = list(num_job_province.keys())
num_province = list(num_job_province.values())
map_china = Map("全国各省Python岗位招聘数量", title_pos='40%')
map_china.add("", job_province, num_province, maptype="china", is_label_show=True,
              is_visualmap=True, visual_text_color="#000")
map_china.render("China.html")
# 地区招聘信息数量
# 各区域招聘Python岗位数量
job_data_district = df["district"]
num_job_district = Counter(job_data_district)
job_district_list = sorted(num_job_district.items(), key=lambda x: x[1], reverse=True)
job_district = [x[0] for x in job_district_list[:20]]
num_district = [x[1] for x in job_district_list[:20]]
bar_district = Bar("各区域招聘Python岗位数量", title_pos='40%')
bar_district.add("", job_district, num_district, label_color=['#FA842B'], yaxis_name="招聘岗位数量",
                 yaxis_name_gap=40, xaxis_rotate=50, is_label_show=True)
bar_district.render("district.html")
# 北京市各区Python岗位招聘数量
# 北京市各区Python岗位招聘数量
job_district = list(num_job_district.keys())
num_district = list(num_job_district.values())
map_beijing = Map("北京市各区Python岗位招聘数量", title_pos='40%')
map_beijing.add(
    "", job_district, num_district, maptype="北京", is_label_show=True,
    is_visualmap=True, visual_text_color="#000")
map_beijing.render("beijing.html")
# 上海市各区Python岗位招聘数量
map_shanghai = Map("上海市各区Python岗位招聘数量", title_pos='40%')
map_shanghai.add(
    "", job_district, num_district, maptype="上海", is_label_show=True,
    is_visualmap=True, visual_text_color="#000")
map_shanghai.render("shanghai.html")
# 深圳市各区Python岗位招聘数量
map_shenzhen = Map("深圳市各区Python岗位招聘数量", title_pos='40%')
map_shenzhen.add(
    "", job_district, num_district, maptype="深圳", is_label_show=True,
    is_visualmap=True, visual_text_color="#000")
map_shenzhen.render("shenzhen.html")
# Python相关职位招聘数量
job_data_positionName = df["positionName"]
num_job_positionName = Counter(job_data_positionName)
job_positionName_list = sorted(num_job_positionName.items(), key=lambda x: x[1], reverse=True)
job_positionName = [x[0] for x in job_positionName_list[:20]]
num_positionName = [x[1] for x in job_positionName_list[:20]]
bar_positionName = Bar("Python相关岗位招聘数量", title_pos='40%')
bar_positionName.add("", job_positionName, num_positionName, yaxis_name="招聘岗位数量",
                     yaxis_name_gap=40, label_color=['#007500'], xaxis_rotate=30, is_label_show=True)
bar_positionName.render("positionName.html")

# （3）薪资水平
# 薪资情况
df['salary_min'] = df['salary_min'].str.replace('k', '').str.split('-', expand=True).astype(int)
df['salary_max'] = df['salary_max'].str.replace('k', '').str.split('-', expand=True).astype(int)
# 平均月薪
list_salary_average = df.apply(lambda x: (x['salary_min'] + x['salary_max']) / 2, axis=1)
num_10, num_10_15, num_15_20, num_25_down, num_25_up = 0, 0, 0, 0, 0
for i in list_salary_average:
    if i < 10:
        num_10 += 1
    elif i < 15:
        num_10_15 += 1
    elif i < 20:
        num_15_20 += 1
    elif i < 25:
        num_25_down += 1
    else:
        num_25_up += 1
list_end = [num_10, num_10_15, num_15_20, num_25_down, num_25_up]
job_salary_message = ["小于10K", "10K—15K", "15K—20K", "20K-25K", "大于25K"]
job_salary_number = list_end[:]
bar_salary = Bar("Python岗位平均月薪分布", title_pos='40%')
bar_salary.add("", job_salary_message, job_salary_number, yaxis_name="公司数量",
               yaxis_name_gap=40, xaxis_rotate=30, is_label_show=True)
bar_salary.render("salary.html")
# 城市和月薪
job_data_city = df["city"]
num_job_city = Counter(job_data_city)
job_city_list = sorted(num_job_city.items(), key=lambda x: x[1], reverse=True)
x_city = [x[0] for x in job_city_list[:10]]
ls_min = []
ls_max = []
for x in x_city:
    lt_min = df[df['city'] == x]['salary_min'].tolist()
    ls_min.append(lt_min)
    lt_max = df[df['city'] == x]['salary_max'].tolist()
    ls_max.append(lt_max)
boxplot_city_salary = Boxplot('各城市最低和最高月薪的箱线图')
boxplot_city_salary.add('最低月薪', x_city, boxplot_city_salary.prepare_data(ls_min))
boxplot_city_salary.add('最高月薪', x_city, boxplot_city_salary.prepare_data(ls_max))
boxplot_city_salary.render("city_salary.html")
# 学历要求
job_education = Counter(df["education"])
job_education_attr = list(job_education.keys())
job_education_value = list(job_education.values())
pie_education = Pie("Python岗位学历要求", title_pos="center")
pie_education.add("", job_education_attr, job_education_value, is_label_show=True,
                  legend_orient="vertical", legend_pos="left")
pie_education.render("education.html")
# 学历和月薪
x_education = '大专，本科，硕士'.split('，')
ls_min = []
ls_max = []
for x in x_education:
    lt_min = df[df['education'] == x]['salary_min'].tolist()
    ls_min.append(lt_min)
    lt_max = df[df['education'] == x]['salary_max'].tolist()
    ls_max.append(lt_max)
boxplot_education_salary = Boxplot('各学历最低和最高月薪的箱线图')
boxplot_education_salary.add('最低月薪', x_education, boxplot_education_salary.prepare_data(ls_min))
boxplot_education_salary.add('最高月薪', x_education, boxplot_education_salary.prepare_data(ls_max))
boxplot_education_salary.render("education_salary.html")
# 工作经验要求
job_workYear = Counter(df["workYear"])
job_workYear_attr = list(job_workYear.keys())
job_workYear_value = list(job_workYear.values())
funnel_workYear = Funnel("工作经验要求", title_pos="center")
funnel_workYear.add("", job_workYear_attr, job_workYear_value, is_label_show=True,
                    label_pos="outside", legend_orient="vertical", legend_pos="left")
funnel_workYear.render("workYear.html")
# 工作经验和月薪
x_workYear = '在校/应届，应届毕业生，1年以下，1-3，3-5，5-10'.split('，')
ls_min = []
ls_max = []
for x in x_workYear:
    lt_min = df[df['workYear'] == x]['salary_min'].tolist()
    ls_min.append(lt_min)
    lt_max = df[df['workYear'] == x]['salary_max'].tolist()
    ls_max.append(lt_max)
boxplot_workYear_salary = Boxplot('各工作经验最低和最高月薪的箱线图')
boxplot_workYear_salary.add('最低月薪', x_workYear, boxplot_workYear_salary.prepare_data(ls_min))
boxplot_workYear_salary.add('最高月薪', x_workYear, boxplot_workYear_salary.prepare_data(ls_max))
boxplot_workYear_salary.render("workYear_salary.html")

# 职位福利
# 岗位类型统计
job_firstType = Counter(df["firstType"])
job_firstType_attr = list(job_firstType.keys())
job_firstType_value = list(job_firstType.values())
job_firstType_pie = Pie("第一岗位类型", title_pos="25%")
job_firstType_pie.add("", job_firstType_attr, job_firstType_value, is_label_show=True,
                      radius=[0, 60], center=[30, 65], legend_orient="vertical", legend_pos="left")

job_secondType = Counter(df["secondType"])
job_secondType_attr = list(job_secondType.keys())
job_secondType_value = list(job_secondType.values())
job_secondType_pie = Pie("第二岗位类型", title_pos='55%')
job_secondType_pie.add("", job_secondType_attr, job_secondType_value, is_label_show=True,
                       radius=[0, 60], center=[60, 65], legend_orient="vertical", legend_pos="75%")
grid_jobType = Grid(width=1200)
grid_jobType.add(job_firstType_pie, grid_right="10%")
grid_jobType.add(job_secondType_pie, grid_left="10%")
grid_jobType.render("jobType.html")
# 职位优势词云图
job_advantage = list(df["positionAdvantage"])


# 将列表数据写入txt文件
def text_save(filename, data):
    with open(filename, 'w', encoding='utf-8') as file_object:
        for i in range(len(data)):
            file_object.write(str(data[i]) + "  ")
    print("保存文件成功")


text_save("positionAdvantage.txt", job_advantage)


# 读取文件
def readDocument():
    text = open('positionAdvantage.txt', 'r', encoding='utf-8').read()
    return text


# 用jieba分词
def segment(doc):
    seg_list = " ".join(jieba.cut(doc, cut_all=False))
    return seg_list


# 制作词云,设置词云参数
def drawWordCloud(seg_list):
    color_mask = imread("词云map.jpg")  # 读取背景图片,注意路径
    wc = WordCloud(font_path="simkai.ttf", background_color='white', mask=color_mask,
                   max_words=2000, max_font_size=50, min_font_size=10)
    wc.generate(seg_list)  # 产生词云
    plt.figure()
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    wc.to_file("职位优势词云图.jpg")  # 保存图片
    plt.show()


# 去停用词
def removeStopWords(seg_list):
    wordlist_stopwords_removed = []
    stop_words = open('StopWords.txt')
    stop_words_text = stop_words.read()
    stop_words.close()
    stop_words_text_list = stop_words_text.split('\n')
    after_seg_text_list = seg_list.split(' ')
    for word in after_seg_text_list:
        if word not in stop_words_text_list:
            wordlist_stopwords_removed.append(word)
    return ' '.join(wordlist_stopwords_removed)


if __name__ == "__main__":
    doc = readDocument()
    segment_list = segment(doc)
    segment_list_remove_stopwords = removeStopWords(segment_list)
    drawWordCloud(segment_list_remove_stopwords)

# 公司福利词云图
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False
text = ''
for line in df['companyLabelList']:
    if len(eval(line)) == 0:
        continue
    else:
        for word in eval(line):
            text += word
cut_word = ','.join(jieba.cut(text))
cloud = WordCloud(font_path="simkai.ttf", background_color='black', max_words=2000,
                  max_font_size=100, width=1000, height=600)
word_cloud = cloud.generate(cut_word)
word_cloud.to_file('公司福利词云图.jpg')
plt.imshow(word_cloud)
plt.axis('off')
plt.show()
