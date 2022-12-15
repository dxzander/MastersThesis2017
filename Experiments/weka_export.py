def weka_export(vectors, classes_names, attributes, title, output_file, classes = []):
	# la varible vectors es una lista de los vectores que le vas a pasar a weka. por default,
	# esta implementación espera que la última dimensión de cada vector sea la clase a la que pertenece.
	# también se incluye código para vectores cuyas clases vienen en una variable aparte,y código para
	# vectores que son diccionarios y cuyas dimensiones y clases se encuentran en sus llaves correspondientes.

	# la variable classes es opcional, y está ahí por si las clases de los vectores se encuentran en una
	# lista aparte.

	# la variable classes_names es una lista con los nombres de cada clase. por ejemplo:
	# classes = ['control', 'depressed']

	# la varible attributes es una lista con el nombre de cada atributo que conforma los vectores.
	# o sea, el nombre de lo que representa cada dimensión de los vectores, en orden. es necesario para el archivo weka.
	# por ejemplo, en vectores de bolsa de plabras esta variable es la lista de las palbras.
	# en el caso de que los vectores tengan en su última dimensión la clase a la qu pertenecen,
	# no hay que incluír una descripción para esta dimensión.
	# si tus vectores no tienen un nombre para cada dimensión, como las neuronas de una red, solo enuméralas.

	# la variable title debe de ser un string. es necesario para el archivo weka. no debe tener espacios.
	# por ejemplo:
	# title = 'depression_posts'

	# la variable output_file es un string del nombre del archivo. recuerda ponerle extensión .arff
	# *imitando a un perro* arff! arff!

	# create file
	with open(output_file, 'w') as f:
		# file header
		f.write('@RELATION ' + title + '\n')
		f.write('\n')
		for attribute in range(len(attributes)):
			# esto crea la lista de atributos en el archivo. esta implementación asume que todos los
			# atributos son del tipo numérico. el tipo numérico de weka no distingue entre flotante y 
			# entero. si requirieras algo distinto puedes consultar en la documentación de weka:
			# https://www.cs.waikato.ac.nz/ml/weka/arff.html
			f.write('@ATTRIBUTE attr' + str(attribute) + ' NUMERIC %' + str(attributes[attribute]) + '\n')
		f.write('@ATTRIBUTE class {' + ','.join(classes_names)  + '}\n')
		f.write('@DATA' + '\n')

		# data section
		# para vectores cuya última dimensión es su clase
		for vector in vectors:
			f.write(','.join(str(x) for x in vector) + '\n')

		# para vectores cuyas clases vienen en una variable aparte
		# for instance in (vectors, classes):
		# 	f.write(','.join(str(x) for x in instance[0]) + ',' + str(instance[1]) + '\n')

		# para vectores cuya información viene en un diccionario.
		# cambiar los nombres de las llaves a lo que se necesite.
		# for vector in vectors:
		# 	f.write(','.join(str(x) for x in vector['vector']) + ',' + str(classes[vector['class']]) + '\n')