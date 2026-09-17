class InvalidCsvError(Exception):
    #Fouten met betrekking tot de
    # extensie of het bestaan van het CSV-bestand.
    #
    pass

class MissingColumnError (Exception):
    #Deze fout treedt op
    #als het CSV-bestand de verwachte kolommen mist.
    #
    pass

class MissingRowError (Exception):
    pass

