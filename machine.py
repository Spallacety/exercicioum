from sklearn.naive_bayes import MultinomialNB

# é pintado?
# tem bigode?
# tem presas grandes?
# mia?

ocelot1 = [1, 1, 1, 0]
ocelot2 = [1, 1, 1, 0]
ocelot3 = [1, 0, 1, 0]
ocelot4 = [1, 0, 1, 0]
cat1 = [1, 1, 0, 1]
cat2 = [0, 1, 0, 1]
cat3 = [0, 0, 1, 1]
cat4 = [1, 0, 0, 1]

data = [ocelot1, ocelot2, ocelot3, ocelot4, cat1, cat2, cat3, cat4]

markers = ['ocelot', 'ocelot', 'ocelot', 'ocelot', 'cat', 'cat', 'cat', 'cat']

mysterious2 = [0, 0, 0, 1] #T 'cat'
mysterious3 = [0, 0, 1, 0] #T 'ocelot'
mysterious4 = [0, 0, 1, 1] #T 'cat'
mysterious6 = [0, 1, 0, 1] #T 'cat'
mysterious7 = [0, 1, 1, 0] #F 'ocelot'
mysterious8 = [0, 1, 1, 1] #T 'cat'
mysterious9 = [1, 0, 0, 0] #T 'ocelot'
mysterious10 = [1, 0, 0, 1] #T 'cat'
mysterious11 = [1, 0, 1, 0] #T 'ocelot'
mysterious12 = [1, 0, 1, 1] #T 'cat'
mysterious13 = [1, 1, 0, 0] #T 'ocelot'
mysterious14 = [1, 1, 0, 1] #T 'cat'
mysterious15 = [1, 1, 1, 0] #T 'ocelot'
mysterious16 = [1, 1, 1, 1] #T 'cat'

# ~92,85%

mysterious_list = [mysterious2, mysterious3, mysterious4, mysterious6, mysterious7, mysterious8, mysterious9, mysterious10, mysterious11, mysterious12, mysterious13, mysterious14, mysterious15, mysterious16]

model = MultinomialNB()
model.fit(data, markers)
print(model.predict(mysterious_list))