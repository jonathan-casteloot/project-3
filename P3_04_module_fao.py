import pandas as pd
import random

path = './DATA/'

csv_cereales   = 'fr_céréales.csv'
csv_vegetaux   = 'fr_vegetaux.csv'
csv_animaux    = 'fr_animaux.csv'
csv_population = 'fr_population.csv'

population     = pd.read_csv('population.csv')
sous_nutrition = pd.read_csv('sous_nutrition.csv')
dispo_alim     = pd.read_csv('dispo_alim.csv')
equilibre_prod = pd.read_csv('equilibre_prod.csv')
balance_com    = pd.read_csv('balance_com.csv')


class Liste :

    def cereales():
        
        dataframe = pd.read_csv(path + csv_cereales, usecols=['Code Produit'])
        return dataframe['Code Produit'].unique()
    
    def produits_animaux():
        
        dataframe  = dispo_alim[dispo_alim['origin'] == 'animal']
        return dataframe['code_produit'].unique()

    
def code_produit(product_name):
    dataframe = dispo_alim[dispo_alim['produit'] == product_name]
    return dataframe['code_produit'].unique()

    
def france_ble():
        
    dataframe = pd.read_csv(path + csv_vegetaux, 
                            usecols=['Zone','Produit','Élément','Valeur','Unité']
                           )

    dataframe = dataframe[ (dataframe['Zone'] == 'France')
                          &(dataframe['Produit'] == 'Blé')
                         ]

    dataframe.drop(index=[37498,37499,37500,37501], 
                   inplace=True
                  )
    
    return dataframe


def sum_population(table_name):
    
    if table_name == 'population':
        people = population['population']
        
    elif table_name == 'sous_nutrition':
        people = sous_nutrition['nb_personnes']
    
    return people.sum()


# order by desc , keep best nb_rank
def order_by_desc_limit(dataframe,colonne_dataframe,nb_rank):
    
    dataframe_top_produit = dataframe.sort_values(by=colonne_dataframe,ascending=False)
    dataframe_top_produit = dataframe_top_produit.head(nb_rank)
    dataframe_top_produit.reset_index(drop = True, inplace = True)
    
    return dataframe_top_produit


# group by and reset index
def group_by_reset_index(dataframe,dataframe_column,operation_name):
    
    if operation_name == 'mean':
        # to avoid wrong mean computation
        dataframe = dataframe[dataframe[dataframe_column]!=0]
        
        dataframe = dataframe.groupby(dataframe_column).mean()
        
    elif operation_name == 'sum':
        dataframe = dataframe.groupby(dataframe_column).sum()
        
    dataframe.reset_index(inplace=True)
    
    return dataframe


def calculer_20_meilleurs_produits(dataframe,colonne_ratio):
    
    dataframe = dataframe[['produit', colonne_ratio]]
    
    # GROUP BY produit WITH mean
    dataframe = group_by_reset_index(dataframe,'produit','mean')
    
    # ORDER BY colonne_ratio DESC LIMIT 20
    dataframe = order_by_desc_limit(dataframe,colonne_ratio,20)

    return dataframe


def somme_equilibre_prod(column_equilibre_prod,column_table_ratio, dataframe_table_ratio , origin=''):
    
    # to select useful data
    e = equilibre_prod[['pays','produit',column_equilibre_prod]].copy()
    d = dispo_alim[['pays','produit','origin']].copy()
    t = dataframe_table_ratio[['produit',column_table_ratio]].copy()
    
    # to filter by origin
    if origin != '':
        d = d[d['origin'] == origin]
        
    e = e.merge(d,how = 'inner',on = ['pays','produit'])
    e = e.merge(t,how = 'left' ,on = ['produit'])

    # from MT to kg
    e[column_equilibre_prod] *= 10**6 

    # compute column with ratio
    e[column_equilibre_prod] *= e[column_table_ratio]

    return e[column_equilibre_prod].sum()


def calculer_personnes_ratio(apport_journalier_recommande,
                             liste_colonnes_equilibre_prod,
                             colonne_table_ratio,
                             dataframe_table_ratio,
                             origin=''):
    nb_personnes = 0
    
    for name_col in liste_colonnes_equilibre_prod:
        nb_personnes += (somme_equilibre_prod(name_col,
                                              colonne_table_ratio,
                                              dataframe_table_ratio,
                                              origin)
                        )/365
    
    nb_personnes /= apport_journalier_recommande

    # to compute ratio
    ratio = nb_personnes * 100 / sum_population('population')
    
    return [nb_personnes,ratio]


def calculer_ratio(dataframe,colonne,nom_ratio):
    # merge : 1 on left + 1 on right = inner join
    dataframe = dataframe.merge(dispo_alim[['code_pays','produit','dispo_alim_tonnes']])

    # from T to kg
    dataframe['dispo_alim_tonnes'] *= 1000
    
    # to compute ratio
    dataframe[colonne] /= dataframe['dispo_alim_tonnes']

    dataframe.rename(columns={colonne : nom_ratio},inplace=True)

    del dataframe['dispo_alim_tonnes']
    
    return dataframe


def retourner_kcal_prot_ratio(titre_dataframe,
                              liste_colonnes_equilibre_prod,
                              dataframe_table_ratio,
                              origin=''
                             ):
    
    # AJR : 2400 kcal 
    kcal = calculer_personnes_ratio(2400,
                                    liste_colonnes_equilibre_prod,
                                    'ratio_energie_poids',
                                    dataframe_table_ratio,
                                    origin
                                   )
    
    # AJR : 50gr ==> 50/1000 kg 
    prot = calculer_personnes_ratio(50 / 1000,
                                    liste_colonnes_equilibre_prod,
                                    'ratio_proteines',
                                    dataframe_table_ratio,
                                    origin
                                   )
    
    # to create dataframe
    dataframe = pd.DataFrame(data = {
                                     'unité'       : ['calories',
                                                      'protéines'],
        
                                     'nb_personnes': [kcal[0],
                                                      prot[0]],
                                     
                                     'pourcentage' : [kcal[1],
                                                      prot[1]]
                                    },
                            )
    return dataframe


def donner_proportion (col1_equilibre_prod,col2_equilibre_prod,is_cumulative,liste_restriction=[]):
    
    # SELECT FROM
    e = equilibre_prod[[col1_equilibre_prod,col2_equilibre_prod,'code_produit']].copy()

    # WHERE code_produit IN liste_cereales
    e = e[e['code_produit'].isin(liste_restriction)]
        
    if is_cumulative:
        
        proportion = ((e[col1_equilibre_prod].sum() * 100) /
                      (e[col1_equilibre_prod].sum() + e[col2_equilibre_prod].sum()))
    else:
        
        proportion = (e[col1_equilibre_prod].sum() * 100) / (e[col2_equilibre_prod].sum())

    return proportion


def china_duplicates(dataframe):
    
    duplicates = (96,128,41,214)
    
    # to find duplicates'id
    index_list = dataframe[dataframe['code_pays'].isin(duplicates)].index
        
    # to drop rows with duplicates'id
    dataframe.drop(index=index_list,inplace=True)
    
    return dataframe


# to give a label with a code_pays
def dataframe_merge_pays(dataframe):
    
    name_pays = pd.read_csv(path + csv_population, 
                            usecols=['Zone','Code zone'],
                            dtype={'Code zone':'int64'}
                           )

    name_pays.rename(columns={'Code zone':'code_pays',
                              'Zone': 'pays'
                             },
                     inplace=True
                    )
    
    name_pays = name_pays.drop_duplicates()  
    
    name_pays = china_duplicates(name_pays)    
    
    return dataframe.merge(name_pays, how = 'left')


# to give a label with a code_produit
def dataframe_merge_produit(dataframe):
    
    columns = ['Code Produit', 'Produit']

    name_produit = pd.read_csv(path + csv_vegetaux,  usecols=columns)
    temp = pd.read_csv(path + csv_animaux ,  usecols=columns)
    
    name_produit = name_produit.merge(temp, how = 'outer')
    name_produit = name_produit.drop_duplicates()
    
    name_produit.rename(columns={'Code Produit' : 'code_produit',
                                 'Produit'      : 'produit'
                                },
                        inplace = True
                       )
    
    return dataframe.merge(name_produit, how = 'left')


# to create dataframe/table
def dataframe_table(table_name ,columns_list, core_dataframe):
    # to select columns from core_dataframe
    dataframe = core_dataframe[columns_list]

    # to order columns
    dataframe = dataframe[columns_list]

    # to export to a csv file
    dataframe.to_csv(table_name + '.csv', index = False)
       
    return dataframe


def match_dispo_int (core_dataframe,table_name):
    
    d = core_dataframe.copy()

    if table_name == 'equilibre_prod':
        # to create column to compare to dispo_int
        d['difference'] = (d['alim_ani'] + d['semences'] + d['pertes'] + d['transfo'] 
                           + d['autres_utilisations'] +d['nourriture'])
        
    elif table_name == 'balance_com':
        # to create column to compare to dispo_int
        d['difference'] = d['productions'] + d['importations'] + d['variations'] - d['exportations']
    
    # to test errors
    d = d[d['difference'] != d['dispo_int']]

    if len(d[d['difference'] != d['dispo_int']]) > 0 :
        if table_name == 'equilibre_prod':
            # to fix the difference between dispo_int and difference
            d['autres_utilisations'] = d['autres_utilisations'] - d['difference'] + d['dispo_int']  
            core_dataframe.loc[d.index,'autres_utilisations'] = d['autres_utilisations']
        
        elif table_name == 'balance_com':
            # to fix the difference between dispo_int and difference
            d['variations'] = d['variations'] - d['difference'] + d['dispo_int']   
            core_dataframe.loc[d.index,'variations'] = d['variations']
    else:
        
        return True

def fix_2013_japan_avoine(core_dataframe):
    
    dataframe_row  = core_dataframe[  (core_dataframe['annee'       ] == 2013)
                                    & (core_dataframe['code_pays'   ] ==  110)
                                    & (core_dataframe['code_produit'] == 2516)
                                   ].copy()

    # to compute availabilities
    japan_dispo_alim = 72*10**6
    japan_population = 127144000
    
    #from japan table_alim https://www.mext.go.jp/en/policy/science_technology/policy/title01/detail01/1374030.htm
    japan_avoine_kcal_kg = 3800
    
    # from japan table_alim https://www.mext.go.jp/en/policy/science_technology/policy/title01/detail01/1374030.htm
    japan_avoine_ratio_prot = 0.12
    
    dataframe_row['dispo_alim_kcal_p_j'] = japan_dispo_alim * japan_avoine_kcal_kg / japan_population /365
    dataframe_row['dispo_prot']          = japan_dispo_alim * japan_avoine_ratio_prot / japan_population /365 *1000 
    dataframe_row['dispo_mat_gr']        *= (-1)

    # to change balance_com
    dataframe_row['variations']          *= (-1)
    dataframe_row['importations']        *= (-1)
    dataframe_row['exportations']        *= (-1)

    # to change dispo_int
    dataframe_row['dispo_int']          *= (-1)

    # to change equilibre_prod
    dataframe_row['nourriture'] = (  dataframe_row['dispo_int'] 
                                   - dataframe_row['transfo'] 
                                   - dataframe_row['autres_utilisations']
                                   - dataframe_row['alim_ani'] )

    # to change dispo_alim
    dataframe_row['dispo_alim_tonnes'] = dataframe_row['nourriture'] * 1000

    # to apply changes
    core_dataframe.loc[dataframe_row.index] = dataframe_row

def match_availabilities_nourriture_0(core_dataframe):
    dataframe = core_dataframe.copy()
    
    # to select where 'nourriture' = 0
    dataframe = dataframe[dataframe['nourriture'] == 0]
    
    # to put availablities to 0
    dataframe['dispo_alim_kcal_p_j'] = 0
    dataframe['dispo_prot']          = 0
    dataframe['dispo_mat_gr']        = 0

    # to apply changes
    core_dataframe.loc[dataframe.index] = dataframe    
    

# to choose 5 elements from list    
def sample_5(dataframe):
    
    dataframe.reset_index(drop=True, inplace=True)
    
    # to create list for sampling
    sample = list(range(0, len(dataframe.index)))
    
    # to sample from list
    sample = random.sample(sample,5)
    
    # to print results
    for index in sample :
        print(dataframe['produit'][index])
