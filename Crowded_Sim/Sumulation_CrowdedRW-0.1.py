# -*- coding: utf-8 -*-
"""
Created on Thu May 14 14:47:49 2020

@author: jpnyvs

2つのグループが通路をソーシャルディスタンスを保ちながら横切った際のシミュレーション
"""

import numpy as np
import pandas as pd


############################  パラメータ  ############################

SIMULATION_ITERATION = 300
N_AGENTS_TYPE0 = 100
N_AGENTS_TYPE1 = 100
## 進行方向へのステップサイズ
STEP_SIZE = 1.5
## ランダムウォーク係数（正規分布からの乱数へかける値）
DISTURBANCE = 0.8
## 初期位置幅
INITIAL_RANGE_TYPE0_X = {'min':0,'max':20}
INITIAL_RANGE_TYPE0_Y = {'min':30,'max':50}   # Type0の移動時の制約でもある
INITIAL_RANGE_TYPE1_X = {'min':30,'max':50}   # Type1の移動時の制約でもある
INITIAL_RANGE_TYPE1_Y = {'min':0,'max':20}
## ソーシャルディスタンス（次のステップを実施しないエージェント間の半径）
STOP_DISTANCE = 2

SAVE_CSV_NAME = 'crowded2.csv'

###################################################################


class Agent():
    """ 各エージェント
    """
    def __init__(self, agent_name=None, agent_type=None, step_size=STEP_SIZE, disturbance=DISTURBANCE):
        self.agent_name = agent_name
        self.agent_type = agent_type    # 0 or 1
        self.step_size = step_size
        self.disturbance = disturbance
        self.step = 0    # 現在のステップ数
        if self.agent_type==0:    # agent_typeで初期位置を分ける
            initial_location_x = np.random.randint(INITIAL_RANGE_TYPE0_X['min'], INITIAL_RANGE_TYPE0_X['max'])
            initial_location_y = np.random.randint(INITIAL_RANGE_TYPE0_Y['min'], INITIAL_RANGE_TYPE0_Y['max'])
        else:
            initial_location_x = np.random.randint(INITIAL_RANGE_TYPE1_X['min'], INITIAL_RANGE_TYPE1_X['max'])
            initial_location_y = np.random.randint(INITIAL_RANGE_TYPE1_Y['min'], INITIAL_RANGE_TYPE1_Y['max'])
        self.location = {'x': initial_location_x, 'y': initial_location_y}    # 現在位置
        #self.location_next = {'x_next':0, 'y_next':0}
        self.location_history = {'time':[self.step], 'x':[self.location['x']], 'y':[self.location['y']]}

    def next_location(self):
        # 予定移動位置
        if self.agent_type==0:    # agent_type別での移動方向
            # x方向へ移動
            x_next = self.location['x'] + self.step_size + np.random.randn() * self.disturbance
            y_next = self.location['y'] + np.random.randn() * self.disturbance
            # 次のステップが枠外の場合、その軸へは移動しない（y方向での制約）
            if (y_next < INITIAL_RANGE_TYPE0_Y['min']) or (y_next > INITIAL_RANGE_TYPE0_Y['max']):
                y_next = self.location['y']
        else:
            # y方向へ移動
            x_next = self.location['x'] + np.random.randn() * self.disturbance
            y_next = self.location['y'] + self.step_size + np.random.randn() * self.disturbance
            # 次のステップが枠外の場合、その軸へは移動しない（x方向での制約）
            if (x_next < INITIAL_RANGE_TYPE1_X['min']) or (x_next > INITIAL_RANGE_TYPE1_X['max']):
                x_next = self.location['x']
                
        # 次のステップに他エージェントが居た場合、移動をしない
        for agent_key, agent_location in AgentsCurrentLocations.agents_locations.items():
            if agent_key == self.agent_name:    # 自分との比較はスキップ
                continue
            # 自分の次の位置と他エージェント(agent_name_key)との距離比較
            distance = (x_next - agent_location['x'])**2 + (y_next - agent_location['y'])**2
            if distance < STOP_DISTANCE**2:
                print("Agent {} faces with another agent {}".format(self.agent_name ,agent_key))
                x_next = self.location['x']
                y_next = self.location['y']
                break
        
        self.step += 1
        self.location['x'] = x_next
        self.location['y'] = y_next
        self.location_history['time'].append(self.step)
        self.location_history['x'].append(x_next)
        self.location_history['y'].append(y_next)
    
    def print_name_location(self):
        print( "name={}, x={}, y={}".format(self.agent_name, self.location['x'], self.location['y']) )


class AgentsCurrentLocations():
    """" 全エージェントの現在のロケーションを格納
    """
    agents_locations = {}


class PlaySimulation():
    """ シミュレーション実施用関数のヘルパークラス 
    """
    
    def move_next_locations(self, agents):
        """全てのAgentを1ステップ進める"""
        for agent in agents:
            agent.next_location()
    
    def do_all_steps(self, agents, n_steps):
        """全てのAgentでシミュレーションの全ステップ実施"""
        for i in range(n_steps):
            self.move_next_locations(agents)
            print("Step {} done.".format(i))
            #self.print_agents_names_locations()
    
    def get_simulated_data(self, agents):
        """結果をcsvへ保存"""
        df = pd.DataFrame()
        for agent in agents:
            if df.shape[0]==0:
                df = pd.DataFrame(agent.location_history)
                df['name'] = agent.agent_name
                df['type'] = agent.agent_type
            else:
                df_tmp = pd.DataFrame(agent.location_history)
                df_tmp['name'] = agent.agent_name
                df_tmp['type'] = agent.agent_type
                df = pd.concat([df, df_tmp])
            #print(agent.location_history)
        df = df[['name','type','time','x','y']]
        #print(df)
        df.to_csv(SAVE_CSV_NAME, index=False)
        print('SAVED!!!')
    
    def print_agents_names_locations(self, agents):
        for agent in agents:
            agent.print_name_location()



# 全エージェントをインスタンス化（インスタンスをリストへ格納）
main_agents_type0 = [Agent(agent_name=i, agent_type=0) for i in range(N_AGENTS_TYPE0)]
main_agents_type1 = [Agent(agent_name=N_AGENTS_TYPE0+i, agent_type=1) for i in range(N_AGENTS_TYPE1)]
main_agents = main_agents_type0
main_agents.extend(main_agents_type1)

# 全エージェントの現在位置を格納 {名前:{'x':位置,'y':位置},..}
AgentsCurrentLocations.agents_locations = {main_agent.agent_name:main_agent.location for main_agent in main_agents}

#print(main_agents_locations)
sim = PlaySimulation()
sim.do_all_steps(main_agents, SIMULATION_ITERATION)
#print(main_agents_locations)
    
sim.get_simulated_data(main_agents)


