import text_tagger as tt

file = "./datasets_samples/Tweets_USA.csv"
text_column = "Tweet content"
tags_columns = ["Latitude", "Longitude"]

tags_types = {"Lat_Long":("numeric-simple", 200, ["Longitude", "Latitude"])}
filter_flags = {"digits"   : True, "stopwords": True, "text_only": False,
                "simbols"  : True, "punct"    : True, "links"    : True,
                "refs"     : True}

languages = ['english']#, 'spanish']

database = tt.DataBase(file, text_column, tags_columns)
database.open()

preprocess = tt.Preprocess(tags_types, filter_flags, languages=languages)
preprocess.preprocess(database)

database.export(target="text")
database.export(target="csv")

database.generate_embedings(method="tf-idf")
database.generate_tags()

database.create_index()

database.save() 

tag_column = 0
tag = database.df[database.tags_columns[tag_column]].iloc[-1]


tt.Generate(max_sequence_len = 16).run(database, tag=tag, tag_column=tag_column)
