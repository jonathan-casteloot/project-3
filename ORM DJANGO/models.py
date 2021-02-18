from django.db import models

class Population(models.Model):
	id_population = models.AutoField(primary_key = True)
	pays          = models.CharField(max_length=100)	
	code_pays     = models.IntegerField()
	annee         = models.IntegerField()
	population    = models.BigIntegerField()

	class Meta:
		unique_together = (('code_pays','annee'),)
		db_table = 'population'

class Sous_nutrition(models.Model):
	id_sous_nutrition = models.AutoField(primary_key = True)
	pays              = models.CharField(max_length = 100)
	code_pays         = models.IntegerField()
	annee             = models.IntegerField()
	nb_personnes      = models.BigIntegerField()

	class Meta:
		unique_together = (('code_pays','annee'),)
		db_table = 'sous_nutrition'

class Dispo_alim(models.Model):
	id_dispo_alim       = models.AutoField(primary_key = True)
	pays                = models.CharField(max_length = 100)
	code_pays           = models.IntegerField()
	annee               = models.IntegerField()
	produit             = models.CharField(max_length = 100)
	code_produit        = models.IntegerField()
	origin              = models.CharField(max_length = 7)
	dispo_alim_tonnes   = models.BigIntegerField()
	dispo_alim_kcal_p_j = models.BigIntegerField()
	dispo_prot          = models.FloatField()
	dispo_mat_gr        = models.FloatField()

	class Meta:
		unique_together = (('annee','code_pays','code_produit'),)
		db_table = 'dispo_alim'

class Equilibre_prod(models.Model):
	id_equilibre_prod   = models.AutoField(primary_key = True)
	pays                = models.CharField(max_length = 100)
	code_pays           = models.IntegerField()
	annee               = models.IntegerField()
	produit             = models.CharField(max_length = 100)
	code_produit        = models.IntegerField()
	dispo_int           = models.IntegerField()
	alim_ani            = models.IntegerField()
	semences            = models.IntegerField()
	pertes              = models.IntegerField()
	transfo             = models.IntegerField()
	nourriture          = models.IntegerField()
	autres_utilisations = models.IntegerField()

	class Meta:
		unique_together = (('annee','code_pays','code_produit'),)
		db_table = 'equilibre_prod'

class Balance_com(models.Model):
	id_balance_com      = models.AutoField(primary_key = True)
	pays                = models.CharField(max_length = 100)
	code_pays           = models.IntegerField()
	annee               = models.IntegerField()
	produit             = models.CharField(max_length = 100)
	code_produit        = models.IntegerField()
	productions         = models.IntegerField()
	importations        = models.IntegerField()
	exportations        = models.IntegerField()
	variations          = models.IntegerField()

	class Meta:
		unique_together = (('annee','code_pays','code_produit'),)
		db_table = 'balance_com'
