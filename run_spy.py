import text_tagger as tt

#Option to reduce dataframe print size
tt.dataset_manager.pd.options.display.max_colwidth = 20


file = "./datasets_samples/Tweets_USA.csv"
text_column = "Tweet content"
tags_columns = ["Latitude", "Longitude"]

tags_types = {"Lat_Long":("numeric-simple", 200, ["Longitude", "Latitude"])}
filter_flags = {"digits"   : True, "stopwords": True, "text_only": False,
                "simbols"  : True, "punct"    : True, "links"    : True,
                "refs"     : False, "tokenize": True}

languages = ['english']#, 'spanish']
other_stopwords = ["&amp;"]

database = tt.DataBase(file, text_column, tags_columns)
database.open()

preprocess = tt.Preprocess(tags_types, filter_flags, 
                           languages=languages, other_stopwords=other_stopwords)
preprocess.preprocess(database)

database.generate_embedings(method="tf-idf")
database.generate_tags()

database.create_index()

tag_column = "AutoTag"
tag = database.df[tag_column].iloc[-1]

# Para salvar os dados
if False:
    database.export(target="text")
    database.export(target="csv")
    database.save()

# Para o extrator
if False:
    extract = tt.Extract(database)
    print("Number of elements in tag", extract.get_size(tag, tag_column))
    print()
    print("Main Words in tag:")
    print(extract.get_words(tag, tag_column, n_words=10))
    print()
    print("Main Tweets in tag:")
    print(*extract.get_text(tag, tag_column), sep="\n")
    
    extract.get_wordcloud(tag, tag_column)
    
    #extract.get_lda(tag, tag_column)

# Para o Generate
if False:    
    generate = tt.Generate(database, max_sequence_len=16)
    generate.train(tag=tag, tag_column=tag_column)
    generate.generate(seed_text="Want to")


# Para o Indentify
if False:
    identify = tt.Identify(database)
    identify.identify(["I ran a marathon in los Angeles this week and did not win", 
                         "A ball rows down the stairs while the boy watch it go"], method="cbow")