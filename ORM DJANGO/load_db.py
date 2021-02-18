import pandas as pd 

from fao_database.models import *
from django.db import transaction

script_path = './scripts/'

dataframe_name = {0     : 'population',
			      1 : 'sous_nutrition',
			      2     : 'dispo_alim',
			      3 : 'equilibre_prod',
			      4   : 'balance_com'
			     }


population     = pd.read_csv(script_path + dataframe_name[0] + '.csv', header = 0)
sous_nutrition = pd.read_csv(script_path + dataframe_name[1] + '.csv', header = 0)
dispo_alim     = pd.read_csv(script_path + dataframe_name[2] + '.csv', header = 0)
equilibre_prod = pd.read_csv(script_path + dataframe_name[3] + '.csv', header = 0)
balance_com    = pd.read_csv(script_path + dataframe_name[4] + '.csv', header = 0)

def run():

	with transaction.atomic():

		print(dataframe_name[0])
		for row in population.itertuples():

			Population.objects.create(pays       = row[1],
								      code_pays  = row[2],
								      annee      = row[3], 
								      population = row[4]
								     )



		print(dataframe_name[1])
		for row in sous_nutrition.itertuples():

			Sous_nutrition.objects.create(pays         = row[1],
									      code_pays    = row[2], 
									      annee        = row[3], 
									      nb_personnes = row[4]
									     )


		print(dataframe_name[2])
		for row in dispo_alim.itertuples():

			Dispo_alim.objects.create(pays                = row[ 1], 
								      code_pays           = row[ 2], 
								  	  annee               = row[ 3], 
								      produit             = row[ 4],
								      code_produit        = row[ 5],
								      origin              = row[ 6],
								      dispo_alim_tonnes   = row[ 7],
								      dispo_alim_kcal_p_j = row[ 8],
								      dispo_prot          = row[ 9],
								      dispo_mat_gr        = row[10]
								     )


		print(dataframe_name[3])
		for row in equilibre_prod.itertuples():

			Equilibre_prod.objects.create(pays                = row[ 1], 
								          code_pays           = row[ 2], 
								          annee               = row[ 3], 
								          produit             = row[ 4],
								          code_produit        = row[ 5],
								          dispo_int           = row[ 6],
								          alim_ani            = row[ 7],
								          semences            = row[ 8],
								          pertes              = row[ 9],
								          transfo             = row[10],
								          nourriture          = row[11],
								          autres_utilisations = row[12]
								         )



		print(dataframe_name[4])
		for row in balance_com.itertuples():

			Balance_com.objects.create(pays         = row[1], 
								       code_pays    = row[2], 
								       annee        = row[3], 
								       produit      = row[4],
								       code_produit = row[5],
								       productions  = row[6],
								       importations = row[7],
								       exportations = row[8],
								       variations   = row[9]
								      )





