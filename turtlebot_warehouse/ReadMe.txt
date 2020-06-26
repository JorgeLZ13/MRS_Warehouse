*********************************************************************
*******************BASE DE MARCAÇÃO PARA WAREHOUSE*******************
*********************************************************************

Após fazer o download do arquívo crie uma pacote dentro da sua pasta
de simulação do tutlebot (turtlebot_simulator) com o nome turtlebot_warehouse.


catkin_create_pkg turtlebot_warehouse


Copie as pastas launch e world para dentro do seu novo pacote.

Copie a pasta warehouse para o diretório de modelos do gazebo (.gazebo/models)

Em seguida faça um catkin_make em seu catkin do turtlebot.

Após o comando source basta acessar o seu turtlebot warehouse.


roslaunch turtlebot_warehouse turtle_warehouse.launch
