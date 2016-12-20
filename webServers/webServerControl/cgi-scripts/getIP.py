'''
Ce script va tout d'abord vérifier que le demandeur de proxy n'est pas deja dans la liste des profiles
FF les utilisant (identifiant unique) et dans le cas échéant , va reindiquer les informations de proxys
deja données

Dans l'autre cas , ce script va lire une base de donnée contenant des representations objectives de proxy (tel un json)
va les interpreter et renverra sous la forme d'un fichier .pac le premier proxy libre qu'elle trouvera
'''
