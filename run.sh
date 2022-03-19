#python no_locking_map_run.py &
#python no_locking_map_run.py &
#python no_locking_map_run.py

#python pessimistic_locking_map_run.py &
#python pessimistic_locking_map_run.py &
#python pessimistic_locking_map_run.py

#python optimistic_locking_map_run.py &
#python optimistic_locking_map_run.py &
#python optimistic_locking_map_run.py

python queue_producer.py --port 5701 &
python queue_consumer.py --port 5702 &
python queue_consumer.py --port 5703