import pickle
from pyexpat import model
from sys import api_version
from this import d

cosine_sim = pickle.load(open('./cosine_sim.pickle','rb'))
df = pickle.load(open('df.pickle','rb'))
svd = pickle.load(open('svd.pickle', 'rb'))


def hybrid(userId,title):
    idx = df[df.title==title].index.values[0]
    tfdbId = df[df.title==title]['tfdbId'].values[0]
    recipe_id = df[df.title==title]['recipeId'].values[0]
    sim_scores = list(enumerate(cosine_sim[int(idx)]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:26]
    recipe_indices = [i[0] for i in sim_scores]
    recipes = df.iloc[recipe_indices][['title','ingredients','id','recipeId','image']]

    recipes['est'] = recipes['recipeId'].apply(lambda x: svd.predict(userId, x).est)

    recipes = recipes.sort_values('est', ascending=False)
    return recipes.head(10)

   

print(hybrid(2,"Roasted Peppers with Boquerones"))


# deploy it in the flask
# Make the frontend
# show users their recommendation





