""" CeleryTasks are defined here
"""
from Common import *
import os

SENSITIVE_WORDS = {
    "secret" : 10,
    "dathena" : 7,
    "internal" : 5,
    "external" : 3,
    "public" : 1,
}

# uncomment for periodic updating of scores, else one is tasked everytime a file is uploaded
# @celery.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(
#         10.0,
#         #crontab(minute = '*/30'), #every 30mins
#         Update_Scores.s(), name='Update scores periodically'
#         )

@celery.task
def Update_Scores():
    """ Retrieves all the files in the DB and updates their sensitivity_score
    """
    #grab data from db
    conn = dbObject.GetConnection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM files')
        res = cur.fetchall()

        if res is not None:
            for record in res:
                if os.path.isfile(record[3]):
                    score = Build_Word_Count(record[3])
                    try:
                        cur.execute(
                            'UPDATE files SET sensitivity_score = (%s), last_updated = NOW() WHERE id = (%s)',
                            (score, record[0])
                        )
                        if res is not None:
                                conn.commit()
                        else:
                            raise Exception("Updating of password hash failed")
                    except (Exception, psycopg2.DatabaseError) as error:
                        conn.rollback()
            

    except (Exception, psycopg2.DatabaseError) as error:
            print(error)


def Build_Word_Count(filepath):
    """ Builds the word count for a text file and returns the sensitivity score

    Args:
        filepath : path to file for reading

    Returns:
        sensitivity score of the file
    """
    all_words = {}
    file = open(filepath, "r")

    for line in file:
        line = line.strip()
        line = line.lower()

        words = line.split(" ")

        for word in words:
            if word in all_words:
                all_words[word] = all_words[word] + 1
            else:
                all_words[word] = 1

    score = 0
    for word in list(all_words.keys()):
        #print(word, all_words[word])
        if word in SENSITIVE_WORDS.keys():
            #print(SENSITIVE_WORDS[word])
            score = score + SENSITIVE_WORDS[word]

    return score

if __name__ == '__main__':
    pass