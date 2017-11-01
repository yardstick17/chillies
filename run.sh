
if [[ $1 = cluster ]]; then
    # This step makes the container of image which has already sark installed.
    sudo docker-compose up

    # sudo docker-compose scale worker=2 # To increaase workers on docker based cluster computing

   # If bash fails, run bash command only on master docker container
   sudo docker exec chiliesrecipe_master_1  sh -c "sudo hadoop fs -mkdir -p /user/root/"
   sudo docker exec chiliesrecipe_master_1  sh -c "cd;hadoop fs -put chilies_recipe/recipes.json /user/root/recipes.json"

   sudo docker exec chiliesrecipe_master_1  sh -c "spark-submit --master spark://172.19.0.2:7077 /root/chilies_recipe/recipe_difficulty_extractuion.py"

#    sudo docker exec chiliesrecipe_master_1  sh -c "hadoop fs -get /recipes-etl /root/chilies_recipe/recipes-etl"

elif [[ $1 = standalone ]]; then
    # To run master and add workers
    #    /opt/spark/sbin/start-master.sh
    #    /opt/spark/sbin/start-slave.sh spark://0.0.0.0:7077
    spark-submit --master spark://0.0.0.0:7077 recipe_difficulty_extractuion.py

elif [[ $1 = cluster_outputs ]]; then
    sudo docker exec -d sh -c "chiliesrecipe_master_1 hadoop fs -get recipes-etl/result recipes-etl/result"
    spark-submit --master spark://localhost:7077 recipe_difficulty_extractuion.py

else
  echo "Usage: ./setup.sh <string: specify-mode>"
 fi
exit 0
