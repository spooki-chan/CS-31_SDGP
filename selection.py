import pandas as pd

def getIds():
    df = pd.read_csv('newfood.csv', index_col='id')
    df = df.iloc[::-1]
    id = {}
    RdishTypes = df['dishTypes'].tolist()
    
    for i in range(len(RdishTypes)):
       dishType = RdishTypes[i]
       if dishType in id:
           if(len(RdishTypes[dishType]) < 15):
               id[dishType].append(df.iloc[i]['tfdbid'])
       else:
           id[dishType] = [df.loc[i]['tfdbid']]


    del id['(no dishtypes listed']
    return id


if __name__ == "__main__":
    id = getIds()
            