from pig_util import outputSchema

@outputSchema("Silver:long")
def fill_silver_na(silver):
    if silver:
        return silver
    else:
        return 0
