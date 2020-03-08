# NBA_DAILY_STPR_-_SPR
Thanks for Dyrral Blackport's code and Nathan Walker's SPR(Simple Player Rating)

1. Prepare

pip install pandas

pip install numpy

pip install nba_stats_tracking   # Dyrral Blackport's code, very useful


2. Only Thing to Do

Edit the date you need to caculate SPR or STPR (Simulated-per-100-poss Tracking Player rating: Something I invented to estimate player's attribution of one single game with Single game's Tracking/Hustle stats from NBA.com in consideration and caculation)

For example, if you want to know what happened in 03/07/2020. Just input the data at the below blank and run this programme, and then you will get the SPR and STPR in 2.CSV

(If you want one day's SPR data, the input in 'date_from' SHOULD be same with it in 'date_to')

"""

date_from = '03/01/2020'
date_to = '03/01/2020'


"""

Then you can wait for your device running and get the result you want.

3. Other Staff

If you also want some other data displayed in 2.csv, you can find the staff you want in the list 'staff' as shown below:

"""

staff = ['PLAYER_NAME',
     'TEAM_ABBREVIATION',
     'DRIVES',
     'DRIVE_PASSES',
     'PULL_UP_FGA',
     'CATCH_SHOOT_FGA',
     'ELBOW_TOUCHES',
     'POST_TOUCHES',
     'PAINT_TOUCHES',
     'POTENTIAL_AST',
     'PULL_UP_PTS_y',
     'CATCH_SHOOT_PTS_y',
     'DRIVE_PTS_y',
     'PAINT_TOUCH_PTS',
     'POST_TOUCH_PTS',
     'ELBOW_TOUCH_PTS',
     'DEFLECTIONS',
     'SCREEN_ASSISTS',
     'OFF_BOXOUTS',
     'DEF_BOXOUTS' ,
     'FGM_ic',
     'FGA_ic',
     'FTM',
     'FTA',
     'OREB',
     'TOV',
     'PF',
     'PTS',
     'STL_y',
     'BLK_y',
     'DREB_y',
     'DEF_RIM_FGM',
     'DEF_RIM_FGA',
     'FG3A',
     'AST_y',
     'TS_PCT',
     'USG_PCT',
     'PACE',
     'MIN_c',
     'W_c']
     
     """
     
     And in DataFrame 'result', you can insert some easy code to let it shown in the csv.
     
     4. Finale
     
     Another great appreciation for Dyrral Blackport and Nathan Walker.
     
