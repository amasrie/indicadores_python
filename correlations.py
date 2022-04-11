import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Crea la carpeta /plots si no existe
if not os.path.exists('plots'):
    os.makedirs('plots')

# Se carga el archivo CSV
df_survey = pd.read_csv ('dataset/survey_results_public.csv', sep=',')

# 1. distribución de edades/tipos

# Se obtienen las edades y tipo de programadores, ignorando NaN
df_age_type = df_survey[["Age", "MainBranch"]].dropna()
print(df_age_type["MainBranch"].unique())

df_age_type["MainBranch"].replace({
	"I am a developer by profession": "Desarrollador", 
	"I used to be a developer by profession, but no longer am": "Retirado", 
	"I am not primarily a developer, but I write code sometimes as part of my work": "Complemento", 
	"I am a student who is learning to code": "Estudiante", 
	"I code primarily as a hobby": "Fanático"}, inplace=True)
# Por cada tipo de programador, se hará un histograma de edades
plt.figure(figsize=(8, 6))
plt.subplots_adjust(left=0.1, right=0.8, top=0.9, bottom=0.1)
unique_types = df_age_type["MainBranch"].unique()
colors = ["red", "green", "orange", "blue", "purple"]
color_index = 0
boxes = plt.boxplot(list(map(lambda type: df_age_type[(df_age_type["MainBranch"] == type) & (df_age_type["Age"] < 120)]["Age"], unique_types)))
for patch in boxes["boxes"]:
	patch.set(color=colors[color_index])
	color_index += 1
plt.title('Distribución de edades por tipo de programador')
plt.ylabel('Edad')
plt.xticks([])
leg = plt.legend(df_age_type["MainBranch"].unique(), bbox_to_anchor=(0.75, 0.51, 0.54, 0.5))
for i, j in enumerate(leg.legendHandles):
    j.set_color(colors[i])
plt.savefig('plots/distribution_age_type.png')

# Calcular valores del gráfico anterior
for i, j in enumerate(unique_types):
	print("-----",j,"-----")
	q25 = np.percentile(df_age_type[(df_age_type["MainBranch"] == j)]["Age"], 25)
	q75 = np.percentile(df_age_type[(df_age_type["MainBranch"] == j)]["Age"], 75)
	iqr = q75 - q25
	print("IQR: ", iqr)
	print("Bigote Inferior: ", np.abs(q25 - (1.5*iqr)))
	print("Q25: ", q25)
	print("Mediana: ", np.median(df_age_type[(df_age_type["MainBranch"] == j)]["Age"]))
	print("Q75: ", q75)
	print("Bigote Superior: ", np.abs(q75 + (1.5*iqr)))

# 2. Correlación entre años programando y horas de trabajo a la semana
plt.figure()
df_times = df_survey[(df_survey["WorkWeekHrs"] < 150) & (df_survey["MainBranch"] == "I am a developer by profession") & (df_survey["Employment"] == "Employed full-time")][["YearsCode", "WorkWeekHrs", "Age"]].dropna()
df_times['YearsCode'].replace({ 'Less than 1 year': 0, 'More than 50 years': 51}, inplace=True)
df_times = df_times.astype({'YearsCode': int})
df_times = df_times[(df_times["Age"] > df_times["YearsCode"])][["YearsCode", "WorkWeekHrs"]].dropna()
print("Correlación entre años programando y horas de trabajo a la semana:\n", df_times.corr())
plt.scatter(df_times["YearsCode"], df_times["WorkWeekHrs"])
plt.title('Dispersión entre años programando y horas de trabajo a la semana')
plt.ylabel('Horas')
plt.xlabel('Años')
plt.savefig('plots/correlation_years_hours.png')

# 3. Correlación entre nivel educativo y tiempo que se tarda en aprender algo nuevo
plt.figure(figsize=(10, 10))
plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.1)
df_education = df_survey[["EdLevel", "NEWLearn"]].dropna()
df_education['EdLevel'].replace({ 
	"Master’s degree (M.A., M.S., M.Eng., MBA, etc.)": "2-Maestría", 
	"Bachelor’s degree (B.A., B.S., B.Eng., etc.)": "4-Pregrado",
	"Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)": "7-Secundaria",
	"Professional degree (JD, MD, etc.)": "3-Profesional",
	"Some college/university study without earning a degree": "5-Universidad (Parcial)",
	"Associate degree (A.A., A.S., etc.)": "6-Técnico",
	"Other doctoral degree (Ph.D., Ed.D., etc.)": "1-Otro",
	"Primary/elementary school": "8-Primaria",
	"I never completed any formal education": "9-Ninguno"
}, inplace=True)
df_education['NEWLearn'].replace({ 
	"Once a year": "Anualmente", 
	"Every few months": "Algunos meses",
	"Once every few years": "En unos años",
	"Once a decade": "Tras una década"
}, inplace=True)

table = df_education.pivot_table(index="EdLevel",columns="NEWLearn",aggfunc=lambda x:len(x))
ax = sns.heatmap(table, linewidth=0.5)
plt.title('Mapa de calor entre educación y aprendizaje de nuevas herramientas')
plt.ylabel('Educación')
plt.xlabel('Tiempo')
plt.savefig('plots/correlation_education.png')

# 4. Correlación entre satisfacción de trabajo actual y la búsqueda de un nuevo empleo




