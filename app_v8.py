import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 
import timeit
from io import BytesIO


# Configurações da página
st.set_page_config(
    page_title = 'Telemarketing analisys',
    page_icon = 'telmarketing_icon.png',
    layout = 'wide',
    initial_sidebar_state='expanded'
)


st.write('# Análise dos dados de Telemarketing')
st.markdown('---')
# Barra lateral
image = 'Bank-Branding.jpg'
st.sidebar.image(image)


# Ajuste dos gráficos
custom_params = {'axes.spines.right': False, 'axes.spines.top': False}
sns.set_theme(style='ticks', rc=custom_params)


# Função para ler os dados
@st.cache_data(show_spinner=True) # Usando o decorador
def load_data(file_data):
    try:
        return pd.read_csv(file_data, sep=';')
    except:
        return pd.read_excel(file_data) 


# Filtro para seleção múltipla
@st.cache_data()
def multiselect_filter(dataframe, col, selecionados):
    if 'all' in selecionados:
        return dataframe 
    else:
        return dataframe[dataframe[col].isin(selecionados)].reset_index(drop=True)


# Transformando dataframe em string
@st.cache_data
def df_tostring(df):
    return df.to_csv(index=False)


# Transformando dataframe em bytes
@st.cache_data
def df_tobytes(df):
    return df.to_csv(index=False).encode('utf-8')


# Transformando para excel
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output)
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.close()
    processed_data = output.getvalue()
    return processed_data


# Função principal 
def main():
    # Carregamento do arquivo
    st.sidebar.write('## Suba o arquivo 📃')
    data_file_1 = st.sidebar.file_uploader('Bank marketing data', type=['csv', 'xlsx'])
    # st.sidebar.write(data_file_1)

    # Trabalhando com o arquivo de dados selecionado
    if (data_file_1 is not None):
        # start = timeit.default_timer() # Contagem tempo
        bank_raw = load_data(data_file_1)

        # st.write('Time: ', timeit.default_timer() - start) # Contagem tempo
        bank = bank_raw.copy()
        st.write('## Dados brutos')
        st.write('- Dimensão do DataFrame "bruto":', bank_raw.shape)
        st.write(bank_raw.head())


        with st.sidebar.form(key='my_form'):

            # Seleção do tipo de gráfico
            graph_type = st.radio('**Tipo de gráfico:**', ('Barras', 'Pizza'))

            # Criando filtros para idade
            max_age = int(bank.age.max())
            min_age = int(bank.age.min())
            idades = st.slider(
                label='**Idades**',
                min_value = min_age,
                max_value = max_age,
                value = (min_age, max_age),
                step = 1
            )
            # st.write('Idades:', idades)
            # st.write('Idade min:', idades[0])
            # st.write('Idade max:', idades[1])


            #### Profissões (filtro) ####

            job_list = bank.job.unique().tolist()
            # st.write('**Profissões:** ', job_list)
            job_list.append('all')
            # seleção
            jobs_selected = st.multiselect('**Profissão:**', job_list, ['all'])
            # st.write('Profissões selecionadas: ', jobs_selected)

            #### ESTADO CIVIL (filtro) ####
            marital_list = bank.marital.unique().tolist()
            marital_list.append('all')
            marital_selected = st.multiselect('**Estado civil:**', marital_list, ['all'])

            #### DEFAULT (filtro) ####
            default_list = bank.default.unique().tolist()
            default_list.append('all')
            default_selected = st.multiselect('**Default:**', default_list, ['all'])

            #### HOUSING - financiamento imobiliário? (filtro) ####
            housing_list = bank.housing.unique().tolist()
            housing_list.append('all')
            housing_selected = st.multiselect('**Tem financiamento imob.?**', housing_list, ['all'])

            #### TEM EMPRESTIMO? (filtro) ####
            loan_list = bank.loan.unique().tolist()
            loan_list.append('all')
            loan_selected = st.multiselect('**Tem empréstimo?**', loan_list, ['all'])

            #### FORMA DE CONTATO (filtro) ####
            contact_list = bank.contact.unique().tolist()
            contact_list.append('all')
            contact_selected = st.multiselect('**Forma de contato:**', contact_list, ['all'])

            #### MÊS (filtro) ####
            month_list = bank.month.unique().tolist()
            month_list.append('all')
            month_selected = st.multiselect('**Mês:**', month_list, ['all'])

            #### DIA DA SEMANA (filtro) ####
            day_list = bank.day_of_week.unique().tolist()
            day_list.append('all')
            day_selected = st.multiselect('**Dia da semana:**', day_list, ['all'])


            ## APLICANDO FILTROS ##
            
            # Idade
            bank = bank[(bank['age'] >= idades[0]) & (bank['age'] <= idades[1])]
            # Profissão
            bank = multiselect_filter(bank, 'job', jobs_selected)
            # Estado vicil
            bank = multiselect_filter(bank, 'marital', marital_selected)
            # Default
            bank = multiselect_filter(bank, 'default', default_selected)
            # Tem financiamento imobiliário
            bank = multiselect_filter(bank, 'housing', housing_selected)
            # Tem empréstimo
            bank = multiselect_filter(bank, 'loan', loan_selected)
            # Forma de contato
            bank = multiselect_filter(bank, 'contact', contact_selected)
            # Mês
            bank = multiselect_filter(bank, 'month', month_selected)
            # Dia da semana
            bank = multiselect_filter(bank, 'day_of_week', day_selected)

            submit_button = st.form_submit_button(label='📈 Aplicar')


        # Aplicando filtros
        st.write('## Dados filtrados')
        st.write('- Dimensão do conjunto de dados:', bank.shape)
        st.write(bank.head())
         # Botões para download dos dados filtrados
        df_xlsx = to_excel(bank)
        st.download_button(
            label='🗃️ Download tabela filtrada em Excel',
            data = df_xlsx,
            file_name = 'bank_filtered.xlsx'
        )
        st.markdown('---')        


        ## PERCENTUAIS ##
        # Dados brutos
        bank_raw_target_perc = bank_raw.y.value_counts(normalize=True).to_frame()*100
        bank_raw_target_perc = bank_raw_target_perc.sort_index()        
        # Dados filtrados
        try:             
            bank_target_perc = bank['y'].value_counts(normalize=True).to_frame()*100
            bank_target_perc = bank_target_perc.sort_index()
        except:
            st.erros('Erro no filtro')

        
        # Botões para download dos dados dos gráficos
        col1, col2 = st.columns(2)

        df_xlsx_raw = to_excel(bank_raw_target_perc)
        col1.write('### Proporção original (dados brutos)')
        col1.write(bank_raw_target_perc)
        col1.download_button(label='🗃️ Download',
                            data = df_xlsx_raw,
                            file_name = 'bank_raw_y.xlsx')
        
        df_xlsx_filt = to_excel(bank_target_perc)
        col2.write('### Proporção nos dados filtrados')
        col2.write(bank_target_perc)
        col2.download_button(label='🗃️ Download',
                            data = df_xlsx_filt,
                            file_name = 'bank_filt_y.xlsx')
        st.markdown('---')


        #### Plots ####

        st.write('## Proporção de aceite')

        fig, ax = plt.subplots(1, 2, figsize=[8, 5])
        if graph_type == 'Barras':            
            sns.barplot(
                data = bank_raw_target_perc,
                x = bank_raw_target_perc.index,
                y = 'proportion',
                ax = ax[0]
            )
            ax[0].bar_label(ax[0].containers[0])
            ax[0].set_title('Dados brutos', fontweight='bold')

            sns.barplot(
                data = bank_target_perc,
                x = bank_target_perc.index, 
                y = 'proportion',
                ax = ax[1]
            )
            ax[1].bar_label(ax[1].containers[0])
            ax[1].set_title('Dados filtrados', fontweight='bold')
        
        else:
            bank_raw_target_perc.plot(
                kind='pie', 
                autopct='%.2f', 
                y = 'proportion',
                ax = ax[0])
            ax[0].set_title('Dados brutos', fontweight='bold')

            bank_target_perc.plot(
                kind='pie', 
                autopct='%.2f',
                y = 'proportion', 
                ax = ax[1]
            )
            ax[1].set_title('Dados filtrados', fontweight='bold')

        st.pyplot(plt)

if __name__ == '__main__':
    main()
