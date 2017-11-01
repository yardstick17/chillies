
if [[ $1 = cluster ]]; then
    sudo docker-compose scale worker=2

    sudo hadoop fs -mkdir -p /user/root/

    #    sudo hadoop fs -put recipes.json /recipes.json
    sudo docker exec chiliesrecipe_master_1  sh -c "cd;hadoop fs -put chilies_recipe/recipes.json /user/root/recipes.json"
    sudo docker exec chiliesrecipe_master_1  sh -c "spark-submit --master spark://172.19.0.2:7077 /root/chilies_recipe/recipe_difficulty_extractuion.py"

    sudo docker exec -it chiliesrecipe_master_1  bash
#    sudo docker exec chiliesrecipe_master_1  sh -c "hadoop fs -get /recipes-etl /root/chilies_recipe/recipes-etl"

elif [[ $1 = standalone ]]; then
    /opt/spark/sbin/start-master.sh
    /opt/spark/sbin/start-slave.sh spark://0.0.0.0:7077
    spark-submit --master spark://0.0.0.0:7077 recipe_difficulty_extractuion.py
elif [[ $1 = cluster_outputs ]]; then
    sudo docker exec -d sh -c "chiliesrecipe_master_1 hadoop fs -get recipes-etl/result recipes-etl/result"
    spark-submit --master spark://localhost:7077 recipe_difficulty_extractuion.py

else
  echo "Usage: ./setup.sh <string: specify-mode>"
 fi
exit 0
