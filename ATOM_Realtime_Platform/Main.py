import os
import codecs
import pandas as pd
from ATOM_Realtime_Platform.RE_function import restart_function as rf

class ATOM_Simulator:
    def __init__(self):
        self.atom_stedy_path = '.\MARS\MARS_KS1.4_bin_Release.exe -i .\MARS\ATOM_steady.i'
        self.atom_restart_path = '.\MARS\MARS_KS1.4_bin_Release.exe -i .\MARS\ATOM_restart.i'
        self.atom_restart_file_path = '.\MARS\ATOM_restart.i'
        self.db_path = './DB.csv'
        self.db = pd.DataFrame()

        self.rf = rf()
    # =============================================================================================================

    def remove_all(self, get_mode):
        if get_mode == 'start':
            # start
            for remove_file in ['coupfl', 'jbinfo', 'outdta', 'plotfl', 'rstplt', 'screen', 'read_steam_comment.o',
                                'fort*']:
                try:
                    os.remove(remove_file)
                except:
                    pass
        elif get_mode == 'restart':
            # restart
            for remove_file in ['coupfl', 'jbinfo', 'outdta', 'plotfl']:
                try:
                    os.remove(remove_file)
                except:
                    pass
    # =============================================================================================================
    # DB part

    def make_para_str(self):
        temp_data = pd.read_csv('plotfl', sep='\s+')
        list_column = temp_data.columns.to_list()  # Type ex. p
        list_column_new = [_.split('.')[0] for _ in list_column]
        list_column_nub = temp_data.iloc[0].to_list()  # Number ex. 805010000
        re_name_list = [f'{col}_{int(name)}' for col, name in zip(list_column_new, list_column_nub)]
        # Update parameter name
        self.db = pd.DataFrame(columns=re_name_list)
        # Add 0 sec
        self.db.loc[0] = temp_data.iloc[1].to_list()
        # Add 1 sec
        self.db.loc[1] = temp_data.iloc[2].to_list()

    def update_db(self):
        temp_data = pd.read_csv('plotfl', sep='\s+')
        # Add last data to self.db
        self.db.loc[len(self.db)] = temp_data.iloc[-1].to_list()

    def save_db(self):
        self.db.to_csv(self.db_path)
    # =============================================================================================================
    # Make restart file

    def make_restart_file(self):
        start_line = f'= Restart\n100 restart transnt\n101 run\n102 si si\n103 -1\n' \
                     f'201 {float(len(self.db)+100)} 1.0e-7 0.05 3 20 400 50000\n'
                     # f'202 {float(len(self.db))} 1.0e-7 0.05 23 200 500 1000\n'

        # -------- control line ---------------
        control_line = ''

        if 110 < len(self.db)+100 <= 120:
            control_line += self.rf.Comp_915(time=float(len(self.db)+100), state='On')
        else:
            control_line += self.rf.Comp_915(time=float(len(self.db)+100), state='Off')

        # -------------------------------------
        end_line = '.'
        # Save restart file
        with open(self.atom_restart_file_path, 'w') as f:
            f.write(start_line+control_line+end_line)

    # =============================================================================================================
    # Run simulator

    def run_simulator(self):
        print('Start_MARS')
        self.remove_all(get_mode='start')
        initial_output = os.popen(self.atom_stedy_path).read()
        print(initial_output)

        # initial parameter setting
        self.make_para_str()

        while True:
            # Modify restart file
            self.make_restart_file()
            # run
            self.remove_all(get_mode='restart')
            output = os.popen(self.atom_restart_path).read()
            print(output)
            self.update_db()
            self.save_db()
            pass


if __name__ == '__main__':
    ATOM = ATOM_Simulator()
    ATOM.run_simulator()