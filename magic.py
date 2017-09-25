
import os
import json
import numpy as np
import pandas as pd
import urllib
import zipfile


json_dir = "data/"
magic_data_dir = json_dir + 'magic-cards-json/'

def get_df():

    if not os.path.exists( magic_data_dir + "AllSets.json" ):
        os.makedirs( magic_data_dir )
        url = 'https://mtgjson.com/json/AllSets.json.zip'
        f, _ = urllib.request.urlretrieve( url )
        zipfileobject = zipfile.ZipFile( f )
        zipfileobject.extractall( magic_data_dir )

    allsets = json.load( open( magic_data_dir + "AllSets.json", 'r' ) )
    data = []
    for s in list( allsets.keys() ):
        data += allsets[s]['cards']

    df = pd.DataFrame( data )
    df = df.set_index( ['multiverseid'] )
    df = fix_enchantcreature( df )
    df = fix_type_leadingspace( df )
    df = add_iscreature( df )
    return df

def fix_type_leadingspace( df ):
    df.type = df.type.str.replace( '^ ', '' )
    return df

def fix_enchantcreature( df ):
    bad = df.type == 'Enchant Creature'
    df.loc[ bad, 'types' ] = [ 'Enchantment' ]
    df.loc[ bad, 'type' ] = 'Enchantment'
    return df

def add_iscreature( df ):
    df['is_creature'] = df['type'].str.contains( 'Creature' )
    df['is_enchantment'] = df['type'].str.contains( 'Enchantment' )
    df['is_artifact'] = df['type'].str.contains( 'Artifact' )
    df['is_instant'] = df['type'].str.contains( 'Instant' )
    df['is_sorcery'] = df['type'].str.contains( 'Sorcery' )
    return df


if __name__ == "__main__":
    df = get_df()
    print( df.head() )
