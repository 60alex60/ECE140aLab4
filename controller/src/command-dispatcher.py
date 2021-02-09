# Time keeping
import time

# Import MySQL Connector Driver
import mysql.connector as mysql

# Import tello
from tellolib import Tello

# Load the DB credentials
import os
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

# At most, send a command every COMMAND_DELAY seconds
COMMAND_DELAY = 1

heart_beat_freq = 10

""" Main Entrypoint """
if __name__ == "__main__":

  # Wait until the database is ready to establish a connection, checking it every second
  while(True):
    try:
      db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
      cursor = db.cursor()
      break
    except:
      time.sleep(1)

  # Create Tello connection
  drone = Tello()

  # Enter into the main event loop
  before = time.time()
  time_last_command_sent = time.time()
  while(True):
    now = time.time()
    if(now - before > COMMAND_DELAY):
      before = now

      # Get the most recent command
      # Take care to select only one pending command that is NOT complete!
      # Use the variable 'response' to hold the command.
      ################################################
      # INSERT CODE TO GET NEXT COMMAND HERE
      ################################################
      response = None
      cursor.execute("select * from Commands where completed=0 order by id")
      response = cursor.fetchall()
      print(response)



      # Check if there was a command in the queue
      if response is not None and response != []:

        time_last_command_sent = now
        print("DEBUG: Command received (dispatcher): ", response)

        currCommand = response[0][1]
        commandID = response[0][0]

        print(currCommand)
        print(commandID)

        ########################################
        # INSERT DRONE CONTROL COMMAND HERE
        ########################################


        drone.send_command(currCommand)

        
        ############################################
        # MARK THE COMMAND AS COMPLETED IN DB HERE
        ############################################

#        sql = "update Commands set completed=1 where id=%s"
#        val = (commandID)
#        cursor.execute(sql, val)

        query = """ UPDATE Commands
                SET completed = %s
                WHERE id = %s """

        data = (1, commandID)


        cursor.execute(query,data)
        db.commit()


      # Else, if time since last command > 10s, query battery to keep connection
      else:
        print("DEBUG: No commands in database queue (dispatcher)")
        if(now - time_last_command_sent > heart_beat_freq):
          print("DEBUG: Query battery level to keep connection (dispatcher)")
          drone.send_command("battery?")
          time_last_command_sent = time.time()